#
# Fortigate IPS modeling for Fortinet zenpack
#
# uses fortinet/fnFortiGateMib/fgIps/fgIpsStatsTable : 1.3.6.1.4.1.12356.101.9.2.1.1
#

from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class FortigateIPS(SnmpPlugin):

    relname = 'fortigateIPSs'
    modname = 'ZenPacks.community.Fortinet.FortigateIPS'

    snmpGetTableMaps = (
        GetTableMap(
            'fgIpsStatsEntry', '1.3.6.1.4.1.12356.101.9.2.1.1', {
                '.1': 'fgIpsIntrusionsDetected',
                '.2': 'fgIpsIntrusionsBlocked',
                '.3': 'fgIpsCritSevDetections',
                '.4': 'fgIpsHighSevDetections',
                '.5': 'fgIpsMedSevDetections',
                '.6': 'fgIpsLowSevDetections',
                '.7': 'fgIpsInfoSevDetections',
                '.8': 'fgIpsSignatureDetections',
                '.9': 'fgIpsAnomalyDetections',
                }
            ),
        GetTableMap(
            'FgVdEntry', '1.3.6.1.4.1.12356.101.3.2.1.1', {
                '.1': 'fgVdEntIndex',
                '.2': 'fgVdEntName',
                }
            ),
        )

    def process(self, device, results, log):

        # prepare a mapping dict : fgVdEntIndex --> fgVdEntName
        vdom_table = results[1].get('FgVdEntry', {})
        vdoms = {}
        for snmpindex, row in vdom_table.items():
            log.debug('vdom entry : <%s> - <%s>' % (snmpindex, row))
            vdoms[snmpindex.strip('.')] = row['fgVdEntName']
        log.debug('vdoms = <%s>' % vdoms)

        # now get the IPS table info and map to Vdom's
        intrusions = results[1].get('fgIpsStatsEntry', {})
        rm = self.relMap()
        for snmpindex, row in intrusions.items():

            idx = snmpindex.strip('.')
            vdom = vdoms[idx]
            intrusions_detected = row.get('fgIpsIntrusionsDetected')
            intrusions_blocked = row.get('fgIpsIntrusionsBlocked')
            idname = vdom

            log.debug('IPS entry added : idx=%s, name=%s' % (idx, idname))
            rm.append(self.objectMap({
                'id': self.prepId(idname),
                'title': idname,
                'snmpindex': idx,
                'intrusions_detected': intrusions_detected,
                'intrusions_blocked': intrusions_blocked,
                }))

        #log.debug('rm=<%s>' % rm)
        return rm
