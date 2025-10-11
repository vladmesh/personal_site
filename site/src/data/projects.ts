import { links } from '@data/links';

export const projects = {
  ru: [
    {
      slug: 'agent-platform',
      title: 'Платформа AI-агентов для поддержки',
      role: 'Техлид · Python, FastAPI, LangChain',
      year: '2024',
      summary: 'Организовал разработку платформы для поддержки клиентов на основе AI-агентов с интеграцией в Helpdesk и CRM.',
      stack: ['Python', 'FastAPI', 'LangChain', 'Redis', 'Docker'],
      links: [
        { href: `${links.github}/agent-platform`, label: { ru: 'Исходники', en: 'Source' } },
        { href: links.demos?.agentPlatform || 'https://demo.vladmesh.dev', label: { ru: 'Демо', en: 'Demo' } }
      ]
    },
    {
      slug: 'pricing-service',
      title: 'Сервис динамического ценообразования',
      role: 'Backend-инженер · Go, PostgreSQL',
      year: '2023',
      summary: 'Построил сервис прогнозирования цен с ML-моделями, сократил время вывода новой акции с 2 дней до 4 часов.',
      stack: ['Go', 'PostgreSQL', 'Redis', 'Kafka'],
      links: [
        { href: `${links.github}/pricing-service`, label: { ru: 'Исходники', en: 'Source' } }
      ]
    }
  ],
  en: [
    {
      slug: 'agent-platform',
      title: 'AI Support Agent Platform',
      role: 'Tech Lead · Python, FastAPI, LangChain',
      year: '2024',
      summary: 'Led the build of AI agent platform for customer support with Helpdesk and CRM integrations.',
      stack: ['Python', 'FastAPI', 'LangChain', 'Redis', 'Docker'],
      links: [
        { href: `${links.github}/agent-platform`, label: { ru: 'Исходники', en: 'Source' } },
        { href: links.demos?.agentPlatform || 'https://demo.vladmesh.dev', label: { ru: 'Демо', en: 'Demo' } }
      ]
    },
    {
      slug: 'pricing-service',
      title: 'Dynamic Pricing Service',
      role: 'Backend Engineer · Go, PostgreSQL',
      year: '2023',
      summary: 'Delivered ML-driven pricing service reducing new campaign time-to-market from 2 days to 4 hours.',
      stack: ['Go', 'PostgreSQL', 'Redis', 'Kafka'],
      links: [
        { href: `${links.github}/pricing-service`, label: { ru: 'Исходники', en: 'Source' } }
      ]
    }
  ]
} as const;
