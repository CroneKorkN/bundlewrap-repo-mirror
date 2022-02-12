```
systemctl is-active "$(systemctl cat zfs-mirror.timer | grep Unit= | cut -d= -f2)"
```
