# Phone

- install termux from Play Store
- install termux::api from Play Store
- open termux
- run `pkg install termux-api openssh`
- run `passwd` and set a password
- run `whoami` to get the username
- run `sshd` to start ssh server
- acquire wakelock for the termux session in notifications

# Server

- you can run something like `su - tasmota-charge -c 'ssh-copy-id -p 8022 u0_q194@10.0.0.166'`
