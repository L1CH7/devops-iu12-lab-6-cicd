# devops-cicd-lab

[![CI Pipeline](https://github.com/L1CH7/devops-iu12-lab-6-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/L1CH7/devops-iu12-lab-6-cicd/actions/workflows/ci.yml)

**Лабораторная работа № 6: CI/CD Pipeline на GitHub Actions**  
Курс: DevOps и инфраструктура | Уровень: Магистратура

---

## Описание

Простое Flask-приложение с полноценным CI/CD пайплайном на GitHub Actions.

### Эндпоинты приложения

| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `/` | GET | Информация о сервисе: name, version, hostname |
| `/health` | GET | Статус здоровья приложения |
| `/greeting` | GET | Приветствие (управляется feature flag) |

### Feature Flag

Эндпоинт `/greeting` управляется переменной окружения `FEATURE_NEW_GREETING`:
```bash
# Классическое приветствие (по умолчанию)
curl http://localhost:5000/greeting
# → {"greeting": "Hello, World!"}

# Новое приветствие
FEATURE_NEW_GREETING=true python -m flask run
curl http://localhost:5000/greeting
# → {"greeting": "Hello from the new greeting feature! 🎉"}
```

---

## Локальный запуск

```bash
cd app
pip install -r requirements.txt
PYTHONPATH=. python src/app.py
```

### Запуск тестов
```bash
cd app
PYTHONPATH=. pytest tests/ -v
```

### Проверка линтером
```bash
cd app
ruff check src/ tests/
```

### Docker
```bash
docker build -t devops-cicd-lab ./app
docker run -p 5000:5000 devops-cicd-lab
```

---

## CI/CD Архитектура

### CI Pipeline (Diamond Pattern)

```
push/PR → main
         │
      [build]  ← кэш pip зависимостей
         │
    ┌────┼────┐
    ▼    ▼    ▼
 [lint] [test] [security-scan]   ← Fan-Out (параллельно)
    │    │    │
    └────┼────┘
         ▼
  [quality-gate]  ← Fan-In (ждёт все три)
         │
  [docker-build]  ← только на main, SHA тег, GHA cache
```

### CD Pipeline (Promotion Pattern)

```
CI успешно →
  [deploy-staging]   ← автоматически (environment: staging)
         │
  [smoke-test]       ← проверка staging
         │
  [deploy-production] ← ручное подтверждение (environment: production)
```

---

## GitHub Actions Features

| Feature | Статус |
|---------|--------|
| Diamond Pipeline (Fan-Out + Fan-In) | ✅ |
| Кэширование pip зависимостей | ✅ |
| Сохранение test-results как артефакт | ✅ |
| Trivy security scan + pip-audit | ✅ |
| Docker image с SHA тегом (не :latest) | ✅ |
| Docker layer cache (type=gha) | ✅ |
| GitHub Environments (staging + production) | ✅ |
| Manual approval для production | ✅ |
| Smoke tests между staging и production | ✅ |
| Branch protection на main | ✅ |
| Feature flag через env переменную | ✅ |
| Conventional Commits | ✅ |
| CI Status Badge | ✅ |
| Dependabot | ✅ |

---

## Trunk-Based Development

1. Всегда работаем от `main`
2. Feature branches живут не более 1-2 дней
3. Все изменения — через Pull Request
4. Merge только после прохождения `quality-gate`
5. Feature flags для переключения функциональности без мёртвого кода

---

## Бонусы

- **CI Badge** в README ✅
- **Dependabot** настроен (`.github/dependabot.yml`) ✅
- **Reusable Workflow** — общая логика вынесена в переиспользуемый workflow ✅
