
`echo export REST_API_PASS=$(bw metadata mseibert.mailman -k mailman/api_password | jq -r .mailman.api_password)`
```sh
curl -s -o /dev/null \
     -w "Status: %{http_code}\nTime: %{time_total}s\n" \
     -u restadmin:$REST_API_PASS \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8001/3.1/queues/in \
     -d '{
       "list_id": "testlist-2.mailman.ckn.li",
       "text": "From: i@ckn.li\nTo: testlist-2@mailman.ckn.li\nSubject: Curl-Driven Test $(date)\n\nHello everyone — this is a test sent via curl! $(date)"
     }'
```

`tail -f /var/log/mailman3/*.log`

```log
==> /var/log/mailman3/mailman.log <==
[12/Jul/2025:10:31:10 +0000] "POST /3.1/queues/in HTTP/1.1" 201 0 "-" "curl/7.88.1"
Jul 12 10:31:10 2025 (2895919) ACCEPT: <175231627036.2895954.10009667988468073605@mseibert.mailman>

==> /var/log/mailman3/smtp.log <==
Jul 12 10:31:12 2025 (2895922) <175231627036.2895954.10009667988468073605@mseibert.mailman> smtp to testlist-2@mailman.ckn.li for 1 recips, completed in 0.059294939041137695 seconds
Jul 12 10:31:12 2025 (2895922) <175231627036.2895954.10009667988468073605@mseibert.mailman> post to testlist-2@mailman.ckn.li from i@ckn.li, 333 bytes
Jul 12 10:31:12 2025 (2895922) <175231627160.2895923.10669516773822847070@mseibert.mailman> smtp to testlist-2@mailman.ckn.li for 1 recips, completed in 0.0047571659088134766 seconds
Jul 12 10:31:12 2025 (2895922) <175231627160.2895923.10669516773822847070@mseibert.mailman> post to testlist-2@mailman.ckn.li from testlist-2-bounces@mailman.ckn.li, 736 bytes
```

`journalctl -f | grep postfix/`

`mailq | head -20`