https://github.com/dehydrated-io/dehydrated/wiki/example-dns-01-nsupdate-script

```sh
printf "server 127.0.0.1
zone acme.resolver.name.
update add _acme-challenge.ckn.li.acme.resolver.name. 600 IN TXT "hello"
send
" | nsupdate -y hmac-sha512:acme:XXXXXX
```
