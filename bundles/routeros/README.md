initialization:
- reset (hold reset for 5-10 seconds, until user light starts flashing)
- open webinterface under 192.168.88.1
- set password
- vlans need to be configured and an additional ip needs to be assined to a vlan which es later accessible preferably through an untagged port
- for example add 10.0.0.62/24 to "home" vlan
- this happens on the first apply
- when vlan filering gets enabled, the apply freezes and the switch is no longer available under the old ip
- now that filtering is active, the switch is available under its new ip, because now you dont speak to the bridge anymore, where the old ip was residing, but to the vlan interface, where the new ip is residing

bw bug:
- f"/interface/bridge/vlan?vlan-ids={vlan_id}&dynamic=false" fails, you need to remove &dynamic=false on create and then add it again

old 6.x Routeros firmware vlan filtering not working:
- update firmware first
- upload to files and just reboot
- didnt work via web interface, log said firmware image broken
- didi work via winbox
