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
    items: {
      company: string;
      title: string;
      description: string;
      from?: string;
      to?: string;
      location?: string;
    }[];
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
    tabs?: {
      dev: string;
      teacher: string;
    };
  };
  contact: {
    title: string;
    description: (
      | { type: 'text'; text: string }
      | { type: 'link'; text: string; href: string }
    )[];
  };
};

import { links } from '@data/links';
import { experience as experienceData } from '@data/experience';

export const homeCopy: Record<'en' | 'ru', HomeCopy> = {
  en: {
    hero: {
      eyebrow: 'Backend / AI',
      greeting: "Hi! I'm Vlad Mesh — backend & AI engineer.",
      subtitle: 'I help teams ship backend features faster and add AI agents to products.',
      ctaPrimary: 'Download CV (EN)',
      ctaSecondary: 'Get in touch',
      cvHref: links.cv.en,
      contactHref: links.email
    },
    about: {
      title: 'About',
      paragraphs: [
        "I'm a backend engineer and tech lead who helps teams launch resilient services and products powered by AI agents.",
        'I design architecture, assemble teams, and deliver production-ready solutions while balancing speed and code quality.'
      ]
    },
    experience: experienceData.en,
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
      title: 'Testimonials',
      tabs: {
        dev: 'Developer',
        teacher: 'Instructor'
      }
    },
    contact: {
      title: "Let's talk",
      description: [
        { type: 'text', text: 'Message me on Telegram ' },
        { type: 'link', text: '@vladmesh', href: links.telegram },
        { type: 'text', text: ' or send an email to ' },
        { type: 'link', text: links.emailPlain, href: links.email },
        { type: 'text', text: '.' }
      ]
    }
  },
  ru: {
    hero: {
      eyebrow: 'Разработка / Менторство',
      greeting: 'Привет! Я Влад — разработчик и ментор.',
      subtitle: 'Пишу бэкенды, настраиваю пайплайны, интегрирую LLM-агентов.',
      ctaPrimary: 'Скачать CV (RU)',
      ctaSecondary: 'Написать мне',
      cvHref: links.cv.ru,
      contactHref: links.telegram
    },
    about: {
      title: 'Обо мне',
      paragraphs: [
        'Шесть лет я занимаюсь тем, что пишу софт и учу других писать софт. Большей частью на Python. Иногда в составе большой команды, иногда самостоятельно под ключ. Чаще это бэкенд (DRF, FastAPI, SQLAlchemy), иногда боты, скрипты, парсеры и десктопные приложения. Последний год переключился на работу с AI-агентами. Чат-боты, RAG, MCP, агентские пайплайны. Больше всего люблю работать над проектами, которые хорошо согласуются с моими интересами и ценностями. Образование, AI-safety, открытые данные, mental health. На этом сайте можно увидеть примеры моих проектов и ознакомиться с моим опытом работы. А также почитать отзывы моих клиентов и учеников. Я открыт к предложениям, связаться со мной можно по контактам ниже (или выше)'
      ]
    },
    experience: experienceData.ru,
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
      title: 'Отзывы',
      tabs: {
        dev: 'Разработчик',
        teacher: 'Преподаватель'
      }
    },
    contact: {
      title: 'Свяжемся?',
      description: [
        { type: 'text', text: 'Пишите в Telegram ' },
        { type: 'link', text: '@vladmesh', href: links.telegram },
        { type: 'text', text: ' или на почту ' },
        { type: 'link', text: links.emailPlain, href: links.email },
        { type: 'text', text: '.' }
      ]
    }
  }
};
