# Aruba switch API python  client

Python based REST-API client for Aruba switches (not ArubaOSX).

See workflows for examples on how to use.

### Installation 
```
pip install pyarubaswitch
```

### Basic Usage examples

```
from pyarubaswitch import PyAosClient
client = PyAosClient("192.168.1.4","username","password")


client.get_lldp_aps()              client.get_port_vlan()             client.get_system_status()
client.get_lldp_info()             client.get_snmpv3()                client.get_telnet_server_status()
client.get_lldp_switches()         client.get_sntp()                  
client.get_loop_protected_ports()  client.get_stp_info()              

client.get_loop_protected_ports()
['2'] 

client.get_system_status()
name: switch-name, hw: J9774A, fw: YA.16.10.0007, sn: XXXXXXX
```
**note** that method above uses HTTP and is not secure. To use HTTPS you must first install a certificate on the switch and then use the client with ssl.
To use ssl for all calls, no validation of cert:
```
ssl_client = PyAosClient("192.168.1.4","username","password",SSL=True)  
```
To use validate ssl:
```
ssl_client = PyAosClient("192.168.1.4","username","password",SSL=True,validate_ssl=True)
```
To use ssl only for login. https is slow performing for all calls. So if you dont consider the rest of the data sensitive use this.
```
ssl_client = PyAosClient("192.168.1.4","username","password",ssl_login=True)
```

The runners in workslows can also be used with a variable file in yaml-format like so:
```
username: "username"
password: "supersecretpassword"
switches:
  - "192.168.1.4"
  - "192.168.1.5"
```