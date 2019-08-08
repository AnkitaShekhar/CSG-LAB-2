import sqlite3
import os
import devices_db
import threading
from itertools import chain

class ping():

    def connect_db(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def ping_lab(self, con):
        cur = con.cursor()
        print("Ping reachability check on LAB devices")
        cur.execute('select ipaddress from DEVICES where component="LAB"')
        iplist = [row[0] for row in cur]
        print(iplist)
        for ip in iplist:
            response = os.system("ping -c 1 " + str(ip))
            if response == 0:
                print("Reachability of IP address " + ip + ": " + "Reachable")
                cur.execute('update DEVICES set reachability="Reachable" where ipaddress=?', [ip])
                con.commit()
            else:
                print("Reachability of IP address " + ip + ": " + "Unreachable")
                cur.execute('update DEVICES set reachability="Unreachable" where ipaddress=?', [ip])
                con.commit()
    def ping_dnacset1(self, con):
        cur = con.cursor()
        print("Ping reachability check on DNAC topology devices")
        cur.execute('select ipaddress from DEVICES where topology="DNAC-TOP-1"')
        iplist = [row[0] for row in cur]
        print(iplist)
        for ip in iplist:
            response = os.system("ping -c 1 " + str(ip))
            if response == 0:
                print("Reachability of IP address " + ip + ": " + "Reachable")
                cur.execute('update DEVICES set reachability="Reachable" where ipaddress=?', [ip])
                con.commit()
            else:
                print("Reachability of IP address " + ip + ": " + "Unreachable")
                cur.execute('update DEVICES set reachability="Unreachable" where ipaddress=?', [ip])
                con.commit()
    def ping_dnacset2(self, con):
        cur = con.cursor()
        print("Ping reachability check on DNAC topology devices")
        cur.execute('select ipaddress from DEVICES where topology="DNAC-TOP-2"')
        iplist = [row[0] for row in cur]
        print(iplist)
        for ip in iplist:
            response = os.system("ping -c 1 " + str(ip))
            if response == 0:
                print("Reachability of IP address " + ip + ": " + "Reachable")
                cur.execute('update DEVICES set reachability="Reachable" where ipaddress=?', [ip])
                con.commit()
            else:
                print("Reachability of IP address " + ip + ": " + "Unreachable")
                cur.execute('update DEVICES set reachability="Unreachable" where ipaddress=?', [ip])
                con.commit()
    def mail(self, con):
        cur = con.cursor()
        cur.execute('select distinct component  from DEVICES where topology="DNAC-TOP-1"')
        return cur

    def get_componentwise_data(self, con, componen):
        cur = con.cursor()
        print("Fetching Component wise data" + str(componen))
        comp = cur.execute('select count (ipaddress), '
                           'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                    'sum(case when telnetstatus = "Unreachable" then 1 else 0 end), '
                    'sum(case when snmpstatus = "Unreachable" then 1 else 0 end) from DEVICES where component=?', [componen])
        return comp.fetchone()


if __name__ == "__main__":

    with open("/home/esadna/KCLAB/myprojectenv/sendmail.txt") as f:
        with open("/home/esadna/KCLAB/myprojectenv/Report.py", "w") as f1:
            for line in f:
                f1.write(line)

    Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", "a")
    Summary = "<html><head><style>table {border-collapse: collapse;} table td{border: 1px solid #ddd; padding: 8px;} table tr:nth-child(even){background-color: #f2f2f2;} table th{pading: 8px; text-align: left;background-color: #4CAF50;color: white;}</style></head><header  align=center><b> Summary </b></header><table align=center class=dataframe><tr><th>Sr.No</th><th>Component</th><th>Total Devices</th><th>Ping Unreachable</th><th>SNMP Unreachable</th>"

    Obj_1 = ping()
    conn = Obj_1.connect_db()
    thread_1 = threading.Thread(target=Obj_1.ping_dnacset2(conn))

    thread_1.start()
    thread_1.join()

    complist = Obj_1.mail(conn)
    print(complist)
    new_dnac_comp = [value[0] for value in complist]
    print(new_dnac_comp)

    obj_2 = devices_db.devices()
    conn = obj_2.connectdb()

    dict_component = {}
    for row in list(new_dnac_comp):
        value = obj_2.get_componentwise_data(conn, row)
        dict_component.update({row: list(value)})
        print(dict_component)

    y = 0
    for key, value in dict_component.items():
        y = y + 1
        print(key, value)
        Summary_Comp = "<tr><td>" + str(y) + "</td><td>" + str(key) + "</td><td>" + str(value[0]) + "</td><td>" + str(value[1]) + "</td><td>" + str(value[3]) + "</td></tr>"
        Summary = Summary + Summary_Comp

    Summary = Summary + "</table><p></p>"
    Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", 'a')
    Topo.write(Summary)
    Topo.close()

    for component in new_dnac_comp:
        compwise = obj_2.get_component_data(conn, str(component))
        y = 0
        Comphtml = "<html><header><b>" + str(component) + "</b></header><table><tr><th>Sr.No</th><th>Device Type</th><th>Real/SIM</th><th>Device Model</th><th>IP Address</th><th>Ping</th><th>SNMP</th></tr>"
        for value in compwise:
            print(value)
            y = y + 1
            WriteTable = "<tr><td>" + str(y) + "</td><td>" + str(value[0]) + "</td><td>" + str(value[1]) + "</td><td>" + str(value[2]) + "</td><td>" + str(value[3]) + "</td><td>" + str(value[4]) + "</td><td>" + str(value[5]) + "</td></tr>"
            Comphtml = Comphtml + WriteTable

        Comphtml = Comphtml + "</table><p></p>"
        Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", 'a')
        Topo.write(Comphtml)
        Topo.close()

    Report = open("/home/esadna/KCLAB/myprojectenv/Report.py", "a")
    Report.write("</html>")
    Report.close()

    with open("/home/esadna/Script/Python/sendmail_2.txt") as f:
        with open("/home/esadna/KCLAB/myprojectenv/Report.py", "a") as f1:
            for line in f:
                f1.write(line)

    os.system('python /home/esadna/Script/Python/Report.py')
    #print(','.join(map(str, chain.from_iterable(value))))


    print("Done")
