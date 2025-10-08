export const skillGroups = [
  {
    title: { ru: 'Backend', en: 'Backend' },
    description: {
      ru: 'Проектирование API и сервисов, устойчивых к росту нагрузки.',
      en: 'Designing resilient APIs and services ready to scale.'
    },
    items: ['Python', 'FastAPI', 'Django', 'Go', 'Node.js', 'GraphQL', 'REST', 'gRPC']
  },
  {
    title: { ru: 'Данные и AI', en: 'Data & AI' },
    description: {
      ru: 'Внедряю ML/LLM-агентов, пайплайны и MLOps.',
      en: 'Implement ML/LLM agents, pipelines, and MLOps practices.'
    },
    items: ['LangChain', 'OpenAI API', 'PydanticAI', 'PostgreSQL', 'ClickHouse', 'Airflow']
  },
  {
    title: { ru: 'DevOps', en: 'DevOps' },
    description: {
      ru: 'Настраиваю CI/CD, мониторинг и инфраструктуру.',
      en: 'Ship CI/CD, monitoring, and infrastructure automation.'
    },
    items: ['Docker', 'Kubernetes', 'Terraform', 'GitHub Actions', 'Grafana', 'Prometheus']
  },
  {
    title: { ru: 'Коммуникации', en: 'Communication' },
    description: {
      ru: 'Организую процессы и помогаю командам доставлять результаты.',
      en: 'Align teams and processes to deliver measurable outcomes.'
    },
    items: ['Team Leadership', 'Roadmapping', 'Stakeholder Management', 'Tech Writing']
  }
] as const;
