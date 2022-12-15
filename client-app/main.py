import asyncio
import psycopg2

from asyncua.sync import Client

def conn(val, timestamp, sql, multi):
    connection = None
    try:
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(
            host = "localhost",
            database="OPC_DATA",
            user="OPC_CLIENT",
            password="admin",
            port="5001"
        )
        # create a cursor
        crsr = connection.cursor()
        print(val)
        if multi:
            crsr.execute(sql, (val[0], val[1], val[2], timestamp))
        else:
            crsr.execute(sql, (val, timestamp))
        connection.commit()
        print('Value saved')
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

class ActuatorPositionHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New actuator position value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO actuator_position(value,ts) VALUES(%s, %s);', False)

class EkstruderValueHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New ekstruder value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO ekstruder_value(value1, value2, value3, ts) VALUES(%s,%s,%s, %s);', True)

class LevelSensorHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New level sensor value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO level_sensor(value, ts) VALUES(%s, %s);', False)

class PistonRodHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New piston rod value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO piston_rod(value, ts) VALUES(%s, %s);', False)

class PumpPressureHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New pump pressure value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO pump_pressure(value, ts) VALUES(%s, %s);', False)

class TemperatureHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New temperature value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO temperature_sensor(value, ts) VALUES(%s, %s);', False)

class WorkTimeHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New temperature value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO work_time(value, ts) VALUES(%s, %s);', False)

class VectorDataHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: vector data value", val)
        conn(val, data.monitored_item.Value.SourceTimestamp, 'INSERT INTO vector_data(value1, value2, value3) VALUES(%s,%s,%s);', True)


async def main():
    client = Client("opc.tcp://localhost:1888")
    client.connect()
    actuatorTag = client.get_node("ns=2;i=16")
    ekstruderTag = client.get_node("ns=2;i=10")
    levelTag = client.get_node("ns=2;i=2")
    pistonTag = client.get_node("ns=2;i=12")
    pumpTag = client.get_node("ns=2;i=14")
    temperatureTag = client.get_node("ns=2;i=4")
    timeTag = client.get_node("ns=2;i=8")
    vectorTag = client.get_node("ns=2;i=6")

    client.create_subscription(500, ActuatorPositionHandler()).subscribe_data_change(actuatorTag)
    client.create_subscription(500, EkstruderValueHandler()).subscribe_data_change(ekstruderTag)
    client.create_subscription(500, LevelSensorHandler()).subscribe_data_change(levelTag)
    client.create_subscription(500, PistonRodHandler()).subscribe_data_change(pistonTag)
    client.create_subscription(500, PumpPressureHandler()).subscribe_data_change(pumpTag)
    client.create_subscription(500, TemperatureHandler()).subscribe_data_change(temperatureTag)
    client.create_subscription(500, WorkTimeHandler()).subscribe_data_change(timeTag)
    client.create_subscription(500, VectorDataHandler()).subscribe_data_change(vectorTag)

asyncio.run(main())