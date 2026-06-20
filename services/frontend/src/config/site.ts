import { SITE_URL } from "astro:env/server";

/**
 * Site configuration: deployment-level knobs (brand, domain, analytics, asset
 * paths). This is NOT editable content. Page content (hero, about, projects,
 * skills, testimonials, contacts, resumes) comes from the backend / admin.
 *
 * Replace the placeholder values below for your own deployment. `domain` is
 * driven by the SITE_URL env var so it can be set per environment without code
 * changes (see infra compose files).
 */

type Lang = "en" | "ru";

const origin = SITE_URL.replace(/\/+$/, "");

export const siteConfig = {
  /** Display name used in header, footer copyright, and meta titles. */
  brand: "Your Name",
  /** Full public origin, e.g. https://example.com. Drives OG tags and hreflang. */
  domain: origin,
  defaultLocale: "en" as Lang,
  /** Link to the source repository, shown in the footer when set. */
  sourceRepo: "",
  /** Fallback CV paths, used when the backend has no active resume for a locale. */
  cv: {
    en: "/cv/cv_en.pdf",
    ru: "/cv/cv_ru.pdf",
  } satisfies Record<Lang, string>,
  analytics: {
    /** Plausible script src. Leave empty to disable analytics. */
    plausibleSrc: "",
    /** data-domain for Plausible. Defaults to the site host. */
    domain: hostOf(origin),
  },
} as const;

function hostOf(url: string): string {
  try {
    return new URL(url).host;
  } catch {
    return url;
  }
}
