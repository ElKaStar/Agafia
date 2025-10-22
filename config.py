"""
Конфигурационный файл для Telegram-бота с GigaChat
"""
import os


class Config:
    """Класс конфигурации приложения"""
    
    # Telegram токен
    TELEGRAM_TOKEN = ""
    
    # GigaChat credentials
    GIGACHAT_CREDENTIALS = ""
    GIGACHAT_RQUID = ""  # Request UID для GigaChat API
    
    # GigaChat API settings
    GIGACHAT_SCOPE = "GIGACHAT_API_PERS"  # Для персонального использования
    GIGACHAT_MODEL = "GigaChat"  # Модель по умолчанию
    
    # Настройки генерации
    TEMPERATURE = 0.7
    MAX_TOKENS = 512  # Гибкая длина в зависимости от сложности вопроса
    
    @staticmethod
    def load_tokens(file_path='Tokens.txt'):
        """Загрузка токенов из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        if line.startswith('Telegram:'):
                            Config.TELEGRAM_TOKEN = line.split(':', 1)[1].strip()
                        elif line.startswith('GigaChat:'):
                            Config.GIGACHAT_CREDENTIALS = line.split(':', 1)[1].strip()
                        elif line.startswith('RqUID:'):
                            Config.GIGACHAT_RQUID = line.split(':', 1)[1].strip()
            
            if not Config.TELEGRAM_TOKEN:
                raise ValueError("Telegram токен не найден в файле")
            if not Config.GIGACHAT_CREDENTIALS:
                raise ValueError("GigaChat credentials не найден в файле")
            if not Config.GIGACHAT_RQUID:
                raise ValueError("RqUID не найден в файле")
                
            print("✓ Токены успешно загружены")
            return True
            
        except FileNotFoundError:
            print(f"❌ Файл {file_path} не найден")
            return False
        except Exception as e:
            print(f"❌ Ошибка при загрузке токенов: {e}")
            return False

