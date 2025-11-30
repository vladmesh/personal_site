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

// TODO: Migrating to backend API - these links are now served from /api/v1/profile/contacts
// Some fields (cv, domain, analytics, demos) are not yet migrated to backend
export const links: Links = {
  email: 'mailto:hi@vladmesh.dev@gmail.com',
  emailPlain: 'vladmesh.dev@gmail.com',
  telegram: 'https://t.me/vladislav_meshk',
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

/*
// MIGRATED TO BACKEND: Contact links now available at /api/v1/profile/contacts
// API returns:
// - email: vladmesh.dev@gmail.com
// - telegram: https://t.me/vladislav_meshk
// - github: https://github.com/vladmesh
// - github_repo: https://github.com/vladmesh/personal-site
// - linkedin: https://www.linkedin.com/in/vladmesh
// - phone: +79000000000 (hidden)
// - whatsapp: https://wa.me/79000000000 (hidden)
//
// Each contact includes translations for 'en' and 'ru' with labels
*/


