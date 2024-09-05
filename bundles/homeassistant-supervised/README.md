https://github.com/home-assistant/supervised-installer?tab=readme-ov-file
https://github.com/home-assistant/os-agent/tree/main?tab=readme-ov-file#using-home-assistant-supervised-on-debian
https://docs.docker.com/engine/install/debian/





https://www.home-assistant.io/installation/linux#install-home-assistant-supervised
https://github.com/home-assistant/supervised-installer
https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md

DATA_SHARE=/usr/share/hassio dpkg --force-confdef --force-confold -i homeassistant-supervised.deb

neu debian
ha installieren
gucken ob geht
dann bw drüberbügeln


https://www.home-assistant.io/integrations/http/#ssl_certificate

`wget "$(curl -L https://api.github.com/repos/home-assistant/supervised-installer/releases/latest | jq -r '.assets[0].browser_download_url')" -O homeassistant-supervised.deb && dpkg -i homeassistant-supervised.deb`
