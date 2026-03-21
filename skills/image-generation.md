---
name: image-generation
description: Generate images using OpenAI DALL-E API. Use when the user asks to generate, create, or draw an image.
---

# Image Generation Skill

Generate images using OpenAI DALL-E 3 via API.

## Environment Variables Required
- `OPENAI_API_KEY` -- OpenAI API key

## Generate an Image (DALL-E 3)

```bash
curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "YOUR_PROMPT_HERE",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "response_format": "url"
  }'
```

Response will contain `data[0].url` -- the generated image URL.

## Size Options
- `1024x1024` -- square (default)
- `1792x1024` -- landscape (16:9)
- `1024x1792` -- portrait (9:16)

## Quality Options
- `standard` -- faster, cheaper
- `hd` -- higher detail, costs more (remind user before using)

## Download and Send via Telegram

After generating, download and send to user:

```bash
# Download image
curl -s "IMAGE_URL" -o /tmp/generated_image.png

# Send via Telegram
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendPhoto" \
  -F chat_id="CHAT_ID" \
  -F photo=@"/tmp/generated_image.png" \
  -F caption="PROMPT_SUMMARY"
```

## Cost Awareness
- DALL-E 3 standard 1024x1024: ~$0.04/image
- DALL-E 3 HD: ~$0.08/image
- Always remind the user before generating HD quality.

## How to Apply
When the user asks to generate or draw an image:
1. Confirm the prompt with the user if ambiguous.
2. Call the DALL-E 3 API with the prompt.
3. Download the result and send it via Telegram.
4. Mention the cost if HD quality was used.
