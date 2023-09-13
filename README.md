# Telegram API Webhook

**Telegram bot implementation using webhooks**

This is a POC (Proof Of Concept) for telegram bot automation using webhook integration.

## Components
- fastapi
- uvicorn
- ngrok [or] equivalent

## Implementation
Setting up a telegram bot server using webhook
- Create a webhook using FastAPI
- Host the webhook on Ngrok or any other ReverseProxy
- Set the webhook on TelegramAPI

## Get Started

#### Environment Variables
- **BOT_TOKEN** - Telegram authentication token provided by @BotFather
- **NGROK_TOKEN** - Ngrok authentication token to initiate tunneling _(not required if using a pre-configured **WEBHOOK**)_

**[Optionally]**
- **HOST** - Defaults to `localhost` (`127.0.0.1`)
- **PORT** - Defaults to `8443`
- **ENDPOINT** - Defaults to `/telegram-webhook`
- **WEBHOOK** - Pre-configured webhook
- **CERTIFICATE** - File path to the public certificate _(only required when using self-signed certs)_
  > For more information visit https://core.telegram.org/bots/self-signed
