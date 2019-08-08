import sqlite3
import json

class vcenter_db():

    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def insert_vcenter_db(self, con, vmlist):
        cur = con.cursor()
        print("Inserting VM in db")
        for key, value in vmlist.items():
            cur.execute('insert into datacenter (virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, esxi, datacenter, vcenter, cpu, memorey, hardisk) '
                    'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', [key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10]])

    def get_vm(self, con):
        cur = con.cursor()
        print("Fetching VM data")
        cur.execute("select virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, esxi, datacenter, vcenter, cpu, memorey, hardisk from datacenter")
        return cur

    def get_esxi(self, con):
        cur = con.cursor()
        print("Fetching esxi data")
        cur.execute("select virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, datacenter, vcenter from datacenter where esxi='10.126.218.41'")
        return cur

    def get_datacenter(self, con, assignid):
        cur = con.cursor()
        print("Fetching esxi data")
        cur.execute("select virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, esxi, vcenter from datacenter where datacenter=?", [assignid])
        return cur

    def get_vcenter(self, con):
        cur = con.cursor()
        print("Fetching esxi data")
        cur.execute("select virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, esxi, datacenter from datacenter")
        vcenter = []
        for row in cur:
            vcenter.append(list(row))
        esxi = []
        for value in vcenter:
            esxi.append(value[6])

        mylist = list(dict.fromkeys(esxi))
        my_dict = {}
        for esxi in mylist:
            print(esxi)
            data = []
            for row in list(vcenter):
                if esxi == row[6]:
                    data.append(row)
                    print(data)

            my_dict.update({esxi: data})
            print(my_dict)
        return my_dict

    def convertuptime(self, secs):
        days = secs // 86400
        hours = (secs - days * 86400) // 3600
        minutes = (secs - days * 86400 - hours * 3600) // 60
        seconds = secs - days * 86400 - hours * 3600 - minutes * 60
        result = ("{0} day{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
                 ("{0} hour{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
                 ("{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "") if minutes else "") + \
                 ("{0} second{1}, ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
        return result
