# 🤖 Агафья - Telegram Бот с GigaChat AI

Telegram-бот на Python с интеграцией искусственного интеллекта GigaChat от Сбера.

## 📋 Описание

Агафья — это интеллектуальный Telegram-бот, который использует API GigaChat от Сбера через REST API для ведения диалогов, ответов на вопросы и помощи пользователям. Бот запоминает контекст разговора и может поддерживать последовательные диалоги.

**Технологии:**
- Python 3.8+
- python-telegram-bot для Telegram API
- Прямые REST API запросы к GigaChat (без LangChain)
- OAuth 2.0 авторизация

## ✨ Возможности

- 💬 Ведение диалогов с учётом контекста
- 🧠 Использование AI-модели GigaChat от Сбера
- 📝 Ответы на вопросы и помощь в различных задачах
- 🔄 Управление историей диалога
- 🇷🇺 Поддержка русского и английского языков

## 🚀 Установка и запуск

### Требования

- Python 3.8 или выше
- Telegram токен (получить у [@BotFather](https://t.me/BotFather))
- GigaChat credentials (получить на [developers.sber.ru](https://developers.sber.ru/))

### Шаг 1: Клонирование/Скачивание проекта

```bash
cd C:\Users\licos\Desktop\projects\AgafiaBotTG
```

### Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 3: Настройка токенов

Убедитесь, что файл `Tokens.txt` содержит ваши токены в следующем формате:

```
Telegram: ВАШ_TELEGRAM_TOKEN
GigaChat: ВАШ_GIGACHAT_CREDENTIALS
```

**Как получить токены:**

1. **Telegram Token:**
   - Откройте [@BotFather](https://t.me/BotFather) в Telegram
   - Отправьте команду `/newbot`
   - Следуйте инструкциям
   - Скопируйте полученный токен

2. **GigaChat Credentials (Authorization Data):**
   - Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru/)
   - Войдите в личный кабинет
   - Перейдите в раздел "GigaChat API"
   - Создайте новый проект или откройте существующий
   - Скопируйте **Authorization Data** (Client Secret в формате Base64)
   - **Важно:** Копируйте полностью весь ключ, включая символы `==` в конце!

### Шаг 4: Тестирование подключения (рекомендуется)

Перед запуском бота рекомендуется проверить подключение к GigaChat:

```bash
python test_gigachat.py
```

Если тест пройден успешно, вы увидите ответ от GigaChat и можете переходить к следующему шагу.

### Шаг 5: Запуск бота

```bash
python bot.py
```

После успешного запуска вы увидите:
```
✓ Токены успешно загружены
🔧 Инициализация бота...
✅ Бот успешно запущен и готов к работе!
```

## 📱 Использование

### Команды бота

- `/start` - Начать работу с ботом
- `/help` - Получить справку
- `/clear` - Очистить историю диалога

### Пример использования

1. Найдите вашего бота в Telegram по username
2. Отправьте команду `/start`
3. Начните диалог, отправив любое сообщение
4. Бот ответит с использованием GigaChat AI

## 🏗️ Структура проекта

```
AgafiaBotTG/
│
├── bot.py                  # Основной файл бота
├── gigachat_client.py      # Клиент для GigaChat API
├── config.py               # Конфигурация
├── requirements.txt        # Зависимости Python
├── Tokens.txt             # Токены (не версионируется)
├── .gitignore             # Игнорируемые файлы
└── README.md              # Документация
```

## 🔧 Конфигурация

Вы можете настроить параметры в файле `config.py`:

```python
GIGACHAT_MODEL = "GigaChat"  # Модель GigaChat
TEMPERATURE = 0.7            # Креативность ответов (0.0 - 1.0)
MAX_TOKENS = 1024           # Максимальная длина ответа
```

## 📚 Документация API

- [GigaChat API Documentation](https://developers.sber.ru/docs/ru/gigachat/api/overview)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)

## ⚠️ Важные замечания

1. **Безопасность:** Никогда не публикуйте файл `Tokens.txt` в открытых репозиториях
2. **SSL:** Бот использует отключение проверки SSL для GigaChat API (по требованию API)
3. **Лимиты:** Соблюдайте лимиты GigaChat API согласно вашему тарифному плану
4. **История:** Бот сохраняет последние 10 сообщений для контекста диалога

## 🐛 Решение проблем

### Ошибка при подключении к GigaChat

Проверьте:
- Правильность GigaChat credentials в `Tokens.txt`
- Активность подписки на GigaChat API
- Доступ к интернету

### Бот не отвечает в Telegram

Проверьте:
- Правильность Telegram токена
- Запущен ли бот (`python bot.py`)
- Логи в консоли

## 📝 Лицензия

Этот проект создан в образовательных целях.

## 👨‍💻 Автор

Создано для работы с GigaChat API от Сбера.

## 🔗 Ссылки

- [Сбер Разработчикам](https://developers.sber.ru/)
- [GigaChat](https://developers.sber.ru/portal/products/gigachat-api)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Приятного использования! 🎉**

