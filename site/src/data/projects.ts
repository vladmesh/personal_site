import { links } from '@data/links';

export const projects = {
  ru: [
    {
      slug: 'ai-assistant',
      title: 'Ai ассистент для личного пользования, на основе мессенджеров',
      year: '2025',
      summary: 'AI-ассистент для мессенджеров с различными инструментами: планирование задач, запись событий в Google Calendar, \
      веб-поиск/парсинг, долговременная память через RAG (векторное хранилище, эмбеддинги, актуализация контекста).',
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
      summary: 'Простенький справочник для ДнД 5e. Список монстров, заклинаний. Фильтры, пажинация, поиск.',
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
      summary: 'AI assistant for messengers with various tools: task planning, event recording in Google Calendar, \
      web search/parsing, long-term memory through RAG (vector store, embeddings, context updating).',
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
      summary: 'Simple DnD 5e reference. List of monsters and spells. Filters, pagination, search.',
      stack: ['Python', 'FastAPI', 'SqlAlchemy', 'Docker'],
      links: [
        { href: `${links.github}/dnd_helper`, label: 'Source' },
        { href: links.demos?.dndHelper, label: 'Demo' }
      ]
    }
  ]
} as const;
