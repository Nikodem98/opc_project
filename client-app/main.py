import asyncio
import psycopg2

from asyncua.sync import Client

def conn(val):
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
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.execute('SELECT * FROM tempe2')
        index = len(crsr.fetchall())
        crsr.execute('INSERT INTO tempe2 (id, temperature) VALUES (%s, %s)', (index, val))
        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        conn(val)
        print("Python: New value", val)

    def event_notification(self, event):
        print("Python: New event", event)

async def main():
    client = Client("opc.tcp://localhost:1888")
    client.connect()
    tag1 = client.get_node("i=13;ns=2")
    print(f"tag1 is: {tag1} with value {tag1.get_value()}")

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    handle1 = sub.subscribe_data_change(tag1)

asyncio.run(main())