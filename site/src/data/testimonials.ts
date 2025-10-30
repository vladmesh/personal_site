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
      ru: 'Я настоятельно рекомендую Владислава за его выдающуюся работу по созданию Telegram-бота для нашего проекта в сфере криптовалют. \
      На протяжении всего проекта он демонстрировал высокий уровень экспертизы, профессионализма и внимания к деталям. \
      Его глубокое понимание Python, Telegram API, а также криптовалютных бирж и их API было критически важным для создания надёжного бота, \
      который предоставлял нашим пользователям оповещения в режиме реального времени. Коммуникация и обновления с его стороны были оперативными и регулярными, \
      а результаты стабильно превосходили наши ожидания. Рекомендую Владислава для любых проектов, где требуется экспертиза в разработке Telegram-ботов или веб-парсеров.'
,
      en: 'I highly recommend Vladislav for his exceptional work in creating a Telegram bot for our cryptocurrency project. He demonstrated a high level of expertise, professionalism, and attention to detail throughout the project. \
      His deep understanding of Python, the Telegram API, and cryptocurrency exchanges and APIs was critical in creating a reliable bot that provided our users with real-time alerts. \
      His communication and updates were prompt and frequent, and he consistently exceeded our expectations. I highly recommend Vladislav for any project that requires expertise in developing Telegram bots or web parsers.'
    },
    author: 'Nikita Nikitin',
    url: 'https://www.upwork.com/freelancers/~01b6b1e325874479ec'
  },
  {
    kind: 'teacher',
    quote: {
      ru: 'Профессионал своего дела, может разобраться с любой задачей для программирования. Объясняет четко и понятно, умеет слушать. Берется за любые сложности.',
      en: 'A consummate professional who can handle any programming task. He explains things clearly and is a great listener. Willing to take on challenges of any complexity.'
    },
    author: 'Dmitriy',
    url: 'https://profi.ru/profile/MeshkorudnyyVD/#reviews-tab'
  },
  {
    kind: 'teacher',
    quote: {
      ru: 'помог разобраться с такими технологиями, как FastAPI, docker, redis, postgres. отвечал на вопросы в переписке. одному разбираться было некомфортно из-за обилия информации, в этом плане Влад очень помог.',
      en: 'Vlad helped me get to grips with FastAPI, Docker, Redis, and Postgres, and he answered my questions over chat. Trying to figure it all out alone felt overwhelming due to the amount of information; Vlad’s support made a huge difference.'
    },
    author: 'Michael',
    url: 'https://profi.ru/profile/MeshkorudnyyVD/#reviews-tab'
  }
];
