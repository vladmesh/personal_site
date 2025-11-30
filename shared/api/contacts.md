# Contacts API

- **Endpoint:** `GET /api/v1/profile/contacts`
- **Auth:** none (public)
- **Purpose:** вернуть список контактов с переводами; отображать только `is_visible=true` на фронте.

## Response model
```json
[
  {
    "id": "uuid",
    "type": "email | telegram | github | linkedin | phone | whatsapp | github_repo | ...",
    "value": "mailto/https/tel value",
    "icon": "string|null",
    "is_visible": true,
    "sort_order": 1,
    "translations": [
      { "language_code": "en", "label": "Email" },
      { "language_code": "ru", "label": "Email" }
    ]
  }
]
```

### Поля
- `type` — машинное имя контакта; фронт маппит в href (`mailto:`/`tel:`/`https://`).
- `value` — голое значение (без `mailto:`), кроме случаев, где оно уже URL (GitHub/LinkedIn/Telegram/WhatsApp).
- `translations[*].label` — подписи по языкам; если нет подходящего языка, фронт использует английский, затем любой.
- `sort_order` — порядок отображения (возрастание).
- `is_visible` — скрытые записи не должны отображаться в UI, но могут использоваться как fallback для ссылок (например, phone).

## Примечания для фронта
- При отсутствии перевода для нужного языка брать `en`, затем первый доступный.
- Типы, которые требуют схемы:
  - `email` → `mailto:{value}`
  - `phone` → `tel:{value}`
  - остальные → `value` как есть (должен быть валидный URL).
- Блоки, которых нет в API, остаются статичными: `links.cv`, `links.analytics`, `links.demos`.
