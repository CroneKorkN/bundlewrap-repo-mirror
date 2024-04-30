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
