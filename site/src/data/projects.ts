import { links } from '@data/links';

export const projects = {
  ru: [
    {
      slug: 'ai-assistant',
      title: 'Ai ассистент для личного пользования, на основе мессенджеров',
      year: '2025',
      role: 'Разработчик и продукт-менеджер',
      summary:
        'AI-ассистент для мессенджеров с различными инструментами: планирование задач, запись событий в Google Calendar, веб-поиск/парсинг, долговременная память через RAG (векторное хранилище, эмбеддинги, актуализация контекста).',
      description: [
        'Ассистент помогает вести ежедневные задачи прямо в мессенджере: создает туду-листы, разбивает большие задачи на шаги и напоминает о дедлайнах.',
        'Через интеграцию с Google Calendar бот может планировать встречи и автоматически добавлять события, а также подбирать свободные слоты.',
        'Для сложных запросов ассистент подключает инструменты веб-поиска и парсинга, а также RAG-пайплайн с долговременной памятью на основе векторного хранилища.'
      ],
      stack: ['Python', 'FastAPI', 'LangChain', 'Langgraph', 'Redis', 'Docker'],
      links: [
        { href: `${links.github}/Assistants`, label: 'Исходники' },
        { href: links.demos?.aiAssistant, label: 'Демо' }
      ]
    },
    {
      slug: 'dnd-helper',
      title: 'Справочник для игры DnD в мессенджерах',
      year: '2025',
      role: 'Разработчик',
      summary: 'Простенький справочник для ДнД 5e. Список монстров, заклинаний. Фильтры, пажинация, поиск.',
      description: [
        'Чат-бот позволяет быстро находить монстров и заклинания с помощью фильтров по уровню, школе магии и типу существа.',
        'Реализована постраничная выдача, чтобы комфортно работать в интерфейсе мессенджера без перегрузки информацией.',
        'Бот разворачивается в Docker и использует FastAPI + SQLAlchemy для предоставления API и хранения справочных данных.'
      ],
      stack: ['Python', 'FastAPI', 'SqlAlchemy', 'Docker'],
      links: [
        { href: `${links.github}/dnd_helper`, label: 'Исходники' },
        { href: links.demos?.dndHelper, label: 'Демо' }
      ]
    }
  ],
  en: [
    {
      slug: 'ai-assistant',
      title: 'AI assistant for personal use, based on messengers',
      year: '2025',
      role: 'Builder & product owner',
      summary:
        'AI assistant for messengers with various tools: task planning, event recording in Google Calendar, web search/parsing, long-term memory through RAG (vector store, embeddings, context updating).',
      description: [
        'The assistant keeps personal productivity in chat: it creates todo lists, breaks large goals into actionable steps, and follows up on deadlines.',
        'With Google Calendar integration the bot can schedule meetings, add new events automatically, and propose available slots.',
        'For research-heavy tasks the assistant triggers web search, scraping tools, and a RAG pipeline backed by a vector store for long-term memory.'
      ],
      stack: ['Python', 'FastAPI', 'LangChain', 'Langgraph', 'Redis', 'Docker'],
      links: [
        { href: `${links.github}/Assistants`, label: 'Source' },
        { href: links.demos?.aiAssistant, label: 'Demo' }
      ]
    },
    {
      slug: 'dnd-helper',
      title: 'DnD reference for messengers',
      year: '2025',
      role: 'Backend developer',
      summary: 'Simple DnD 5e reference. List of monsters and spells. Filters, pagination, search.',
      description: [
        'The chat-bot lets players look up monsters and spells with filters for level, school, and creature type to speed up tabletop sessions.',
        'I added cursor-based pagination so that answers stay compact in the messenger UI while still exposing full data.',
        'The service runs in Docker and exposes a FastAPI + SQLAlchemy backend that powers the bot and a public API.'
      ],
      stack: ['Python', 'FastAPI', 'SqlAlchemy', 'Docker'],
      links: [
        { href: `${links.github}/dnd_helper`, label: 'Source' },
        { href: links.demos?.dndHelper, label: 'Demo' }
      ]
    }
  ]
} as const;
