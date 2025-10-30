import type { MiddlewareHandler } from 'astro';

const supported = ['ru', 'en'] as const;

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

  return next();
};
