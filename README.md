# TODO

- dont spamfilter forwarded mails
- gollum wiki
- blog?
- fix dkim not working sometimes
- LDAP
- oauth2/OpenID
- icinga

Raspberry pi as soundcard
- gadget mode
- OTG g_audio
- https://audiosciencereview.com/forum/index.php?threads/raspberry-pi-as-usb-to-i2s-adapter.8567/post-215824

# install bw fork

pip3 install --editable git+file:///Users/mwiegand/Projekte/bundlewrap-fork@main#egg=bundlewrap

# monitor timers

```sh
Timer=backup

Triggers=$(systemctl show ${Timer}.timer --property=Triggers --value)
echo $Triggers
if systemctl is-failed "$Triggers"
then
  InvocationID=$(systemctl show "$Triggers" --property=InvocationID --value)
  echo $InvocationID
  ExitCode=$(systemctl show "$Triggers" -p ExecStartEx --value | sed 's/^{//' | sed 's/}$//' | tr ';' '\n' | xargs -n 1 | grep '^status=' | cut -d '=' -f 2)
  echo $ExitCode
  journalctl INVOCATION_ID="$InvocationID" --output cat
fi
```

telegraf: execd for daemons

TEST
