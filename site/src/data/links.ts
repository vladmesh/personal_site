export type Links = {
  email: string; // mailto
  emailPlain: string; // plain email string for display when needed
  telegram: string;
  github: string;
  githubRepo: string;
  linkedin: string;
  phone?: string; // tel:
  whatsapp?: string; // https://wa.me/
  cv: {
    en: string;
    ru: string;
  };
  domain: string; // site domain (https://...)
  analytics?: {
    plausible?: string; // script src
    domain?: string; // plausible data-domain
  };
  demos?: {
    aiAssistant?: string;
    dndHelper?: string;
  };
};

export const links: Links = {
  email: 'mailto:hi@vladmesh.dev',
  emailPlain: 'hi@vladmesh.dev',
  telegram: 'https://t.me/vladmesh',
  github: 'https://github.com/vladmesh',
  githubRepo: 'https://github.com/vladmesh/personal-site',
  linkedin: 'https://www.linkedin.com/in/vladmesh',
  phone: 'tel:+79000000000',
  whatsapp: 'https://wa.me/79000000000',
  cv: {
    en: '/cv/cv_en.pdf',
    ru: '/cv/cv_ru.pdf'
  },
  domain: 'https://vladmesh.dev',
  analytics: {
    plausible: 'https://plausible.io/js/script.js',
    domain: 'vladmesh.dev'
  },
  demos: {
    aiAssistant: 'https://t.me/virutual_helper_bot',
    dndHelper: 'https://t.me/dnd_helperbot'
  }
};


