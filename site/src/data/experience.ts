export type ExperienceItem = {
  company: string;
  title: string;
  description: string[];
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
type LocalizedStringArray = { en: string[]; ru: string[] };

type ExperienceGroup = {
  company: LocalizedString;
  title: LocalizedString;
  description: LocalizedStringArray;
  from?: LocalizedString;
  to?: LocalizedString;
  location?: LocalizedString;
};

export const experienceGroups: ExperienceGroup[] = [
  {
    company: { en: 'DNK IT Solutions', ru: 'DNK IT Solutions' },
    title: { en: 'Python Software Developer', ru: 'Python разработчик' },
    description: {
      en: [
        'Participated in the design and development of a platform that selects parameters and automates company registration in the UAE (uppersetup.com).',
        'Designed a microservices backend architecture in Python using FastAPI, SQLAlchemy, and Redis.',
        'Conducted load testing and unit testing.',
        'Developed and implemented a CI/CD pipeline for automated deployments.'
      ]
    ,
      ru: [
        'Участвовал в проектировании и разработке платформы, которая подбирает параметры и автоматизирует регистрацию компании в ОАЭ (uppersetup.com)',
        'Проектировал микросервисную архитектуру для бэкенда на python, с использованием FastAPI, SQLAlchemy, Redis',
        'Проводил нагрузочное и unit тестирование',
        'Разработал и внедрил CI/CD pipeline для автоматизации деплоя'
      ]
    },
    from: { en: '2022', ru: '2022' },
    to: { en: '2023', ru: '2023' },
    location: { en: 'Bishkek', ru: 'Бишкек' }
  },
  {
    company: { en: 'Yandex Practicum', ru: 'Яндекс Практикум' },
    title: { en: 'Backend Engineer', ru: 'Backend‑инженер' },
    description: {
      en: [
        'Contributed to backend development of a children’s math platform as part of a Scrum team',
        'Developed a Python monolith using Django REST Framework (DRF), Celery, Redis, and PostgreSQL',
        'Optimized for high load: database query tuning, indexing, sharding, etc.'
      ]
    ,
      ru: [
        'Участвовал в разработке бэкенда для платформы детской математики, в составе scrum-команды',
        'Разрабатывал монолитную архитектуру на python, с использованием DRF, Celery, Redis, PostgreSQL',
        'Занимался оптимазацией под высокие нагрузки. Отладка запросов к базе, индексы, шардирование и т.д'
      ]
    },
    from: { en: '2021', ru: '2021' },
    to: { en: '2022', ru: '2022' },
    location: { en: 'Saint Petersburg', ru: 'Санкт-Петербург' }
  },
  {
    company: { en: 'Piterauto', ru: 'Питеравто' },
    title: { en: 'Software Developer', ru: 'Разработчик ПО' },
    description: {
      en: [
        'Integrated CRMs, built end-to-end data pipelines (ETL), and set up business process automation',
        'Designed and launched from scratch a trip fiscalization system using Python, FastAPI, PostgreSQL, RabbitMQ, and Docker; later evolved into a standalone product — https://www.mega-fiscal.ru/'
      ]
    ,
      ru: [
        'Интегрировал CRM, строил сквозные пайплайны данных (ETL), настраивал автоматизацию бизнес процессов.',
        'Разработал с нуля и внедрил систему для фискализации поездок, с использованием Python, FastAPI, PostgreSQL, RabbitMQ, Docker. Позже этот проект вырос в отдельный продукт - https://www.mega-fiscal.ru/'
      ]
    },
    from: { en: '2018', ru: '2018' },
    to: { en: '2021', ru: '2021' },
    location: { en: 'Saint Petersburg', ru: 'Санкт-Петербург' }
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


