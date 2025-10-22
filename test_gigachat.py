"""
Тестовый скрипт для проверки подключения к GigaChat через REST API
"""
import sys
import io
import warnings
warnings.filterwarnings('ignore')

# Устанавливаем кодировку UTF-8 для Windows консоли
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import Config
from gigachat_client import GigaChatClient

def test_gigachat():
    """Тестирование подключения к GigaChat"""
    print("="*60)
    print("🧪 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К GIGACHAT API")
    print("="*60)
    
    # Загружаем токены
    print("\n📂 Загрузка токенов из файла Tokens.txt...")
    if not Config.load_tokens():
        print("❌ Не удалось загрузить токены!")
        return False
    
    print(f"\n🔑 Telegram Token: {Config.TELEGRAM_TOKEN[:20]}...")
    print(f"🔑 GigaChat Credentials: {Config.GIGACHAT_CREDENTIALS[:20]}...{Config.GIGACHAT_CREDENTIALS[-10:]}")
    print(f"🔑 Scope: {Config.GIGACHAT_SCOPE}")
    
    # Инициализация клиента
    print("\n" + "="*60)
    print("🔧 ИНИЦИАЛИЗАЦИЯ GIGACHAT КЛИЕНТА")
    print("="*60)
    
    client = GigaChatClient()
    
    # Получение access token
    print("\n" + "="*60)
    print("🔐 ПОЛУЧЕНИЕ ACCESS TOKEN")
    print("="*60 + "\n")
    
    if not client._get_access_token():
        print("\n" + "="*60)
        print("❌ ТЕСТ ПРОВАЛЕН: Не удалось получить access token")
        print("="*60)
        return False
    
    # Тестовый запрос
    print("\n" + "="*60)
    print("💬 ОТПРАВКА ТЕСТОВОГО СООБЩЕНИЯ")
    print("="*60)
    
    test_message = "Привет! Представься, пожалуйста."
    print(f"\n👤 Пользователь: {test_message}")
    print("⏳ Ожидание ответа от GigaChat...\n")
    
    response = client.send_message(test_message)
    
    if response.startswith("❌"):
        print("\n" + "="*60)
        print("❌ ТЕСТ ПРОВАЛЕН")
        print("="*60)
        print(f"\n{response}\n")
        print("="*60)
        return False
    
    print("="*60)
    print("✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
    print("="*60)
    print(f"\n🤖 GigaChat: {response}\n")
    print("="*60)
    print("✅ Все работает отлично! Можете запускать бота командой:")
    print("   python bot.py")
    print("="*60)
    return True

if __name__ == "__main__":
    test_gigachat()
