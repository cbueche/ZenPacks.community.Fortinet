# Fortinet / Fortigate monitoring

## Introduction

This is a Zenpack for [Fortinet FortiGate firewalls](https://www.fortinet.com/products/firewalls/firewall.html). The [existing Zenpack](http://wiki.zenoss.org/ZenPack:Fortigate_SNMP_Monitor) by Fabio Paracchini seems to be abandoned and use obsolete MIB's. This Zenpack is developed using [zenpacklib](https://zenpacklib.zenoss.com).

## Supported devices

I only had FortiGate models 100D and 3000D with OS version 5.x to test my zenpack. Feel free to try it with other models, and report if it works or break. I'm happy to assist you to get it working with other models.

### models

- 100D and 3000D (OS version 5.x) : confirmed by @cbueche
- Fortigate 800C : confirmed by @mattbze

# Features

- serial number and firmware version in overview page
- interface traffic
- CPU load
- memory load
- disk usage
- session count
- IPS statistics
- Sensors (voltage, temperature, fans, PSU)
- Vdoms
- Per Vdom :
    - interface traffic
    - CPU load
    - memory load
    - disk usage
    - session count and rate

# Release notes

- 23.12.2016 : 1.0.0 : initial version

# Installation

## Pre-requisites : Python packages

The installation of the required PyYAML should happen automatically. If not, use this :

```
easy_install PyYAML
```

## Device class

- create device class `/Network/Firewall/Fortigate`

## Zenpack

- install the Zenpack:

```
zenpack --install ZenPacks.community.Fortinet
zopectl restart; zenhub restart
```

- a full `zenoss restart` is probably better.

## set the Python class of the existing device

This is a one-time operation that is needed for devices that were present before the Zenpack installation (the devices added after installation get the correct Python class automatically). The symptom to decide if you need this: `WARNING zen.ApplyDataMap: no relationship:XXX found on:YYY` in zenhub.log.

*Warning*: this loops must be repeated until no device get moved anymore. Not sure why, maybe some glitch of Zenoss 4.x.

`zendmd`

```
for d in dmd.Devices.Network.Firewall.Fortigate.getSubDevicesGen():
    devname = d.getId()
    print('checking %s' % devname)
    if d.__class__.__name__ != 'FortigateDevice':
        dmd.Devices.Network.Firewall.Fortigate.moveDevices('/Network/Firewall/Fortigate', devname)
        commit()
        print('class of %s set to FortigateDevice' % devname)

```

## Post-installation

### MIB load

If you want to automatically map the device models and the SNMP traps, you need to load two MIB's:

```
cd MIB
cp FORTINET-*.mib $ZENHOME/share/mibs/site
cd $ZENHOME/share/mibs/site
zenmib run -v 10
zentrap restart
```

The go to Zenoss / advanced / MIBs. See if MIBs are available.

### modeler plugins for /Network/Firewall/Fortinet

The plugins are automatically assigned during the Zenpack installation:

- zenoss.snmp.NewDeviceMap
- zenoss.snmp.DeviceMap
- zenoss.snmp.InterfaceMap
- zenoss.snmp.InterfaceAliasMap
- zenoss.snmp.RouteMap
- community.snmp.FortigateGlobal
- community.snmp.FortigateSensor
- community.snmp.FortigateVdom
- community.snmp.FortigateIPS

# Development notes

Using Vagrant in Virtualbox, use `vagrant up` to create and start a Zenoss to further develop this Zenpack. In the VM, /tmp/work is mapped to the Zenpack source, you can use these commands to install it:

    zenpack --link --install ZenPacks.community.Fortinet
    zopectl restart; zenhub restart

# Known issues

In HA-mode, the `zenoss.snmp.RouteMap` modeler plugin produces these warnings in zenhub.log:

    WARNING zen.IpInterface: Adding IP Address 10.1.2.3 to Index_47 found it on device 10.4.5.6

The reason for the warning is probably that both firewall instances see the same values and fight over who owns them. To avoid the issue, remove the `zenoss.snmp.RouteMap` modeler plugin from /Network/Firewall/Fortigate. The consequence is the loss of the `Network Routes` from the Components view.

# To-do

- automate the device class creation for `/Network/Firewall/Fortigate`
- automate the installation of the MIBs
- event clear from monitoring/performance template
- disk usage alertings
- add a screenshot with real-life data

# Resources

- [zenpacklib](http://zenpacklib.zenoss.com/)
- [FORTINET-FORTIGATE-MIB](http://www.oidview.com/mibs/12356/FORTINET-FORTIGATE-MIB.html)
