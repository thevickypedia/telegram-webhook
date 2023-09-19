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
- **NGROK_TOKEN** - Ngrok authentication token to initiate tunneling _(not required if using a
  pre-configured **WEBHOOK**)_

**[Optionally]**

- **HOST** - Defaults to `localhost` (`127.0.0.1`)
- **PORT** - Defaults to `8443`
- **ENDPOINT** - Defaults to `/telegram-webhook`
- **WEBHOOK** - Pre-configured webhook
- **CERTIFICATE** - File path to the public certificate _(only required when using self-signed certs)_
  > For more information visit https://core.telegram.org/bots/self-signed
- **SECRET_TOKEN** - Secret token sent in a header in every webhook request to ensure that the request comes from a
  webhook set by the owner.
- **DEBUG** - Boolean flag to enable debug level logging.

###### Sample request

If a secret token was set in env var, the header `X-Telegram-Bot-Api-Secret-Token` is required for two-factor
authentication.

> The following code snippet replicates `TelegramAPI` does.

```python
import os
from urllib.parse import urljoin

import requests

from config import settings

payload = {'message': {'text': 'hello-world', 'chat': {'id': os.environ.get('CHAT_ID')}}}

public = settings.certificate
private = 'private.pem'
bundle = 'ca_bundle.pem'

with open(public, 'rb') as public_file, open(private, 'rb') as private_file, open(bundle, 'wb') as output_file:
    public_data = public_file.read()
    private_data = private_file.read()
    output_file.write(public_data + private_data)

response = requests.post(url=urljoin(str(settings.webhook), settings.endpoint),
                         json=payload, cert=(public, private), verify=bundle,
                         headers={"X-Telegram-Bot-Api-Secret-Token": settings.secret_token}, timeout=5)
print(response.status_code)
print(response.text)
```

#### References

- [Using self-signed certificates](https://core.telegram.org/bots/self-signed)
- [Making webhook requests](https://core.telegram.org/bots/api#making-requests)
- [Certificate as `inputFile` object](https://core.telegram.org/bots/api#inputfile)
- [Guide to webhooks](https://core.telegram.org/bots/webhooks)
