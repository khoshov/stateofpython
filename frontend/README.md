# Survey Frontend

Modern frontend для системы опросов, построенный на Next.js и shadcn/ui.

## Особенности

- **Next.js 15** с App Router
- **shadcn/ui** компоненты для красивого интерфейса
- **TypeScript** для типобезопасности
- **Tailwind CSS** для стилизации
- **Responsive design** - работает на всех устройствах

## Пользовательский сценарий

1. **Главная страница**: Пользователь вводит email и нажимает "Участвовать в опросе"
2. **Email отправка**: Система отправляет ссылку на опрос (в демо версии сразу перенаправляет)
3. **Прохождение опроса**: Пользователь отвечает на вопросы по одному, ответы сохраняются после каждого вопроса
4. **Завершение**: После последнего вопроса показывается экран завершения
5. **Просмотр ответов**: Пользователь может посмотреть все свои ответы

## Технические особенности

### Компоненты UI
- `Button` - кнопки с различными вариантами
- `Card` - контейнеры для контента
- `Input` - поля ввода
- `RadioGroup` - выбор одного варианта
- `Progress` - индикатор прогресса
- `Badge` - значки для ответов

### Страницы
- `/` - главная страница с вводом email
- `/survey/[token]` - прохождение опроса
- `/results/[token]` - просмотр результатов

### API Integration
- `surveyApi.submitEmail()` - отправка email для участия
- `surveyApi.getQuestions()` - получение вопросов
- `surveyApi.submitAnswer()` - сохранение ответа
- `surveyApi.getResults()` - получение результатов

## Установка и запуск

### Установка зависимостей
```bash
npm install
```

### Конфигурация
```bash
cp .env.local.example .env.local
```

Отредактируйте `.env.local` и укажите URL вашего FastAPI бэкенда:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Запуск в режиме разработки
```bash
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

### Сборка для продакшена
```bash
npm run build
npm start
```

## Структура проекта

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # Главная страница
│   │   ├── survey/[token]/    # Страница опроса
│   │   └── results/[token]/   # Страница результатов
│   ├── components/ui/         # shadcn/ui компоненты
│   └── lib/
│       ├── utils.ts          # Утилиты
│       └── api/              # API клиент
├── public/                    # Статические файлы
└── package.json
```

## Интеграция с Backend

Фронтенд ожидает следующие API endpoints от FastAPI:

- `POST /api/v1/survey/participate` - участие в опросе
- `GET /api/v1/survey/questions?token=` - получение вопросов
- `POST /api/v1/survey/answer` - отправка ответа
- `GET /api/v1/survey/results?token=` - получение результатов
- `POST /api/v1/survey/complete` - завершение опроса

## Разработка

### Добавление новых компонентов UI
```bash
npx shadcn@latest add [component-name]
```

### Кастомизация тем
Редактируйте CSS переменные в `src/app/globals.css`

### Типы данных
Все типы определены в `src/lib/api/types.ts`
