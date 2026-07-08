export type HomeCopy = {
  hero: {
    eyebrow: string;
    greeting: string;
    subtitle: string;
    ctaPrimary: string;
    ctaSecondary: string;
    // Primary CTA target. Empty string => the button opens the contact modal.
    // Set to an anchor like "#offer" (see offerVisible) to repoint it without
    // touching the component.
    primaryHref: string;
    // Secondary CTA target (CV download).
    secondaryHref: string;
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
  // When the offer block is visible, point the hero primary CTA at it.
  offerVisible?: boolean;
};

const baseHomeCopy = {
  en: {
    hero: {
      eyebrow: "",
      greeting: "Your headline",
      subtitle: "A short subtitle about what you do",
      ctaPrimary: "Contact me",
      ctaSecondary: "Download CV",
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
      title: "Personal projects",
      ctaLabel: "All projects",
      ctaHref: "/en/projects",
    },
    skills: {
      title: "Skills",
      subtitle: "Core stack and tooling",
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
      subtitle: "Короткий подзаголовок о том, чем вы занимаетесь",
      ctaPrimary: "Написать мне",
      ctaSecondary: "Скачать CV",
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
      title: "Личные проекты",
      ctaLabel: "Все проекты",
      ctaHref: "/ru/projects",
    },
    skills: {
      title: "Навыки",
      subtitle: "Основные стек и инструменты",
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
  hero: Omit<HomeCopy["hero"], "primaryHref" | "secondaryHref">;
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
      primaryHref: overrides.offerVisible ? "#offer" : "",
      secondaryHref: overrides.resumeHref ?? siteConfig.cv[lang],
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
