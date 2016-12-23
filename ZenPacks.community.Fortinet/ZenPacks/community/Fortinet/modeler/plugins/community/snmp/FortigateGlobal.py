#
# Fortigate global modeling for Fortinet zenpack
#

from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin,
    GetMap
    )
from Products.DataCollector.plugins.DataMaps import ObjectMap

class FortigateGlobal(SnmpPlugin):

    relname = 'fortigateGlobal'
    modname = 'ZenPacks.community.Fortinet.FortigateGlobal'

    # get the serial number and the firmware version
    snmpGetMap = GetMap({'.1.3.6.1.4.1.12356.100.1.1.1.0': 'fnSysSerial',
                         '.1.3.6.1.4.1.12356.101.4.1.1.0': 'fgSysVersion'})

    def process(self, device, results, log):

        # getting the serial number
        serial = results[0].get('fnSysSerial', 'noserial')
        log.debug('got serial = %s' % serial)
        om_serial = ObjectMap({'serialNumber': serial}, compname='hw')

        # getting the firmware version
        fversion = results[0].get('fgSysVersion', 'noversion')
        log.debug('got version = %s' % fversion)
        om_version = ObjectMap({'setOSProductKey': fversion})

        data_to_return = [om_serial, om_version]
        log.debug('data_to_return = <%s>' % data_to_return)
        return data_to_return
