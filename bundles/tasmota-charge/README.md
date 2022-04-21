# Phone

- install termux from F-Droid
- install termux::api from F-Droid
- open termux
- run `pkg update`
- run `pkg install termux-api openssh`
- run `passwd` and set a password
- run `whoami` to get the username
- run `sshd` to start ssh server
- run `su - tasmota-charge -c 'ssh-copy-id -p 8022 u0_a233@10.0.0.175'` on server node
- acquire wakelock for the termux session in notifications

# Server

- you can run something like `su - tasmota-charge -c 'ssh -p 8022 u0_a233@10.0.0.175'`
