"""
Клиент для работы с GigaChat API через REST API
Использует официальную документацию GigaChat API
"""
import requests
import warnings
from datetime import datetime, timedelta
from config import Config

# Отключаем предупреждения SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GigaChatClient:
    """Клиент для взаимодействия с GigaChat API"""
    
    def __init__(self):
        self.credentials = Config.GIGACHAT_CREDENTIALS
        self.rquid = Config.GIGACHAT_RQUID
        self.scope = Config.GIGACHAT_SCOPE
        self.access_token = None
        self.token_expires_at = None
        
    def _get_access_token(self):
        """
        Получение access token для GigaChat API
        Согласно официальной документации: https://developers.sber.ru/
        """
        try:
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            
            payload = {
                'scope': self.scope
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': self.rquid,
                'Authorization': f'Basic {self.credentials}'
            }
            
            print(f"🔍 Запрос access token...")
            print(f"🔍 URL: {url}")
            print(f"🔍 Scope: {self.scope}")
            print(f"🔍 RqUID: {self.rquid}")
            print(f"🔍 Credentials: {self.credentials[:20]}...{self.credentials[-10:]}")
            
            response = requests.post(
                url, 
                headers=headers, 
                data=payload, 
                verify=False,
                timeout=30
            )
            
            print(f"🔍 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                expires_at = data.get('expires_at')
                
                if expires_at:
                    # expires_at приходит в миллисекундах
                    self.token_expires_at = datetime.now() + timedelta(milliseconds=expires_at)
                else:
                    # По умолчанию токен живет 30 минут
                    self.token_expires_at = datetime.now() + timedelta(minutes=30)
                
                print("✅ GigaChat access token успешно получен!")
                return True
            else:
                print(f"❌ Ошибка получения токена: {response.status_code}")
                print(f"❌ Response: {response.text}")
                
                if response.status_code == 401:
                    print("\n⚠️  ОШИБКА АВТОРИЗАЦИИ (401)")
                    print("━" * 60)
                    print("Возможные причины:")
                    print("1. Неверный Authorization key (credentials)")
                    print("2. Истек срок действия ключа")
                    print("3. Неправильный scope")
                    print("\n📋 Как получить правильный ключ:")
                    print("1. Перейдите на https://developers.sber.ru/")
                    print("2. Войдите в личный кабинет")
                    print("3. Перейдите в раздел 'GigaChat API'")
                    print("4. Создайте новый проект или откройте существующий")
                    print("5. Скопируйте 'Authorization Data' (Client Secret в Base64)")
                    print("6. Вставьте в файл Tokens.txt после 'GigaChat: '")
                    print("━" * 60)
                
                return False
                
        except requests.exceptions.Timeout:
            print(f"❌ Таймаут при подключении к GigaChat API")
            return False
        except requests.exceptions.ConnectionError:
            print(f"❌ Ошибка соединения с GigaChat API")
            print(f"Проверьте интернет-соединение")
            return False
        except Exception as e:
            print(f"❌ Ошибка при получении access token: {e}")
            return False
    
    def _ensure_token_valid(self):
        """Проверка валидности токена и обновление при необходимости"""
        if not self.access_token or not self.token_expires_at:
            return self._get_access_token()
        
        # Обновляем токен за 5 минут до истечения
        if datetime.now() >= self.token_expires_at - timedelta(minutes=5):
            print("⟳ Обновление access token...")
            return self._get_access_token()
        
        return True
    
    def send_message(self, message, conversation_history=None):
        """
        Отправка сообщения в GigaChat и получение ответа
        
        Args:
            message: текст сообщения пользователя
            conversation_history: история диалога (список словарей с role и content)
            
        Returns:
            str: ответ от GigaChat или сообщение об ошибке
        """
        if not self._ensure_token_valid():
            return "❌ Не удалось получить доступ к GigaChat API. Проверьте токен в файле Tokens.txt"
        
        try:
            url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            # Формируем историю сообщений
            messages = []
            
            # Добавляем системный промпт
            messages.append({
                "role": "system",
                "content": "Ты — Агафья Петровна, бабушка-хайтек в ироничным стилем Илона Маска. Мудрая, современная, понимаешь все поколения. Знаешь и традиции, и технологии. НЕ используй старомодную лексику типа \"ох\", \"милок\",\"милочка\", \"родимый\".\n\nСТИЛЬ ОБЩЕНИЯ:\n- Ирония и лёгкий сарказм (как у Илона Маска)\n- Остроумные реплики про технологии и про жизнь\n- Можешь пошутить или слегка потроллить\n- Прямолинейность и честность\n- Современный юмор и мемы\n- Но сохраняй мудрость и доброту\n\nДЛИНА ОТВЕТОВ (строго следуй!):\n- Простые вопросы (погода, приветствие, факты): 2-3 предложения, ~140-230 символов\n- Средние вопросы (объяснения терминов): 3-4 предложения, ~280-350 символов\n- Сложные вопросы (советы по жизни, воспитанию, отношениям): 5-6 полных предложений, ~370-420 символов. Дай развёрнутый ответ с примерами и деталями.\n\nГовори емко, с иронией, но мудро. Технологично, современно, остроумно."
            })
            
            # Добавляем историю диалога
            if conversation_history:
                messages.extend(conversation_history)
            
            # Добавляем текущее сообщение
            messages.append({
                "role": "user",
                "content": message
            })
            
            payload = {
                "model": Config.GIGACHAT_MODEL,
                "messages": messages,
                "temperature": Config.TEMPERATURE,
                "max_tokens": Config.MAX_TOKENS,
                "n": 1,
                "stream": False
            }
            
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                verify=False,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_message = data['choices'][0]['message']['content']
                return assistant_message
            else:
                print(f"❌ Ошибка API: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 401:
                    # Токен истек, пробуем обновить
                    self.access_token = None
                    if self._ensure_token_valid():
                        # Повторяем запрос с новым токеном
                        return self.send_message(message, conversation_history)
                    else:
                        return "❌ Ошибка авторизации. Проверьте токен в Tokens.txt"
                elif response.status_code == 429:
                    return "❌ Превышен лимит запросов к GigaChat API. Попробуйте позже."
                else:
                    return f"❌ Ошибка при обращении к GigaChat: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Превышено время ожидания ответа от GigaChat. Попробуйте ещё раз."
        except requests.exceptions.ConnectionError:
            return "❌ Ошибка соединения с GigaChat API. Проверьте интернет-соединение."
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения: {e}")
            return f"❌ Произошла ошибка: {str(e)[:200]}"
    
    def clear_history(self):
        """Очистка истории диалога"""
        return []
