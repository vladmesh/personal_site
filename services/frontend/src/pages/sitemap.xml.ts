import type { APIRoute } from 'astro';
import { siteConfig } from '@config/site';
import { fetchProfile } from '@lib/profile/full';

const staticPaths = ['/', '/llm-systems/', '/projects/'];

/** /sitemap.xml: static pages plus every project case, in both locales. */
export const GET: APIRoute = async () => {
  const profile = await fetchProfile('en');
  const paths = [...staticPaths, ...profile.projects.map((project) => `/projects/${project.slug}/`)];
  const urls = paths.flatMap((path) =>
    (['en', 'ru'] as const).map((lang) => {
      const alternates = (['en', 'ru'] as const)
        .map((alt) => `    <xhtml:link rel="alternate" hreflang="${alt}" href="${siteConfig.domain}/${alt}${path}"/>`)
        .join('\n');
      return `  <url>\n    <loc>${siteConfig.domain}/${lang}${path}</loc>\n${alternates}\n  </url>`;
    })
  );
  const body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ...urls,
    '</urlset>',
    ''
  ].join('\n');
  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
  });
};
