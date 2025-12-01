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
      description: string[];
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
      | { type: "text"; text: string }
      | { type: "link"; text: string; href: string }
    )[];
  };
};

import { links } from "@data/links";

export type ContactCopyInfo = {
  emailHref: string;
  emailText: string;
  telegramHref: string;
  telegramHandle: string;
  primaryContactHref?: string;
};

type HomeOverrides = {
  experience?: HomeCopy["experience"];
  resumeHref?: string;
};

const baseHomeCopy = {
  en: {
    hero: {
      eyebrow: "Development / Mentorship",
      greeting: "Hi! I'm Vlad — a developer and mentor.",
      subtitle: "I build backends, set up pipelines, and integrate LLM agents.",
      ctaPrimary: "Download CV (EN)",
      ctaSecondary: "Contact me",
    },
    about: {
      title: "About me",
      paragraphs: [
        "For six years I've been writing software and teaching others to write it — mostly in Python. Sometimes as part of a large team, sometimes solo end-to-end. More often it's backend (DRF, FastAPI, SQLAlchemy), sometimes bots, scripts, scrapers, and desktop apps. Over the last year I’ve shifted to AI agents: chatbots, RAG, MCP, and agentic pipelines. I enjoy projects that align with my interests and values: education, AI safety, open data, and mental health. Here you can browse examples of my projects and my work experience, as well as read feedback from clients and students. I’m open to opportunities — feel free to reach out via the contacts below (or above).",
      ],
    },
    experience: {
      title: "Experience",
      summary: "Experience",
      items: [],
    },
    projects: {
      title: "Projects",
      ctaLabel: "All projects",
      ctaHref: "/en/projects",
    },
    skills: {
      title: "Skills",
      subtitle: "Core stack and tooling.",
    },
    testimonials: {
      title: "Testimonials",
      tabs: {
        dev: "Developer",
        teacher: "Mentor",
      },
    },
    contact: {
      title: "Let's talk",
    },
  },
  ru: {
    hero: {
      eyebrow: "Разработка / Менторство",
      greeting: "Привет! Я Влад — разработчик и ментор.",
      subtitle: "Пишу бэкенды, настраиваю пайплайны, интегрирую LLM-агентов.",
      ctaPrimary: "Скачать CV (RU)",
      ctaSecondary: "Написать мне",
    },
    about: {
      title: "Обо мне",
      paragraphs: [
        "Шесть лет я занимаюсь тем, что пишу софт и учу других писать софт. Большей частью на Python. Иногда в составе большой команды, иногда самостоятельно под ключ. Чаще это бэкенд (DRF, FastAPI, SQLAlchemy), иногда боты, скрипты, парсеры и десктопные приложения. Последний год переключился на работу с AI-агентами. Чат-боты, RAG, MCP, агентские пайплайны. Больше всего люблю работать над проектами, которые хорошо согласуются с моими интересами и ценностями. Образование, AI-safety, открытые данные, mental health. На этом сайте можно увидеть примеры моих проектов и ознакомиться с моим опытом работы. А также почитать отзывы моих клиентов и учеников. Я открыт к предложениям, связаться со мной можно по контактам ниже (или выше)",
      ],
    },
    experience: {
      title: "Опыт работы",
      summary: "Опыт работы",
      items: [],
    },
    projects: {
      title: "Проекты",
      ctaLabel: "Все проекты",
      ctaHref: "/ru/projects",
    },
    skills: {
      title: "Навыки",
      subtitle: "Основные стек и инструменты.",
    },
    testimonials: {
      title: "Отзывы",
      tabs: {
        dev: "Разработчик",
        teacher: "Преподаватель",
      },
    },
    contact: {
      title: "Свяжемся?",
    },
  },
} as const satisfies Record<"en" | "ru", Omit<HomeCopy, "hero" | "contact"> & {
  hero: Omit<HomeCopy["hero"], "cvHref" | "contactHref">;
  contact: Omit<HomeCopy["contact"], "description">;
}>;

export function buildHomeCopy(
  lang: "en" | "ru",
  contactInfo: ContactCopyInfo,
  overrides: HomeOverrides = {},
): HomeCopy {
  const base = baseHomeCopy[lang];

  return {
    ...base,
    hero: {
      ...base.hero,
      cvHref: overrides.resumeHref ?? links.cv[lang],
      contactHref: contactInfo.primaryContactHref ?? contactInfo.telegramHref,
    },
    contact: {
      ...base.contact,
      description: buildContactDescription(lang, contactInfo),
    },
    experience: overrides.experience ?? base.experience,
  };
}

function buildContactDescription(
  lang: "en" | "ru",
  info: ContactCopyInfo,
): HomeCopy["contact"]["description"] {
  const descriptions = {
    en: [
      { type: "text" as const, text: "Message me on Telegram " },
      { type: "link" as const, text: info.telegramHandle, href: info.telegramHref },
      { type: "text" as const, text: " or send an email to " },
      { type: "link" as const, text: info.emailText, href: info.emailHref },
      { type: "text" as const, text: "." },
    ],
    ru: [
      { type: "text" as const, text: "Пишите в Telegram " },
      { type: "link" as const, text: info.telegramHandle, href: info.telegramHref },
      { type: "text" as const, text: " или на почту " },
      { type: "link" as const, text: info.emailText, href: info.emailHref },
      { type: "text" as const, text: "." },
    ],
  };

  return descriptions[lang];
}
