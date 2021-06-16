DOVECOT
=======

rescan index: https://doc.dovecot.org/configuration_manual/fts/#rescan

```
    sudo -u vmail doveadm fts rescan -u 'test@mail2.sublimity.de'
    sudo -u vmail doveadm index -u 'test@mail2.sublimity.de' -q '*'
```
