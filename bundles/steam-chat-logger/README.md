# steam-chat-logger

Stores Steam friend chats in PostgreSQL; Steam itself keeps about 14 days.
[steam_chat_logger](https://git.sublimity.de/cronekorkn/steam_chat_logger) is the application.

## No Steam login on the node

- The node holds no Steam session. A login of its own, by QR code with hourly token renewal, ran from
  2026-10-25 until Steam locked the account as possibly hijacked.
- The chats come from `steam-chat-export.user.js` in a browser that is logged in to Steam anyway: once a day
  it reads them with that session and posts them to `https://<steam-chat-viewer hostname>/import`.
- `steam-chat-logger.service` runs `receiver.py`, which stores an export and fetches names, avatars and
  images from Steam's public urls.
- Do not bring back a timer or a login on the node without the maintainer asking for it.

## Setting up a browser

- Install the userscript from the application repo in Tampermonkey or Violentmonkey.
- Set the import token through the userscript menu. It is `steam-chat-logger/import_token` in the node's
  metadata; read it yourself, an agent must not print it.

## Monitoring

- `steam chat import` turns critical when `/var/lib/steam_chat_logger/last_import` is older than 4 days:
  the browser was closed, logged out of Steam or lost its token.

## Cross-bundle

- The `/import` location lives in the vhost of `steam-chat-viewer`, which reads
  `steam-chat-logger/import_port`.
- `steam-chat-viewer` declares the database too, so it works on a node without this bundle.
