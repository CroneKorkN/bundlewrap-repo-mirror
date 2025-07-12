# Mailman

- django admin udner /admin

## Testmail

`echo export REST_API_PASS=$(bw metadata mseibert.mailman -k mailman/api_password | jq -r .mailman.api_password)`
```sh
curl -s -o /dev/null \
     -w "Status: %{http_code}\nTime: %{time_total}s\n" \
     -u restadmin:$REST_API_PASS \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8001/3.1/queues/in \
     -d "{
       \"list_id\": \"testlist-2.mailman.ckn.li\",
       \"text\": \"From: i@ckn.li\nTo: testlist-2@mailman.ckn.li\nSubject: Curl Test $(date '+%Y-%m-%d %H:%M:%S')\n\nThis message was sent at $(date '+%Y-%m-%d %H:%M:%S').\"
     }"
```

## Log locations

`tail -f /var/log/mailman3/*.log`

`journalctl -f | grep postfix/`

`mailq | head -20`