# Content Download

Telegram bot for downloading social-media content through the Content API.

## Content API

Set `CONTENT_API` to the API base URL, for example
`https://content-api.wasmer.app`. Every platform endpoint must return the same
canonical response:

```json
{
  "success": true,
  "platform": "xiaohongshu",
  "original_url": "https://xhslink.cn/...",
  "resolved_url": "https://www.xiaohongshu.com/...",
  "title": "Example title",
  "description": null,
  "thumbnail_url": "https://...",
  "media": [
    {
      "url": "https://...",
      "type": "video",
      "quality": null,
      "extension": "mp4"
    }
  ],
  "metadata": {}
}
```

API failures use:

```json
{
  "success": false,
  "platform": "xiaohongshu",
  "error": {"message": "...", "type": "extraction_error"}
}
```

The bot supports video, image, audio, document, and HLS media returned in the
`media` array. A YouTube message containing `audio` or `music` sends its audio
item; it uses the standard `/youtube` endpoint rather than a separate legacy
endpoint.

## Supported platforms

- YouTube
- Instagram
- Facebook
- Douyin / TikTok
- Bilibili
- Xiaohongshu / RedNote
- HoYoLAB
- X / Twitter

## Required environment variables

- `BOT_TOKEN`
- `DATABASE_URL`
- `CONTENT_API`
