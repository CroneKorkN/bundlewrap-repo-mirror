```
setfacl -Rm g:telegraf:rX /var/spool/postfix/
setfacl -dm g:telegraf:rX /var/spool/postfix/
```

TODO io
```bash
for pid in $(ls /proc | grep '^[0-9]\+$')
do
  out=$(cat /proc/$pid/io 2> /dev/null) || continue
  read="$(echo $out | grep '^read_bytes:' | cut -d' ' -f2)"
  write="$(echo $out | grep '^write_bytes:' | cut -d' ' -f2)"
  [ $read = 0 ] && [ $write = 0 ] && continue
  comm=$(cat /proc/$pid/comm); echo "$comm: $read/$write"
done
```
