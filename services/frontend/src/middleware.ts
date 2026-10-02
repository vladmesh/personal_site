import type { MiddlewareHandler } from 'astro';
import { projectSlugRedirects } from '@config/redirects';

const supported = ['ru', 'en'] as const;

const projectPath = /^\/(ru|en)\/projects\/([^/]+)\/?$/;

export const onRequest: MiddlewareHandler = async ({ url, redirect }, next) => {
  // Allow static CV files to bypass locale redirects
  if (url.pathname.startsWith('/cv/')) {
    return next();
  }

  if (url.pathname === '/' || url.pathname === '') {
    return redirect('/en/', 302);
  }

  const [, maybeLocale] = url.pathname.split('/');
  if (maybeLocale && !supported.includes(maybeLocale as (typeof supported)[number])) {
    return redirect('/en/', 302);
  }

  const projectMatch = projectPath.exec(url.pathname);
  if (projectMatch) {
    const [, locale, slug] = projectMatch;
    const target = Object.hasOwn(projectSlugRedirects, slug) ? projectSlugRedirects[slug] : undefined;
    if (target) {
      return redirect(`/${locale}/projects/${target}/`, 301);
    }
  }

  return next();
};
