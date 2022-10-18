mailserver
==========

argin2 hashes
-------------

`echo -n 'WarumGehtDasNicht?' | argon2 FAPf+gTwqTRr+3H0cDktqw`

logs
----

`journalctl -u postfix@-.service -u dovecot.service -u rspamd.service -o cat -f`
