Pg Pass workaround: set manually:

```
root@freescout /ro psql freescout
psql (15.6 (Debian 15.6-0+deb12u1))
Type "help" for help.

freescout=# \password freescout
Enter new password for user "freescout":
Enter it again:
freescout=#
\q
```


# problems

# check if /opt/freescout/.env is resettet
# ckeck `psql -h localhost -d freescout -U freescout -W`with pw from .env
# chown -R www-data:www-data /opt/freescout
# sudo su - www-data -c 'php /opt/freescout/artisan freescout:clear-cache' -s /bin/bash
# javascript funny? `sudo su - www-data -c 'php /opt/freescout/artisan storage:link' -s /bin/bash`
# benutzer bilder weg? aus dem backup holen: `/opt/freescout/.zfs/snapshot/zfs-auto-snap_hourly-2024-11-22-1700/storage/app/public/users` `./customers`
