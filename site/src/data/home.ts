export type HomeCopy = {
  hero: {
    eyebrow: string;
    greeting: string;
    subtitle: string;
    ctaPrimary: string;
    ctaSecondary: string;
    cvHref: string;
    contactHref: string;
  };
  about: {
    title: string;
    paragraphs: string[];
  };
  experience: {
    title: string;
    summary: string;
    items: string[];
  };
  projects: {
    title: string;
    ctaLabel: string;
    ctaHref: string;
  };
  skills: {
    title: string;
    subtitle: string;
  };
  testimonials: {
    title: string;
  };
  contact: {
    title: string;
    description: (
      | { type: 'text'; text: string }
      | { type: 'link'; text: string; href: string }
    )[];
  };
};

export const homeCopy: Record<'en' | 'ru', HomeCopy> = {
  en: {
    hero: {
      eyebrow: 'Backend / AI',
      greeting: "Hi! I'm Vlad Mesh — backend & AI engineer.",
      subtitle: 'I help teams ship backend features faster and add AI agents to products.',
      ctaPrimary: 'Download CV (EN)',
      ctaSecondary: 'Get in touch',
      cvHref: '/cv/cv_en.pdf',
      contactHref: 'mailto:hi@vladmesh.dev'
    },
    about: {
      title: 'About',
      paragraphs: [
        "I'm a backend engineer and tech lead who helps teams launch resilient services and products powered by AI agents.",
        'I design architecture, assemble teams, and deliver production-ready solutions while balancing speed and code quality.'
      ]
    },
    experience: {
      title: 'Experience',
      summary: 'Experience',
      items: [
        'Tech lead for a customer support product team: built an AI agent platform, orchestrated the roadmap, and integrated with Helpdesk/CRM.',
        'Backend engineer in retail: launched a Go-based dynamic pricing service that reduced promo rollout from 2 days to 4 hours.',
        'AI solutions consultant: help startups validate ideas fast, plug in LLMs, and establish delivery and operations processes.'
      ]
    },
    projects: {
      title: 'Projects',
      ctaLabel: 'All projects',
      ctaHref: '/en/projects'
    },
    skills: {
      title: 'Skills',
      subtitle: 'Core stack and tooling.'
    },
    testimonials: {
      title: 'Testimonials'
    },
    contact: {
      title: "Let's talk",
      description: [
        { type: 'text', text: 'Message me on Telegram ' },
        { type: 'link', text: '@vladmesh', href: 'https://t.me/vladmesh' },
        { type: 'text', text: ' or send an email to ' },
        { type: 'link', text: 'hi@vladmesh.dev', href: 'mailto:hi@vladmesh.dev' },
        { type: 'text', text: '.' }
      ]
    }
  },
  ru: {
    hero: {
      eyebrow: 'Backend / AI',
      greeting: 'Привет! Я Влад Меш — backend и AI-инженер.',
      subtitle: 'Помогаю компаниям ускорять разработку и интегрировать AI-агентов.',
      ctaPrimary: 'Скачать CV (RU)',
      ctaSecondary: 'Написать мне',
      cvHref: '/cv/cv_ru.pdf',
      contactHref: 'https://t.me/vladmesh'
    },
    about: {
      title: 'Обо мне',
      paragraphs: [
        'Я backend-инженер и техлид, который помогает командам выводить на рынок устойчивые сервисы и продукты с AI-агентами.',
        'Проектирую архитектуру, собираю команды и довожу решения до продакшена, держу в фокусе как скорость поставки, так и качество кода.'
      ]
    },
    experience: {
      title: 'Опыт работы',
      summary: 'Опыт работы',
      items: [
        'Техлид в продуктовой команде поддержки: собрал платформу AI-агентов, организовал поток задач и интеграции с Helpdesk/CRM.',
        'Backend-инженер в ретейле: запустил сервис динамического ценообразования на Go, сократил вывод акций с 2 дней до 4 часов.',
        'Консультант по AI-решениям: помогаю стартапам быстро проверять гипотезы, подключать LLM и строить процессы эксплуатации.'
      ]
    },
    projects: {
      title: 'Проекты',
      ctaLabel: 'Все проекты',
      ctaHref: '/ru/projects'
    },
    skills: {
      title: 'Навыки',
      subtitle: 'Основные стек и инструменты.'
    },
    testimonials: {
      title: 'Отзывы'
    },
    contact: {
      title: 'Свяжемся?',
      description: [
        { type: 'text', text: 'Пишите в Telegram ' },
        { type: 'link', text: '@vladmesh', href: 'https://t.me/vladmesh' },
        { type: 'text', text: ' или на почту ' },
        { type: 'link', text: 'hi@vladmesh.dev', href: 'mailto:hi@vladmesh.dev' },
        { type: 'text', text: '.' }
      ]
    }
  }
};
