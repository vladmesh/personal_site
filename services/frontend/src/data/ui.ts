export type UICopy = {
  header: {
    brand: string;
    nav: {
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
    header: {
      brand: 'Vladislav Meshkorudnyj',
      nav: {
        projects: 'Projects',
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
      metaTitle: 'Projects — Vladislav Meshkorudnyj',
      metaDescription: 'Portfolio of backend and AI projects shipped by Vladislav Meshkorudnyj.',
      eyebrow: 'Portfolio',
      title: 'Selected projects',
      intro: 'Case studies of backend, platform, and AI work. Each project includes metrics and stack details.'
    }
  },
  ru: {
    header: {
      brand: 'Vladislav Meshkorudnyj',
      nav: {
        projects: 'Проекты',
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
      metaTitle: 'Проекты — Владислав Мешкорудный',
      metaDescription: 'Портфолио backend и AI проектов.',
      eyebrow: 'Портфолио',
      title: 'Ключевые проекты',
      intro: 'Кейсы по backend-разработке, платформенным решениям и AI-агентам. Каждый проект — с цифрами и стеком.'
    }
  }
};


