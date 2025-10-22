@echo off
chcp 65001 > nul
echo ======================================
echo  Запуск Telegram бота Агафья
echo ======================================
echo.

REM Проверка наличия Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.8+ с https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

REM Проверка установленных зависимостей
echo Проверка зависимостей...
python -c "import telegram" > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Зависимости не установлены. Установка...
    pip install -r requirements.txt
    echo.
    echo Проверка установки...
    python -c "import telegram, requests" > nul 2>&1
    if %errorlevel% neq 0 (
        echo [ОШИБКА] Не удалось установить зависимости!
        pause
        exit /b 1
    )
    echo [OK] Зависимости успешно установлены
) else (
    echo [OK] Зависимости уже установлены
)

echo.
echo ======================================
echo  Запуск бота...
echo ======================================
echo.

REM Запуск бота
python bot.py

pause

