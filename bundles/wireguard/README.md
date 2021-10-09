echo module wireguard +p > /sys/kernel/debug/dynamic_debug/control
dmesg -wT | grep wireguard
