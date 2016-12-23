#
# Fortigate sensor modeling for Fortinet zenpack
#
# uses fortinet/fnFortiGateMib/fgSystem/fgHwSensors : 1.3.6.1.4.1.12356.101.4.3
#

from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin,
    GetTableMap
    )
from Products.DataCollector.plugins.DataMaps import ObjectMap

class FortigateSensor(SnmpPlugin):

    relname = 'fortigateSensors'
    modname = 'ZenPacks.community.Fortinet.FortigateSensor'

    # get the sensors
    snmpGetTableMaps = (
        GetTableMap(
            'fgHwSensorEntry', '1.3.6.1.4.1.12356.101.4.3.2.1', {
                '.1': 'fgHwSensorEntIndex',
                '.2': 'fgHwSensorEntName',
                '.3': 'fgHwSensorEntValue',
                '.4': 'fgHwSensorEntAlarmStatus',
                }
            ),
        )

    def process(self, device, results, log):

        sensors = results[1].get('fgHwSensorEntry', {})
        rm = self.relMap()
        for snmpindex, row in sensors.items():

            idx = snmpindex.strip('.')
            sensor_index = row.get('fgHwSensorEntIndex')
            sensor_name = row.get('fgHwSensorEntName')
            sensor_value = row.get('fgHwSensorEntValue')
            sensor_alarm_status = row.get('fgHwSensorEntAlarmStatus')
            idname = sensor_name

            log.debug('sensor entry added : idx=%s, index=%s, name=%s, value=%s, al_status=%s' % (idx, sensor_index, sensor_name, sensor_value, sensor_alarm_status))
            rm.append(self.objectMap({
                'id': self.prepId(idname),
                'title': idname,
                'snmpindex': idx,
                'svalue': sensor_value,
                'status': sensor_alarm_status,
                }))

        return rm
