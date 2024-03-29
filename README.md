# Aruba switch API python  client

Python based REST-API client for Aruba switches (not ArubaOSX).

See workflows for examples on how to use.

### Requirements
Only tested with REST-API version 7 on aruba switch. The older REST-APIs where very slow anyhow.
See https://asp.arubanetworks.com for latest firmware.
You can check firmware version here: 
http:///switch-ip-adress/rest/version

Also requires the requests module.

### Installation 
```
pip install pyarubaswitch
```

### Basic Usage examples

```
from pyarubaswitch import ArubaSwitchClient
client = ArubaSwitchClient("192.168.1.4","username","password")


client.get_lldp_aps()              client.get_port_vlan()             client.get_system_status()
client.get_lldp_info()             client.get_snmpv3()                client.get_telnet_server_status()
client.get_lldp_switches()         client.get_sntp()                  
client.get_loop_protected_ports()  client.get_stp_info()              

client.get_loop_protected_ports()
['2'] 

client.get_system_status()
name: switch-name, hw: J9774A, fw: YA.16.10.0007, sn: XXXXXXX

client.logout()
```
Always do .logout() after your done with API calls. Otherwise the switch might run out of API-sessions and you must either reset rest-api interface on the switch or wait for the session timer to run out.

**note** that method above uses HTTP and is not secure. To use HTTPS you must first install a certificate on the switch and then use the client with ssl.
To use ssl for all calls, no validation of cert:
```
ssl_client = ArubaSwitchClient("192.168.1.4","username","password",SSL=True)  
```
To use validate ssl:
```
ssl_client = ArubaSwitchClient("192.168.1.4","username","password",SSL=True,validate_ssl=True)
```


The runners in workslows can also be used with a variable file in yaml-format like so:
```
username: "username"
password: "supersecretpassword"
switches:
  - "192.168.1.4"
  - "192.168.1.5"
```
### How to generate self-signed cert on switch from cli 
```
Configuration example: 
    (config)# crypto pki identity-profile Test_Profile subject
    Enter Common Name(CN) : myTestSwitch
    Enter Org Unit(OU) : myOrgUnit
    Enter Org Name(O) : myOrg
    Enter Locality(L) : myLocation
    Enter State(ST) : myState
    Enter Country(C) : NL
    (config)# crypto pki enroll-self-signed certificate-name Test_Certificate
    or : crypto pki enroll-self-signed certificate-name test2 key-type ecdsa
    (config)# web-management ssl

```
### Very simplle self-signed cert sample with rest-enabled sample
```
rest-interface
crypto pki enroll-self-signed certificate-name sll-self subject common-name switchmgmt
web-management ssl
```