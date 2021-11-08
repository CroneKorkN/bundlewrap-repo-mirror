https://github.com/dehydrated-io/dehydrated/wiki/example-dns-01-nsupdate-script

```
printf "server 127.0.0.1
zone acme.resolver.name.
update add _acme-challenge.ckn.li.acme.resolver.name. 600 IN TXT "hello"
send
" | nsupdate -y hmac-sha512:acme:Y9BHl85l352BGZDXa/vg90hh2+5PYe4oJxpkq/oQvIODDkW8bAyQSFr0gKQQxjyIOyYlTjf0MGcdWFv46G/3Rg==
```
