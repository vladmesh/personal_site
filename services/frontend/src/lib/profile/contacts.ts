import { ApiError, fetchApi } from "@lib/api/client";

const CONTACTS_ENDPOINT = "/api/v1/profile/contacts";

export type ContactTranslationApiModel = {
  language_code: string;
  label: string | null;
};

export type ContactApiModel = {
  id: string;
  type: string;
  value: string;
  icon: string | null;
  is_visible: boolean;
  sort_order: number;
  translations: ContactTranslationApiModel[];
};

export type ContactLink = {
  type: string;
  label: string;
  href: string;
  icon: string | null;
  sortOrder: number;
  isVisible: boolean;
  value: string;
  display: string;
};

export type ContactsResult = {
  items: ContactLink[];
  lookup: Record<string, ContactLink>;
};

export async function fetchContacts(lang: "en" | "ru"): Promise<ContactsResult> {
  const payload = await fetchApi<ContactApiModel[]>(CONTACTS_ENDPOINT);
  const items = normalizeContacts(payload, lang);

  if (!items.length) {
    throw new ApiError("No contacts returned from API", 502, payload);
  }

  return {
    items,
    lookup: toLookup(items),
  };
}

export function selectContact(
  contacts: ContactsResult,
  preferredTypes: string[],
): ContactLink | undefined {
  for (const type of preferredTypes) {
    const candidate = contacts.lookup[type];
    if (candidate) return candidate;
  }
  return undefined;
}

export function getTelegramHandle(contact?: ContactLink): string | undefined {
  if (!contact) return undefined;
  return formatDisplay(contact.type, contact.value, contact.href);
}

function normalizeContacts(payload: ContactApiModel[], lang: "en" | "ru"): ContactLink[] {
  return payload
    .filter((contact) => contact.is_visible)
    .map((contact) => normalizeContact(contact, lang))
    .filter(Boolean)
    .sort((a, b) => (a?.sortOrder ?? 0) - (b?.sortOrder ?? 0)) as ContactLink[];
}

function normalizeContact(contact: ContactApiModel, lang: "en" | "ru"): ContactLink | null {
  const href = buildHref(contact.type, contact.value);
  if (!href) return null;

  return {
    type: contact.type,
    label: pickLabel(contact.translations, lang) ?? prettifyType(contact.type),
    href,
    icon: contact.icon,
    sortOrder: contact.sort_order ?? 0,
    isVisible: contact.is_visible,
    value: contact.value,
    display: formatDisplay(contact.type, contact.value, href),
  };
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

function pickLabel(
  translations: ContactTranslationApiModel[],
  lang: "en" | "ru",
): string | undefined {
  const exact = translations.find((t) => t.language_code === lang)?.label;
  if (exact) return exact;
  const en = translations.find((t) => t.language_code === "en")?.label;
  if (en) return en;
  return translations[0]?.label ?? undefined;
}

export function prettifyType(type: string): string {
  return type
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase())
    .trim();
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

function toLookup(items: ContactLink[]): Record<string, ContactLink> {
  return items.reduce<Record<string, ContactLink>>((acc, item) => {
    acc[item.type] = item;
    return acc;
  }, {});
}
