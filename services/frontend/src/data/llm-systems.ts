/**
 * Copy for the /{lang}/llm-systems service page and /llms.txt.
 * Prices and scope live here, not in the admin, so the page and llms.txt stay in sync.
 */

type Lang = 'en' | 'ru';

export type ServicePackage = {
  id: string;
  name: string;
  summary: string;
  includes: string[];
  timeline: string;
  price: string;
  /** Lowest price in EUR, for JSON-LD. */
  priceEur: number;
};

export type ServiceCase = {
  title: string;
  text: string;
  href?: string;
};

export type LlmSystemsCopy = {
  metaTitle: string;
  metaDescription: string;
  eyebrow: string;
  title: string;
  intro: string[];
  packagesTitle: string;
  timelineLabel: string;
  priceLabel: string;
  packages: ServicePackage[];
  hourly: string;
  casesTitle: string;
  cases: ServiceCase[];
  contactTitle: string;
  contactText: string;
  emailLabel: string;
  telegramLabel: string;
};

/** Profiles not in the contacts API, added to JSON-LD sameAs. */
export const personSameAs = ['https://www.lesswrong.com/users/vladmesh'];

const inspectTutorials = 'https://www.lesswrong.com/posts/EvGLAuEtHpicKGBJh/hands-on-tutorials-for-inspect-ai-1';

const inspectPrs = 'https://github.com/UKGovernmentBEIS/inspect_ai/pulls?q=is%3Apr+author%3Avladmesh+is%3Amerged';

export const llmSystemsCopy: Record<Lang, LlmSystemsCopy> = {
  en: {
    metaTitle:
      'AI agent developer for hire: turnkey Telegram bot with LLM, LLM evaluation consultant, multi-agent orchestration',
    metaDescription:
      'Vladislav Meshkorudnyi builds LLM chatbots and agents and sets up the evals that show whether they work. Fixed-price packages from €1,500. Remote, EU time zone.',
    eyebrow: 'LLM systems',
    title: 'LLM systems end to end: chatbots, agents, evals',
    intro: [
      'I am an AI agent developer for hire. I build LLM chatbots and agents and set up the evals that show whether they work. Part-time, fixed price, remote from Cyprus (EU time zone).',
      'Typical requests: a turnkey Telegram bot with LLM, multi-agent orchestration for an internal workflow, or an LLM evaluation consultant for a product that is already live. Each package below has a fixed scope and price.'
    ],
    packagesTitle: 'Packages',
    timelineLabel: 'Timeline',
    priceLabel: 'Price',
    packages: [
      {
        id: 'audit',
        name: 'LLM product audit',
        summary: 'Find out where your chatbot or agent fails and what to fix first.',
        includes: [
          'Review of architecture, prompts and traces',
          'Baseline eval on 50 of your real cases',
          'Failures grouped by type',
          'Fixes ranked by expected effect',
          '45-minute call with the results'
        ],
        timeline: '1 week',
        price: '€1,500, counts toward the next package',
        priceEur: 1500
      },
      {
        id: 'eval-harness',
        name: 'Eval harness',
        summary: 'A test suite for your LLM product that runs on every change.',
        includes: [
          'Golden set of 100 to 200 cases',
          'Deterministic checks plus an LLM judge calibrated on human labels (Inspect AI or promptfoo)',
          'Regression gate in your CI',
          'Written report',
          'The harness stays with you'
        ],
        timeline: '2 to 3 weeks',
        price: '€3,500',
        priceEur: 3500
      },
      {
        id: 'agent-system',
        name: 'Agent system or orchestrator',
        summary: 'One agent or several agents that do real work with tools, built in milestones.',
        includes: [
          'Tools, memory, a task queue and acceptance checks',
          'Retries, rate and quota limits',
          'Evals on the agent trajectory as well as the final answer',
          'About 50 hours per milestone'
        ],
        timeline: '4 to 6 weeks per milestone',
        price: 'from €5,000 per milestone',
        priceEur: 5000
      },
      {
        id: 'chatbot',
        name: 'Telegram or web chatbot with LLM',
        summary: 'A turnkey bot that answers from your data.',
        includes: [
          'Dialog flows for your use case',
          'RAG over your documents or database',
          'Admin view and logs',
          'Smoke test set from day one',
          'Deployment to your server'
        ],
        timeline: '2 to 3 weeks',
        price: 'from €1,800, support €300 per month',
        priceEur: 1800
      }
    ],
    hourly: 'Consulting, code review or help for your team: €90 per hour.',
    casesTitle: 'Work I can show',
    cases: [
      {
        title: 'Personal assistant agent in Telegram',
        text: 'My own assistant for daily work: mail, calendar, memory in markdown files, model subscriptions rotated between providers. In daily use. The repository is private.'
      },
      {
        title: 'Agent hive with mechanical acceptance',
        text: 'Executor agents take cards from a queue. A card closes only after an acceptance command exits with 0 and the agent writes a report. Owner clarifications reach the agent while it works.'
      },
      {
        title: 'quota-balancer (qb)',
        text: 'Quota scheduler and model gateway for coding-agent subscriptions and API keys: each task goes where quota is left.',
        href: 'https://github.com/pasekahq/quota-balancer'
      },
      {
        title: 'ulei',
        text: 'Agent harness in Rust: own agent loop over the qb gateway, Telegram channel, owner inbox.',
        href: 'https://github.com/pasekahq/ulei'
      },
      {
        title: 'ummanu',
        text: 'Agent orchestration with shared memory, task pipelines, skills and recovery across several CLI agents.',
        href: 'https://github.com/pasekahq/ummanu'
      },
      {
        title: 'ru-it-stt-eval',
        text: 'Reproducible benchmark of speech-to-text engines on Russian speech with English IT terms.',
        href: 'https://github.com/vladmesh/ru-it-stt-eval'
      },
      {
        title: 'Inspect AI contributor',
        text: 'Two merged PRs in the UK AISI eval framework: a grade-parse failure is now unscored instead of incorrect (#4048), and vLLM models get the server context window (#4216).',
        href: inspectPrs
      },
      {
        title: 'Hands-On Tutorials for Inspect AI',
        text: 'Co-authored post on LessWrong: worked examples of building evals with Inspect AI.',
        href: inspectTutorials
      },
      {
        title: 'Character model test for a companion app',
        text: 'Paid evaluation of a character model: test scenarios and a written report. The client is not named.'
      }
    ],
    contactTitle: 'Contact',
    contactText: 'Write what you are building and what goes wrong.',
    emailLabel: 'Email',
    telegramLabel: 'Telegram'
  },
  ru: {
    metaTitle:
      'Разработка LLM-агентов и чат-ботов под ключ: Telegram-бот с LLM, оценка качества (evals), мультиагентная оркестрация',
    metaDescription:
      'Владислав Мешкорудный делает LLM-чат-боты и агентов и ставит evals, которые показывают, работают ли они. Пакеты с фиксированной ценой от €1,500. Удалённо, часовой пояс EU.',
    eyebrow: 'LLM-системы',
    title: 'LLM-системы под ключ: чат-боты, агенты, evals',
    intro: [
      'Я разрабатываю LLM-агентов и чат-ботов и ставлю evals, которые показывают, работают ли они. Частичная занятость, фиксированная цена, удалённо с Кипра (часовой пояс EU).',
      'С чем обычно приходят: Telegram-бот с LLM под ключ, мультиагентная оркестрация для внутреннего процесса или оценка качества LLM-продукта, который уже в проде. У каждого пакета ниже фиксированные объём и цена.'
    ],
    packagesTitle: 'Пакеты',
    timelineLabel: 'Срок',
    priceLabel: 'Цена',
    packages: [
      {
        id: 'audit',
        name: 'Аудит LLM-продукта',
        summary: 'Где ваш бот или агент ошибается и что чинить первым.',
        includes: [
          'Разбор архитектуры, промптов и трейсов',
          'Baseline-eval на 50 ваших реальных кейсах',
          'Ошибки, сгруппированные по типам',
          'Список правок по ожидаемому эффекту',
          'Созвон 45 минут по итогам'
        ],
        timeline: '1 неделя',
        price: '€1,500, засчитывается в следующий пакет',
        priceEur: 1500
      },
      {
        id: 'eval-harness',
        name: 'Eval-харнесс',
        summary: 'Набор тестов для LLM-продукта, который запускается на каждое изменение.',
        includes: [
          'Golden set на 100–200 кейсов',
          'Детерминированные проверки и LLM-судья, откалиброванный по ручной разметке (Inspect AI или promptfoo)',
          'Регрессионный гейт в вашем CI',
          'Письменный отчёт',
          'Харнесс остаётся у вас'
        ],
        timeline: '2–3 недели',
        price: '€3,500',
        priceEur: 3500
      },
      {
        id: 'agent-system',
        name: 'Агентская система или оркестратор',
        summary: 'Один или несколько агентов с инструментами, по вехам.',
        includes: [
          'Инструменты, память, очередь задач и приёмка',
          'Ретраи, лимиты запросов и квот',
          'Evals и на траекторию агента, и на финальный ответ',
          'Около 50 часов на веху'
        ],
        timeline: '4–6 недель на веху',
        price: 'от €5,000 за веху',
        priceEur: 5000
      },
      {
        id: 'chatbot',
        name: 'Telegram- или веб-бот с LLM',
        summary: 'Бот под ключ, который отвечает по вашим данным.',
        includes: [
          'Сценарии под вашу задачу',
          'RAG по вашим документам или базе',
          'Админка и логи',
          'Smoke-набор тестов с первого дня',
          'Деплой на ваш сервер'
        ],
        timeline: '2–3 недели',
        price: 'от €1,800, поддержка €300 в месяц',
        priceEur: 1800
      }
    ],
    hourly: 'Консультации, ревью кода, помощь команде: €90 в час.',
    casesTitle: 'Что можно посмотреть',
    cases: [
      {
        title: 'Личный ассистент-агент в Telegram',
        text: 'Мой ассистент для ежедневной работы: почта, календарь, память в markdown, ротация подписок между провайдерами моделей. Работает каждый день. Репозиторий приватный.'
      },
      {
        title: 'Рой агентов с механической приёмкой',
        text: 'Агенты-исполнители берут карточки из очереди. Карточка закрывается, только когда команда приёмки вернула 0 и агент написал отчёт. Уточнения владельца доходят до агента по ходу работы.'
      },
      {
        title: 'quota-balancer (qb)',
        text: 'Планировщик квот и шлюз моделей для подписок coding-агентов и API-ключей: задача уходит туда, где осталась квота.',
        href: 'https://github.com/pasekahq/quota-balancer'
      },
      {
        title: 'ulei',
        text: 'Агентский харнесс на Rust: свой агентский цикл поверх шлюза qb, канал Telegram, входящие владельца.',
        href: 'https://github.com/pasekahq/ulei'
      },
      {
        title: 'ummanu',
        text: 'Оркестрация агентов: общая память, пайплайны задач, навыки, восстановление после сбоев для нескольких CLI-агентов.',
        href: 'https://github.com/pasekahq/ummanu'
      },
      {
        title: 'ru-it-stt-eval',
        text: 'Воспроизводимый бенчмарк распознавания речи на русском с английскими IT-терминами.',
        href: 'https://github.com/vladmesh/ru-it-stt-eval'
      },
      {
        title: 'Контрибьютор Inspect AI',
        text: 'Два смерженных PR во фреймворк evals UK AISI: ошибка разбора оценки теперь даёт unscored вместо incorrect (#4048), модели vLLM получают окно контекста сервера (#4216).',
        href: inspectPrs
      },
      {
        title: 'Hands-On Tutorials for Inspect AI',
        text: 'Пост в соавторстве на LessWrong: разборы того, как строить evals на Inspect AI.',
        href: inspectTutorials
      },
      {
        title: 'Тест character-модели для companion-приложения',
        text: 'Платная оценка character-модели: сценарии и письменный отчёт. Клиент не называется.'
      }
    ],
    contactTitle: 'Контакты',
    contactText: 'Напишите, что вы делаете и что не работает.',
    emailLabel: 'Email',
    telegramLabel: 'Telegram'
  }
};
