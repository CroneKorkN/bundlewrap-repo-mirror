# wake on lan

## woken

wol by magic packet

```
ethtool -s enp1s0 wol g
```

p  Wake on phy activity
u  Wake on unicast messages
m  Wake on multicast messages
b  Wake on broadcast messages
a  Wake on ARP
g  Wake on MagicPacket(tm)
s  Enable SecureOn(tm) password for MagicPacket(tm)
d  Disable (wake on nothing).  This option clears all previous options.

```
systemctl suspend
```

## waker

```
wakeonlan d8:cb:8a:e7:be:c6
```
