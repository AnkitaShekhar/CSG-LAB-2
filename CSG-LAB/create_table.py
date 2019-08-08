import sqlite3

conn = sqlite3.connect('KCLAB.db')
print("Opened database successfully")

conn.execute('CREATE TABLE datacenter (virtualmachine TEXT,'
             'ipaddress TEXT, '
             'guestos TEXT, '
             'powerstate TEXT, '
             'uptime INT, '
             'datastore TEXT, '
             'cpu TEXT, '
             'memorey TEXT,'
             'hardisk TEXT,'
             'esxi TEXT,'
             'datacenter TEXT,'
             'vcenter TEXT)')

print("Table created successfully")
conn.close()

