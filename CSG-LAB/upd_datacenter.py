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
            cur.execute('insert into datacenter (virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, cpu, memorey, hardisk, esxi, datacenter, vcenter) '
                    'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', [key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10]])

    def get_vm(self, con):
        cur = con.cursor()
        print("Fetching VM data")
        cur.execute("select virtualmachine, ipaddress, guestos, powerstate, uptime, datastore, esxi, datacenter, vcenter, cpu, memorey, hardisk from datacenter")
        newlist = [row for row in list(cur)]



        newvmlist = []
        for val1 in newlist:
            value = [val2 for val2 in val1]
            newvmlist.append(value)
        print(newvmlist)


        for value in newvmlist:
            print(value[4])
            newuptime = vcenter_db.convertuptime(self, value[4])
            memory = vcenter_db.format_kbytes(self, int(value[10]))
            hardisk = vcenter_db.format_bytes(self, int(value[11]))

            print(newuptime, memory, hardisk)
            value[4] = newuptime
            value[10] = memory
            value[11] = hardisk
            print(value[4])
        return newvmlist

    def get_esxi(self, con):
        cur = con.cursor()
        print("Fetching esxi data")
        cur.execute("select DISTINCT esxi, bladecpu, bladevcpu, bladememory, bladehardisk, blademodel, esxiversion, datacenter, vcenter from datacenter")
        newlist = [row for row in list(cur)]

        newesxilist = []
        for val1 in newlist:
            value = [val2 for val2 in val1]
            newesxilist.append(value)

        print(newesxilist)

        for value in newesxilist:
            memory = vcenter_db.format_bytes(self, int(value[3]))
            hardisk = vcenter_db.format_bytes(self, int(value[4]))
            value[3] = memory
            value[4] = hardisk

        newesxi = []
        for value in newesxilist:
            cur.execute('select count(virtualmachine) from datacenter where esxi=?', [value[0]])
            val1 = [val[0] for val in cur]

            cur.execute('select count(powerstate) from datacenter where esxi=? and powerstate="poweredOn"', [value[0]])
            val2 = [val[0] for val in cur]

            cur.execute('select count(powerstate) from datacenter where esxi=? and powerstate="poweredOff"', [value[0]])
            val3 = [val[0] for val in cur]

            val4 = value + val1 + val2 + val3
            newesxi.append(val4)
        print(newesxi)
        return newesxi

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
                 ("{0} second{1} ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
        return result

    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
            size = round(size)
        return str(size) + power_labels[n]+'B'

    def format_kbytes(self, size):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: 'K', 1: 'M', 2: 'G', 3: 'T'}
        while size > power:
            size /= power
            n += 1
            size = round(size)
        return str(size) + power_labels[n]+'B'

    def dashboard_data(self, con):
        cur = con.cursor()
        print("Fetching Data for showing in dashaboard")
        cur.execute('select count(DISTINCT vcenter), count(DISTINCT datacenter), count(DISTINCT esxi), count(DISTINCT virtualmachine) from datacenter')
        return list(cur)

    def dc_data(self,con):
        cur = con.cursor()
        print("Fetching data for datacenter")
        cur.execute('select DISTINCT datacenter from datacenter')



        print()
        dcdata = [value[0] for value in cur]
        print(dcdata)
        dclist = {}
        tmplist = []
        for value in dcdata:
            cur = con.cursor()
            cur.execute('select count(esxi), count(virtualmachine), vcenter from datacenter where datacenter=?', [value])
            tmp1 = []
            for row in cur:
                tmp1.append(row)
            print(tmp1)

            tmp2 = []
            for row in tmp1:
                tmp2.append(row)
            print(tmp2)

            tmplist.append(value)
            print(tmplist + tmp)
            print(tmplist)
            #dclist.append( list(value) + list(cur))
            print(tmplist)
        return dclist