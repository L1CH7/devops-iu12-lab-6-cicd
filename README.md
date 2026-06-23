# devops-cicd-lab

[![CI Pipeline](https://github.com/L1CH7/devops-iu12-lab-6-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/L1CH7/devops-iu12-lab-6-cicd/actions/workflows/ci.yml)

**Лабораторная работа № 6: CI/CD Pipeline на GitHub Actions**  
Курс: DevOps и инфраструктура | Уровень: Магистратура
* **Студент:** L1CH7
* **Репозиторий проекта:** https://github.com/L1CH7/devops-iu12-lab-6-cicd

---

## Описание

Простое Flask-приложение с полноценным CI/CD пайплайном на GitHub Actions, переведённое на современный инструмент управления зависимостями `uv`.

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

# Новое приветствие с поддержкой query-параметра ?name
FEATURE_NEW_GREETING=true python -m flask run
curl "http://localhost:5000/greeting?name=Alice"
# → {"greeting": "Hello, Alice! 🎉 (new greeting feature)"}
```

---

## Локальный запуск (с использованием uv)

```bash
cd app
uv sync --all-extras
PYTHONPATH=. uv run python src/app.py
```

### Запуск тестов
```bash
cd app
PYTHONPATH=. uv run pytest tests/ -v
```

### Проверка линтером
```bash
cd app
uv run ruff check src/ tests/
```

### Docker (запуск из реестра пакетов GHCR)

**Ссылка на собранный пакет (Package):** https://github.com/L1CH7/devops-iu12-lab-6-cicd/pkgs/container/devops-cicd-lab

```bash
# Стянуть собранный образ ветки master
docker pull ghcr.io/l1ch7/devops-cicd-lab:master

# Запуск стабильной версии (feature-флаг выключен)
docker run -d -p 5000:5000 --name app_stable ghcr.io/l1ch7/devops-cicd-lab:master

# Запуск с активированным фича-флагом
docker run -d -p 5001:5000 -e FEATURE_NEW_GREETING=true --name app_feature ghcr.io/l1ch7/devops-cicd-lab:master
```

---

## CI/CD Архитектура

### CI Pipeline (Diamond Pattern)

```
push/PR → master
         │
      [build]  ← кэш uv зависимостей
         │
    ┌────┼────┐
    ▼    ▼    ▼
 [lint] [test] [security-scan]   ← Fan-Out (параллельно)
    │    │    │
    └────┼────┘
         ▼
  [quality-gate]  ← Fan-In (ждёт все три)
         │
  [docker-build]  ← только на master, SHA тег, GHA cache
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
| Кэширование uv зависимостей (`enable-cache: true`) | ✅ |
| Сохранение test-results как артефакт | ✅ |
| Trivy security scan + pip-audit | ✅ |
| Docker image с SHA тегом | ✅ |
| Docker layer cache (type=gha) | ✅ |
| GitHub Environments (staging + production) | ✅ |
| Manual approval для production | ✅ |
| Smoke tests между staging и production | ✅ |
| Branch protection на master | ✅ |
| Feature flag через env переменную | ✅ |
| Conventional Commits | ✅ |
| CI Status Badge | ✅ |
| Dependabot | ✅ |

---

## Trunk-Based Development & Branch Protection

1. Всегда работаем от `master`. Прямой пуш в `master` заблокирован правилами Branch Protection.
2. Вся разработка ведётся в короткоживущих feature-ветках.
3. Слияние изменений — исключительно через Pull Request после прохождения `quality-gate` (*Required Status Check*).
4. Feature flags для переключения функциональности без мёртвого кода.

**Пример успешного Pull Request с проверками:** https://github.com/L1CH7/devops-iu12-lab-6-cicd/pull/1

---

## Бонусы и продвинутый функционал

- **CI Badge** в README ✅
- **Dependabot** настроен (`.github/dependabot.yml`) ✅
- **Matrix Build** — запуск тестов параллельно на Python 3.12 и 3.13 ✅
