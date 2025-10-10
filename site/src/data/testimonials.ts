export type Testimonial = {
  kind: 'dev' | 'teacher';
  quote: { ru: string; en: string };
  author: string;
  role?: string;
  url?: string;
};

export const testimonials: Testimonial[] = [
  {
    kind: 'dev',
    quote: {
      ru: 'Влад выстроил процесс релизов и внедрил AI-агентов, благодаря чему служба поддержки сократила время ответа на 35%.',
      en: 'Vlad rebuilt our release process and introduced AI agents which cut support response times by 35%.'
    },
    author: 'Анна Иванова',
    role: 'Head of Customer Success, SaaS Inc.',
    url: 'https://example.com/reference-1'
  },
  {
    kind: 'teacher',
    quote: {
      ru: 'Он быстро погружается в домен и приносит измеримый результат. Команда довольна сотрудничеством.',
      en: 'He ramps up fast and delivers measurable outcomes. The team loved collaborating with him.'
    },
    author: 'Michael Chen',
    role: 'CTO, Fintech Startup',
    url: 'https://example.com/reference-2'
  }
];
