import { fetchApi } from "@lib/api/client";
import { prettifyType } from "@lib/profile/contacts";
import type { ContactLink, ContactsResult } from "@lib/profile/contacts";
import type { HomeCopy } from "@data/home";

type Lang = "en" | "ru";

type ApiStack = {
  id: string;
  name: string;
  icon_url: string | null;
  category: string | null;
  proficiency: number | null;
};

type ApiWorkExperience = {
  id: string;
  company_name: string;
  company_url: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  position: string;
  description: string;
  location: string | null;
  stacks: ApiStack[];
};

type ApiProject = {
  id: string;
  slug: string;
  link: string | null;
  repo_link: string | null;
  start_date: string;
  end_date: string | null;
  is_featured: boolean;
  title: string;
  description: string;
  role: string | null;
  stacks: ApiStack[];
};

type ApiTestimonial = {
  id: string;
  author_name: string;
  author_url: string | null;
  author_avatar_url: string | null;
  kind: string | null;
  date: string;
  author_position: string | null;
  content: string;
};

type ApiContact = {
  id: string;
  type: string;
  value: string;
  icon: string | null;
  sort_order: number;
  label: string | null;
};

type ApiResume = {
  id: string;
  language_code: string;
  file_path: string;
  generated_at: string;
  is_active: boolean;
};

type ProfileFullResponse = {
  experience: ApiWorkExperience[];
  projects: ApiProject[];
  stacks: ApiStack[];
  testimonials: ApiTestimonial[];
  contacts: ApiContact[];
  resumes: ApiResume[];
};

export type FrontProject = {
  slug: string;
  title: string;
  year: string;
  role?: string;
  summary: string;
  description: string[];
  stack: string[];
  links: { href: string; label: string }[];
};

export type SkillGroup = {
  title: { en: string; ru: string };
  description: { en: string; ru: string };
  items: string[];
};

export type TestimonialEntry = {
  kind: "dev" | "teacher";
  quote: { en: string; ru: string };
  author: string;
  role?: string;
  url?: string;
};

export type ProfileData = {
  experience: HomeCopy["experience"];
  projects: FrontProject[];
  skills: SkillGroup[];
  testimonials: TestimonialEntry[];
  contacts: ContactsResult;
  resumes: Record<Lang, string | undefined>;
};

const CONTACT_SECTION_LABELS: Record<Lang, Record<string, string>> = {
  en: { demo: "Demo", source: "Source" },
  ru: { demo: "Демо", source: "Исходники" },
};

const SKILL_META: Record<
  string,
  { title: { en: string; ru: string }; description: { en: string; ru: string } }
> = {
  Backend: {
    title: { en: "Backend", ru: "Backend" },
    description: {
      en: "Designing resilient APIs and services ready to scale.",
      ru: "Проектирование API и сервисов, устойчивых к росту нагрузки.",
    },
  },
  "Data & AI": {
    title: { en: "Data & AI", ru: "Данные и AI" },
    description: { en: "Implement ML/LLM agents, pipelines, and MLOps practices.", ru: "Внедряю ML/LLM-агентов, пайплайны и MLOps." },
  },
  DevOps: {
    title: { en: "DevOps", ru: "DevOps" },
    description: { en: "Ship CI/CD, monitoring, and infrastructure automation.", ru: "Настраиваю CI/CD, мониторинг и инфраструктуру." },
  },
  Communication: {
    title: { en: "Communication", ru: "Коммуникации" },
    description: {
      en: "Align teams and processes to deliver measurable outcomes.",
      ru: "Организую процессы и помогаю командам доставлять результаты.",
    },
  },
  Other: {
    title: { en: "Other", ru: "Другое" },
    description: { en: "Additional tools and technologies.", ru: "Дополнительные инструменты и технологии." },
  },
};

export async function fetchProfile(lang: Lang): Promise<ProfileData> {
  const payload = await fetchApi<ProfileFullResponse>(`/api/v1/profile/full?lang=${lang}`);

  const contacts = buildContacts(payload.contacts);
  const resumeMap = buildResumeMap(payload.resumes);

  return {
    experience: buildExperienceSection(payload.experience, lang),
    projects: buildProjects(payload.projects, lang),
    skills: buildSkills(payload.stacks, lang),
    testimonials: buildTestimonials(payload.testimonials, lang),
    contacts,
    resumes: resumeMap,
  };
}

function buildExperienceSection(entries: ApiWorkExperience[], lang: Lang): HomeCopy["experience"] {
  const items = entries.map((entry) => ({
    company: entry.company_name,
    title: entry.position,
    description: splitLines(entry.description),
    from: formatYear(entry.start_date),
    to: entry.is_current ? (lang === "ru" ? "по наст. время" : "Present") : formatYear(entry.end_date),
    location: entry.location ?? undefined,
  }));

  return {
    title: lang === "ru" ? "Опыт работы" : "Experience",
    summary: lang === "ru" ? "Опыт работы" : "Experience",
    items,
  };
}

function buildProjects(entries: ApiProject[], lang: Lang): FrontProject[] {
  return entries.map((entry) => {
    const descriptionLines = splitLines(entry.description);
    const summary = descriptionLines[0] ?? "";

    const links = [
      entry.link ? { href: entry.link, label: CONTACT_SECTION_LABELS[lang].demo } : null,
      entry.repo_link ? { href: entry.repo_link, label: CONTACT_SECTION_LABELS[lang].source } : null,
    ].filter(Boolean) as { href: string; label: string }[];

    return {
      slug: entry.slug,
      title: entry.title,
      year: formatYear(entry.start_date),
      role: entry.role ?? undefined,
      summary,
      description: descriptionLines,
      stack: entry.stacks.map((s) => s.name),
      links,
    };
  });
}

function buildSkills(stacks: ApiStack[], lang: Lang): SkillGroup[] {
  const grouped = new Map<string, string[]>();
  stacks.forEach((stack) => {
    const category = stack.category || "Other";
    const arr = grouped.get(category) ?? [];
    arr.push(stack.name);
    grouped.set(category, arr);
  });

  const groups: SkillGroup[] = [];
  grouped.forEach((items, category) => {
    const meta = SKILL_META[category] ?? {
      title: { en: category, ru: category },
      description: { en: "", ru: "" },
    };
    groups.push({
      title: meta.title,
      description: meta.description,
      items: items.sort(),
    } as SkillGroup);
  });

  // Preserve predictable order using SKILL_META keys
  const order = Object.keys(SKILL_META);
  groups.sort((a, b) => order.indexOf(a.title.en) - order.indexOf(b.title.en));

  return groups;
}

function buildTestimonials(entries: ApiTestimonial[], lang: Lang): Testimonial[] {
  return entries.map((entry) => ({
    kind: entry.kind === "teacher" ? "teacher" : "dev",
    quote: { en: entry.content, ru: entry.content },
    author: entry.author_name,
    role: entry.author_position ?? undefined,
    url: entry.author_url ?? undefined,
  })) as TestimonialEntry[];
}

function buildContacts(contacts: ApiContact[]): ContactsResult {
  const items = contacts
    .map((contact) => {
      const href = buildHref(contact.type, contact.value);
      if (!href) return null;
      return {
        type: contact.type,
        label: contact.label ?? prettifyType(contact.type),
        href,
        icon: contact.icon,
        sortOrder: contact.sort_order ?? 0,
        isVisible: true,
        value: contact.value,
        display: formatDisplay(contact.type, contact.value, href),
      } as ContactLink;
    })
    .filter(Boolean)
    .sort((a, b) => (a?.sortOrder ?? 0) - (b?.sortOrder ?? 0)) as ContactLink[];

  return {
    items,
    lookup: items.reduce<Record<string, ContactLink>>((acc, item) => {
      acc[item.type] = item;
      return acc;
    }, {}),
  };
}

function buildResumeMap(resumes: ApiResume[]): Record<Lang, string | undefined> {
  const map: Record<Lang, string | undefined> = { en: undefined, ru: undefined };
  resumes.forEach((resume) => {
    const lang = resume.language_code as Lang;
    if (lang === "en" || lang === "ru") {
      map[lang] = resume.file_path;
    }
  });
  return map;
}

function splitLines(value: string): string[] {
  return value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

function formatYear(value: string | null): string {
  if (!value) return "";
  const year = new Date(value).getFullYear();
  return Number.isNaN(year) ? "" : String(year);
}

function buildHref(type: string, value: string): string | null {
  if (!value) return null;
  const trimmed = value.trim();
  if (!trimmed) return null;

  if (type === "email") {
    return trimmed.startsWith("mailto:") ? trimmed : `mailto:${trimmed}`;
  }
  if (type === "phone") {
    return trimmed.startsWith("tel:") ? trimmed : `tel:${trimmed}`;
  }
  return trimmed;
}

function formatDisplay(type: string, value: string, href: string): string {
  if (type === "email") return value;
  if (type === "phone") return value.replace(/^tel:/i, "");
  if (type === "telegram") {
    const handle = extractHandleFromHref(href);
    return handle ?? value;
  }
  return value;
}

function extractHandleFromHref(href: string): string | undefined {
  const match = href.match(/t\.me\/([^/?#]+)/i);
  if (match?.[1]) return `@${match[1]}`;
  if (href.startsWith("@")) return href;
  return undefined;
}
