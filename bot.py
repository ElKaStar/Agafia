"""
Telegram бот с интеграцией GigaChat AI
"""
import sys
import io
import logging
import warnings
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from gigachat_client import GigaChatClient

# Устанавливаем кодировку UTF-8 для Windows консоли
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Отключаем предупреждения SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# GigaChat клиент будет инициализирован после загрузки токенов
gigachat = None

# Хранилище истории диалогов для каждого пользователя
user_conversations = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    welcome_message = (
        "👋 Привет! Я — Агафья Петровна, бабушка-хайтек с иронией Илона Маска.\n\n"
        "Понимаю все поколения, знаю технологии и традиции. "
        "Отвечаю с долей сарказма, но всегда по делу 😏\n\n"
        "💬 Что умею:\n"
        "• Давать советы (иногда язвительно, но мудро)\n"
        "• Объяснять технологии с юмором\n"
        "• Троллить глупые вопросы... шучу, отвечу на все\n"
        "• Быть честной и прямолинейной\n\n"
        "📱 Команды:\n"
        "/start - Перезапуск системы\n"
        "/clear - Форматирование памяти\n"
        "/help - Мануал для чайников\n\n"
        "Пиши что хочешь. Обещаю не слишком язвить 🚀"
    )
    
    await update.message.reply_text(welcome_message)
    logger.info(f"Пользователь {user_id} запустил бота")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_message = (
        "💡 Агафья Петровна — бабушка-хайтек + Илон Маск mode\n\n"
        "📱 Команды:\n"
        "/start - Reboot\n"
        "/clear - Delete history.exe\n"
        "/help - RTFM (это она)\n\n"
        "💬 Как общаться:\n"
        "• Личка: пиши что угодно\n"
        "• Группы: упомяни 'Агафья' (иначе проигнорирую)\n"
        "• Reply на моё сообщение тоже работает\n"
        "• Помню контекст (не как твой браузер)\n"
        "• Говорю с иронией, но честно\n"
        "• Технологии + мудрость + сарказм\n\n"
        "Погнали! 🚀"
    )
    
    await update.message.reply_text(help_message)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /clear - очистка истории диалога"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    await update.message.reply_text(
        "🔄 Память отформатирована. Кто ты вообще такой? Шучу, начинаем с нуля."
    )
    logger.info(f"Пользователь {user_id} очистил историю диалога")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id
    chat_type = update.message.chat.type
    user_message = update.message.text
    
    logger.info(f"Сообщение от {user_id} в чате {chat_type}: {user_message}")
    
    # Проверяем, нужно ли отвечать в групповом чате
    if chat_type in ['group', 'supergroup']:
        # В групповых чатах отвечаем только если:
        # 1. Упомянули "Агафья Петровна" или "Агафья" или "агафья"
        # 2. Или это ответ на наше сообщение
        # 3. Или упомянули бота через @username
        
        bot_mentioned = False
        message_lower = user_message.lower()
        
        # Проверяем упоминания имени
        if 'агафья петровна' in message_lower or 'агафья' in message_lower:
            bot_mentioned = True
            logger.info("Бот упомянут по имени в группе")
        
        # Проверяем, это ответ на сообщение бота
        if update.message.reply_to_message:
            if update.message.reply_to_message.from_user.id == context.bot.id:
                bot_mentioned = True
                logger.info("Это ответ на сообщение бота")
        
        # Проверяем упоминание через @username
        if update.message.entities:
            for entity in update.message.entities:
                if entity.type == "mention":
                    mention_text = user_message[entity.offset:entity.offset + entity.length]
                    bot_username = context.bot.username
                    if bot_username and f"@{bot_username}" == mention_text:
                        bot_mentioned = True
                        logger.info("Бот упомянут через @username")
        
        # Если бот не упомянут, игнорируем сообщение
        if not bot_mentioned:
            logger.info("Бот не упомянут в групповом чате, игнорируем")
            return
    
    # Инициализируем историю для нового пользователя
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    # Отправляем "печатает..." пока ждём ответ
    await update.message.chat.send_action("typing")
    
    try:
        # Получаем ответ от GigaChat
        conversation_history = user_conversations[user_id]
        response = gigachat.send_message(user_message, conversation_history)
        
        # Сохраняем диалог в истории
        user_conversations[user_id].append({
            "role": "user",
            "content": user_message
        })
        user_conversations[user_id].append({
            "role": "assistant",
            "content": response
        })
        
        # Ограничиваем историю последними 10 сообщениями (5 пар вопрос-ответ)
        if len(user_conversations[user_id]) > 10:
            user_conversations[user_id] = user_conversations[user_id][-10:]
        
        # Отправляем ответ пользователю
        await update.message.reply_text(response)
        logger.info(f"Ответ отправлен пользователю {user_id}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await update.message.reply_text(
            "😔 Извините, произошла ошибка при обработке вашего сообщения. "
            "Попробуйте ещё раз или используйте /clear для очистки истории."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "😔 Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        )


def main():
    """Основная функция запуска бота"""
    global gigachat
    
    print("🚀 Запуск Telegram бота Агафья...")
    
    # Загружаем токены
    if not Config.load_tokens():
        print("❌ Не удалось загрузить токены. Проверьте файл Tokens.txt")
        return
    
    # Инициализация GigaChat клиента ПОСЛЕ загрузки токенов
    print("🔧 Инициализация GigaChat клиента...")
    gigachat = GigaChatClient()
    
    print("🔧 Инициализация бота...")
    
    # Создаём приложение
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    
    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    print("✅ Бот успешно запущен и готов к работе!")
    print("Нажмите Ctrl+C для остановки бота\n")
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

