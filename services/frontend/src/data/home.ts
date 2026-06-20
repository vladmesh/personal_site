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

import { siteConfig } from "@config/site";

export type ContactCopyInfo = {
  emailHref: string;
  emailText: string;
  telegramHref: string;
  telegramHandle: string;
  primaryContactHref?: string;
};

export type SiteContentCopy = {
  hero: { eyebrow: string; greeting: string; subtitle: string };
  about: { title: string; paragraphs: string[] };
};

type HomeOverrides = {
  experience?: HomeCopy["experience"];
  resumeHref?: string;
  siteContent?: SiteContentCopy | null;
};

const baseHomeCopy = {
  en: {
    hero: {
      eyebrow: "",
      greeting: "Your headline",
      subtitle: "A short subtitle about what you do.",
      ctaPrimary: "Download CV (EN)",
      ctaSecondary: "Contact me",
    },
    about: {
      title: "About",
      paragraphs: [],
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
      eyebrow: "",
      greeting: "Ваш заголовок",
      subtitle: "Короткий подзаголовок о том, чем вы занимаетесь.",
      ctaPrimary: "Скачать CV (RU)",
      ctaSecondary: "Написать мне",
    },
    about: {
      title: "Обо мне",
      paragraphs: [],
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
  const sc = overrides.siteContent;

  return {
    ...base,
    hero: {
      ...base.hero,
      eyebrow: sc?.hero.eyebrow ?? base.hero.eyebrow,
      greeting: sc?.hero.greeting ?? base.hero.greeting,
      subtitle: sc?.hero.subtitle ?? base.hero.subtitle,
      cvHref: overrides.resumeHref ?? siteConfig.cv[lang],
      contactHref: contactInfo.primaryContactHref ?? contactInfo.telegramHref,
    },
    about: sc?.about ?? base.about,
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
