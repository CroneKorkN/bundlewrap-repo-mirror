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

pip3 install --editable git+file:///Users/mwiegand/Projekte/bundlewrap-fork#egg=bundlewrap

# monitor timers

```sh
Triggers=$(systemctl show logrotate.timer --property=Triggers --value)
if systemctl is-failed "$Triggers"
do
  InvocationID=$(systemctl show "$Triggers" --property=InvocationID --value)
  journalctl INVOCATION_ID="$InvocationID" --output cat
fi
```
