# Задача: переключить контакты на backend API

Контекст: фронтенд сейчас тянет контакты из захардкоженного `src/data/links.ts`, а в бэкенде уже есть `/api/v1/profile/contacts` + сиды. Эта доработка даст первый реальный кусок данных с бэка, создаст базовый HTTP-клиент и покажет паттерн миграции остальных секций.

## Что уже готово
- API `GET /api/v1/profile/contacts` реализован, сиды добавлены (`seed_contacts_001`).
- CORS по умолчанию открыт для localhost (config.py + infra/.env.example).

## План итерациями
1) Подготовка контракта и конфигов  
   - Зафиксировать URL и схему ответа (`ContactRead` + `translations`) в `docs` или `shared/api`.  
   - Добавить переменную `PUBLIC_API_BASE_URL` (dev/prod) в `services/frontend/.env.example` и описать в README/frontend.  
   - Для прод: расширить `BACKEND_CORS_ORIGINS` нужными доменами (localhost уже покрыт).

2) Базовый HTTP-клиент во фронте  
   - Создать модуль `src/lib/api/client.ts` с typed fetch-оберткой (base URL из env, timeout, throw на non-2xx).  
   - Добавить типы ответа `ContactApiModel`/`ContactTranslationApiModel` (пока ручные, позже можно сгенерировать из OpenAPI).

3) Адаптер контактов  
   - Написать `src/lib/profile/contacts.ts` с функцией `fetchContacts(lang)` → нормализованный объект/массив, который можно подставить в UI.  
   - В адаптере выбирать перевод по `language_code`, сортировать по `sort_order`, учитывать `is_visible`, маппить `type` → href (mailto/tel/https).  
   - Оставить fallback на статические `links` для полей, которых еще нет в API (cv, analytics, demos).

4) Интеграция в страницы  
   - В `pages/*/index.astro` загрузить контакты через `Astro.fetch` или клиентский остров (решить стратегию: build-time vs runtime для `output: static`).  
   - Пробросить данные в Hero (cta href), блок "Contact", и в любые компоненты, которые используют `links`.  
   - Обновить `src/data/home.ts` так, чтобы контактные ссылки приходили из адаптера, а не из хардкода.

5) Состояния загрузки и ошибки  
   - Добавить легкий лоадер/плейсхолдер для CTA и contact-блока; при ошибке показывать статический fallback и логировать в консоль.  
   - Убедиться, что билд не падает, если API временно недоступно (например, `try/catch` + graceful degradation).

6) Проверки и документация  
   - Ручной прогон: dev-стек в compose, проверить обе локали RU/EN, что скрытые контакты не отображаются.  
   - Добавить заметку в `docs/PROJECT_PLAN.md` или `services/frontend/README.md` про источник данных контактов и стратегию деградации.  
   - Зафиксировать TODO для следующих секций (projects, experience, testimonials) по тому же паттерну.
