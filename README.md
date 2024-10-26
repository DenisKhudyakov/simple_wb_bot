# Telegram Bot with API WB

В этом руководстве приведены инструкции по настройке и запуску Telegram-бота с помощью Docker Compose. Настройка гарантирует, что бот будет работать в изолированной среде с зависимостями и службами, управляемыми через Docker.
## Предпосылки

- Установите GIT [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Установите на Ваш компьютер [Docker](https://www.docker.com/get-started).
- Установите на Ваш компьютер [Docker Compose](https://docs.docker.com/compose/install/).
- Получите токен у BotFather [Telegram Bot Token](https://core.telegram.org/bots#creating-a-new-bot).



## Запуск

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DenisKhudyakov/simple_wb_bot.git
   cd telegram-bot-docker

2. **Создайте .env файл в корне проекта и укажите необходимые переменные среды, например токен бота:**
    
    TELEGRAM_BOT_TOKEN=your_bot_token

3. **Команда для запуска**

    ```bash
   docker-compose up --build -d
