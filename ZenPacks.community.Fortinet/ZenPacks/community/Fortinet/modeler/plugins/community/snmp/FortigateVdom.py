#
# Fortigate Vdom modeling for Fortinet zenpack
#
# uses fortinet/fnFortiGateMib/fgVirtualDomain/fgVdEntry : 1.3.6.1.4.1.12356.101.3
#

from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class FortigateVdom(SnmpPlugin):

    relname = 'fortigateVdoms'
    modname = 'ZenPacks.community.Fortinet.FortigateVdom'

    '''
    FgVdEntry ::= SEQUENCE {
        fgVdEntIndex    FgVdIndex,          1
        fgVdEntName     DisplayString,      2
        fgVdEntOpMode   FgOpMode,           3
        fgVdEntHaState  FgHaState,          4
        fgVdEntCpuUsage Gauge32,            5
        fgVdEntMemUsage Gauge32,            6
        fgVdEntSesCount Gauge32,            7
        fgVdEntSesRate  Gauge32             8
    }
'''

    snmpGetTableMaps = (
        GetTableMap(
            'FgVdEntry', '1.3.6.1.4.1.12356.101.3.2.1.1', {
                '.1': 'fgVdEntIndex',
                '.2': 'fgVdEntName',
                '.3': 'fgVdEntOpMode',
                '.4': 'fgVdEntHaState',
                }
            ),
        )

    def process(self, device, results, log):

        sensors = results[1].get('FgVdEntry', {})

        rm = self.relMap()
        for snmpindex, row in sensors.items():

            idx = snmpindex.strip('.')
            vdom_index = row.get('fgVdEntIndex')
            vdom_name = row.get('fgVdEntName')
            vdom_opmode = row.get('fgVdEntOpMode')
            vdom_hastate = row.get('fgVdEntHaState')
            idname = vdom_name

            log.debug('vdom entry added : idx=%s, index=%s, name=%s' % (idx, vdom_index, vdom_name))
            rm.append(self.objectMap({
                'id': self.prepId(idname),
                'title': vdom_name,
                'snmpindex': idx,
                'opmode': vdom_opmode,
                'hastate': vdom_hastate,
                }))

        #log.debug('rm=<%s>' % rm)
        return rm
