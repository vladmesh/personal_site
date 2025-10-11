export type ExperienceItem = {
  company: string;
  title: string;
  description: string;
  from?: string;
  to?: string;
  location?: string;
};

export type ExperienceSection = {
  title: string;
  summary: string;
  items: ExperienceItem[];
};

type LocalizedString = { en: string; ru: string };

type ExperienceGroup = {
  company: LocalizedString;
  title: LocalizedString;
  description: LocalizedString;
  from?: LocalizedString;
  to?: LocalizedString;
  location?: LocalizedString;
};

export const experienceGroups: ExperienceGroup[] = [
  {
    company: { en: 'Customer support product team', ru: 'Продуктовая команда поддержки' },
    title: { en: 'Tech Lead', ru: 'Техлид' },
    description: {
      en: 'Built an AI agent platform, orchestrated the roadmap, and integrated with Helpdesk/CRM.',
      ru: 'Собрал платформу AI-агентов, организовал поток задач и интеграции с Helpdesk/CRM.'
    },
    from: { en: '2024', ru: '2024' },
    to: { en: 'Present', ru: 'Сейчас' },
    location: { en: 'Remote', ru: 'Удалённо' }
  },
  {
    company: { en: 'Retail', ru: 'Ритейл' },
    title: { en: 'Backend Engineer', ru: 'Backend‑инженер' },
    description: {
      en: 'Launched a Go-based dynamic pricing service that reduced promo rollout from 2 days to 4 hours.',
      ru: 'Запустил сервис динамического ценообразования на Go, сократил вывод акций с 2 дней до 4 часов.'
    },
    from: { en: '2022', ru: '2022' },
    to: { en: '2023', ru: '2023' },
    location: { en: 'Moscow', ru: 'Москва' }
  },
  {
    company: { en: 'Startups', ru: 'Стартапы' },
    title: { en: 'AI Solutions Consultant', ru: 'Консультант по AI‑решениям' },
    description: {
      en: 'Help startups validate ideas fast, plug in LLMs, and establish delivery and operations processes.',
      ru: 'Помогаю быстро проверять гипотезы, подключать LLM и строить процессы эксплуатации.'
    },
    from: { en: '2021', ru: '2021' },
    to: { en: '2022', ru: '2022' },
    location: { en: 'Remote', ru: 'Удалённо' }
  }
];

export const experience: Record<'en' | 'ru', ExperienceSection> = {
  en: {
    title: 'Experience',
    summary: 'Experience',
    items: experienceGroups.map((g) => ({
      company: g.company.en,
      title: g.title.en,
      description: g.description.en,
      from: g.from?.en,
      to: g.to?.en,
      location: g.location?.en
    }))
  },
  ru: {
    title: 'Опыт работы',
    summary: 'Опыт работы',
    items: experienceGroups.map((g) => ({
      company: g.company.ru,
      title: g.title.ru,
      description: g.description.ru,
      from: g.from?.ru,
      to: g.to?.ru,
      location: g.location?.ru
    }))
  }
};


