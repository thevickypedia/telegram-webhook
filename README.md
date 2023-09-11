# telegram-webhook
Telegram bot implementation using webhooks

This is a POC (Proof Of Concept) for telegram bot automation using webhook integration.

## Components
- fastapi
- uvicorn
- ngrok

## Implementation
Setting up a telegram bot server using webhook
- Create a webhook using FastAPI
- Host the webhook on Ngrok
- Set the webhook on TelegramAPI

## Get Started

#### Environment Variables
- **BOT_TOKEN** - Telegram authentication token provided by @BotFather
- **NGROK_TOKEN** - Ngrok authentication token to initiate tunneling

**[Optionally]**
- **HOST** - Defaults to `localhost` (`127.0.0.1`)
- **PORT** - Defaults to `8443`
