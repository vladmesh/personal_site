# Проект: персональный сайт Влад Меш

## Текущий статус

**Архитектура**: Микросервисная (Frontend + Backend + PostgreSQL)
**Технологии**: Astro + Tailwind (frontend), FastAPI + SQLAlchemy + Alembic (backend)
**Инфраструктура**: Docker Compose, Caddy, GitHub Actions
**Деплой**: ✅ live на https://vladmesh.dev (push в main → автодеплой, Let's Encrypt TLS)
**CI/CD**: ✅ ускорен ~8 мин → ~3 мин

## Цели первой итерации

- ✅ Сформировать статичный сайт-визитку на Astro + Tailwind.
- ✅ Подготовить RU/EN локализации с одинаковой структурой контента.
- ✅ Описать инфраструктуру деплоя (Caddy + Docker Compose + GitHub Actions).
- ✅ **Реструктурировать проект под микросервисную архитектуру.**
- ✅ **Создать backend сервис с FastAPI + SQLAlchemy + Alembic.**

## Завершено в текущей итерации

- ✅ Создана микросервисная структура (`infra/`, `services/`, `shared/`)
- ✅ Frontend мигрирован в `services/frontend/`
- ✅ Backend создан с async SQLAlchemy и Alembic
- ✅ Docker Compose для dev и prod окружений
- ✅ Makefile для управления сервисами
- ✅ Базовая структура API с health check endpoint
- ✅ Обновлена документация
- ✅ Модели контента + read-API (`/api/v1/profile/*`, агрегатор `/full`)
- ✅ Админка sqladmin (парольная аутентификация)
- ✅ Frontend интегрирован с backend API (`/profile/full`)
- ✅ Рабочий CI/CD: образы в ghcr, автодеплой на VPS, Caddy + автовыпуск TLS
- ✅ GitHub Secrets и доступ к VPS настроены
- ✅ **CI/CD ускорен ~8 мин → ~3 мин** (PR #10): кеш Docker-слоёв (`type=gha`), параллельная сборка backend/frontend, пересборка только изменившегося сервиса (path-фильтры), один прогон `pytest --cov` вместо трёх, единая lint+test джоба, health-poll вместо фиксированного `sleep`, docs-only пуши деплой не триггерят.

## Бэклог следующих шагов

### 0. Шаблонизация: контент vs структура (Приоритет: ПЕРВЫЙ)

Цель: репозиторий без персональных данных, всё наполняется через БД/админку.
Структурированный контент (опыт, проекты, навыки, отзывы, контакты, резюме) уже
едет из backend через `/api/v1/profile/full`. Осталось вынести остаток.

Граница, которую держим:
- **Site-config** (бренд, домен, analytics, дефолтная локаль, пути CV) — `src/config/site.ts` + env, не админка.
- **Редактируемый контент** (hero, about + уже готовые секции) — БД + админка.
- **UI-лейблы** (навигация, заголовки секций, CTA) — i18n-строки в коде.

Разбивка по PR:
- [ ] **PR 1 — зачистка и siteConfig** (ветка `chore/templatize-site-config`): удалён легаси `site/`; `links.ts`/`ui.ts`/analytics/мета сведены в `siteConfig` с нейтральными плейсхолдерами и env-домен через `SITE_URL`; чинит баг двойного `@` в email. Остаётся только нарратив Hero/About в `home.ts` (→ PR 2).
- [ ] **PR 2 — Hero/About в backend**: модель `SiteContent` (per-locale: eyebrow, greeting, subtitle, about-заголовок и абзацы) + отдача в `/full` + sqladmin-вьюшка + провод в `home.ts`; удалить захардкоженный текст. После этого вся главная редактируется через `/admin`.
- [ ] **PR 3 — обезличить seed**: убрать персональные данные из `seed_contacts_data.py` / `seed_profile_content.py` (или вынести в опциональный example-seed), чтобы чистая БД поднималась пустой.

### 1. Контент (Приоритет: ПОСЛЕ шаблонизации)
P0 воронки: сайт живой, но контент — заглушки. Правится в `/admin` без передеплоя.
   - [ ] Репозишн Hero/About под Technical & Security Health Check.
   - [ ] Заменить dev-проекты на обезличенные кейсы (ситуация → что нашёл → результат, с цифрами).
   - [ ] Секция оффера/услуг.
   - [ ] Добавить RU PDF резюме в `public/cv/` (сейчас только en).
   - [ ] Сгенерировать OG-изображения для страниц и кейсов.

### 2. UI/UX
   - [ ] Настроить адаптивные отступы и анимации (Astro transitions).
   - [ ] Продумать печатную версию `/ru/cv`.

### 3. Технический долг
   - [ ] Обновить версии GitHub Actions — `actions/checkout`, `docker/build-push-action@v5→v6`, `docker/login-action`, `docker/setup-buildx-action`, `dorny/paths-filter` ещё на Node 20 (CI пишет deprecation-варнинг, форсится на Node 24). Бамп уберёт варнинг.
   - [ ] Настроить ESLint/Prettier и husky-hooks.
   - [ ] Подключить Plausible (сменить `data-domain`).
   - [ ] Включить sitemap/robots + hreflang для вложенных страниц.
   - [ ] Добавить `.dockerignore`, убрать неиспользуемый `development` stage из Dockerfile (см. `INFRA_AUDIT.md`).
   - [ ] Аутентификация админки: сейчас пароль (sqladmin); при необходимости — OAuth2/JWT.

### 4. Инфраструктура
   - [ ] Добавить мониторинг uptime (UptimeRobot/BetterStack).
   - [ ] Настроить backup стратегию для PostgreSQL (cron `pg_dump` + off-site).

### 5. Итерация 2+
   - [ ] Реализовать Cloudflare Worker для формы контактов.
   - [ ] Поддержка UTM-трекера и коротких ссылок.
   - [ ] Сбор отдельных PDF-профилей под вакансии.
   - [ ] Добавить admin dashboard с аналитикой.

## Отдельные вопросы

- Нужна ли отдельная страница "About" или достаточно блока в Hero?
- Нужны ли дополнительные языки (например, немецкий)?
- Планируется ли блог/новости?

Ответы помогут уточнить дальнейший бэклог.
