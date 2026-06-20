import { siteConfig } from '@config/site';

export type UICopy = {
  home: {
    metaTitle: string;
    metaDescription: string;
  };
  header: {
    brand: string;
    nav: {
      offer: string;
      projects: string;
      skills: string;
      testimonials: string;
      contact: string;
    };
  };
  footer: {
    rights: string;
    sourceLabel: string;
    social: {
      github: string;
      linkedin: string;
      telegram: string;
    };
  };
  projectCard: {
    detailsLabel: string;
  };
  projectsPage: {
    metaTitle: string;
    metaDescription: string;
    eyebrow: string;
    title: string;
    intro: string;
  };
};

export const uiCopy: Record<'en' | 'ru', UICopy> = {
  en: {
    home: {
      metaTitle: `${siteConfig.brand} — Portfolio`,
      metaDescription: 'Backend engineering, AI agents, and selected projects.'
    },
    header: {
      brand: siteConfig.brand,
      nav: {
        offer: 'Offer',
        projects: 'Work',
        skills: 'Skills',
        testimonials: 'Testimonials',
        contact: 'Contact'
      }
    },
    footer: {
      rights: 'All rights reserved.',
      sourceLabel: 'Source code',
      social: {
        github: 'GitHub',
        linkedin: 'LinkedIn',
        telegram: 'Telegram'
      }
    },
    projectCard: {
      detailsLabel: 'View case'
    },
    projectsPage: {
      metaTitle: `Projects — ${siteConfig.brand}`,
      metaDescription: 'Selected backend, platform, and AI case studies.',
      eyebrow: 'Portfolio',
      title: 'Selected projects',
      intro: 'Case studies of backend, platform, and AI work. Each project includes metrics and stack details.'
    }
  },
  ru: {
    home: {
      metaTitle: `${siteConfig.brand} — Портфолио`,
      metaDescription: 'Backend-разработка, AI-агенты и избранные проекты.'
    },
    header: {
      brand: siteConfig.brand,
      nav: {
        offer: 'Оффер',
        projects: 'Работы',
        skills: 'Навыки',
        testimonials: 'Отзывы',
        contact: 'Контакты'
      }
    },
    footer: {
      rights: 'Все права защищены.',
      sourceLabel: 'Исходники сайта',
      social: {
        github: 'GitHub',
        linkedin: 'LinkedIn',
        telegram: 'Telegram'
      }
    },
    projectCard: {
      detailsLabel: 'Подробнее'
    },
    projectsPage: {
      metaTitle: `Проекты — ${siteConfig.brand}`,
      metaDescription: 'Портфолио backend и AI проектов.',
      eyebrow: 'Портфолио',
      title: 'Ключевые проекты',
      intro: 'Кейсы по backend-разработке, платформенным решениям и AI-агентам. Каждый проект — с цифрами и стеком.'
    }
  }
};


