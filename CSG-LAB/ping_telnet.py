import sqlite3
import os
import devices_db
import threading
from netmiko import ConnectHandler
from itertools import chain
from pyroute2 import IPRoute

class ping():

    def connect_db(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def addroute(self):
        ip = IPRoute()
        ip.route('add', dst='1.1.0.0',gateway='10.197.124.254')
        ip.close()

    def dnac_telnet_set1(self, con):
        cur = con.cursor()
        print("Telnet check on DNAC topology devices")
        cur.execute('select ipaddress, username, password, enablepassword from DEVICES where topology="DNAC-TOP-1"')
        devicelist = [value for value in cur]
        for value in devicelist:
            print(value)
            try:
                device = ConnectHandler(device_type='cisco_ios_telnet', ip=value[0], username=value[1], password=value[2], secret=value[3])
                device.enable()
                cur.execute('update DEVICES set telnetstatus="Reachable" where ipaddress=? and topology="DNAC-TOP-1"', [value[0]])
                con.commit()
                print("Device Connected")
                device.disconnect()
            except Exception as e:
                print(e)
                cur.execute('update DEVICES set telnetstatus="Unreachable" where ipaddress=? and topology="DNAC-TOP-1"', [value[0]])
                con.commit()

    def dnac_telnet_set2(self, con):
        cur = con.cursor()
        print("Telnet check on DNAC topology devices")
        cur.execute('select ipaddress, username, password, enablepassword from DEVICES where topology="DNAC-TOP-2"')
        devicelist = [value for value in cur]
        for value in devicelist:
            print(value)
            try:
                device = ConnectHandler(device_type='cisco_ios_telnet', ip=value[0], username=value[1], password=value[2], secret=value[3])
                device.enable()
                cur.execute('update DEVICES set telnetstatus="Reachable" where ipaddress=? and topology="DNAC-TOP-2"', [value[0]])
                con.commit()
                print("Device Connected")
                device.disconnect()
            except Exception as e:
                print(e)
                cur.execute('update DEVICES set telnetstatus="Unreachable" where ipaddress=? and topology="DNAC-TOP-2"', [value[0]])
                con.commit()

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
        cur.execute('select ipaddress, snmpread from DEVICES where topology="DNAC-TOP-1"')
        iplist = [row for row in cur]
        #print(iplist)
        for ip in iplist:
            response = os.system("ping -c 1 " + str(ip[0]))
            response_2 = os.system("snmpwalk -v2c -c " + str(ip[1]) + " " + str(ip[0]) + " 1.3.6.1.2.1.1.1")
            print(response_2)

            if response == 0:
                print("Reachability of IP address " + ip[0] + ": " + "Reachable")
                cur.execute('update DEVICES set reachability="Reachable" where ipaddress=? and topology="DNAC-TOP-1"', [ip[0]])
                con.commit()
            else:
                print("Reachability of IP address " + ip[0] + ": " + "Unreachable")
                cur.execute('update DEVICES set reachability="Unreachable" where ipaddress=? and topology="DNAC-TOP-1"', [ip[0]])
                con.commit()
            if response_2 == 0:
                print("Reachability of IP address " + ip[0] + ": " + "Reachable")
                cur.execute('update DEVICES set snmpstatus="Reachable" where ipaddress=? and topology="DNAC-TOP-1"', [ip[0]])
                con.commit()
            else:
                print("Reachability of IP address " + ip[0] + ": " + "Unreachable")
                cur.execute('update DEVICES set snmpstatus="Unreachable" where ipaddress=? and topology="DNAC-TOP-1"', [ip[0]])
                con.commit()


    def ping_dnacset2(self, con):
        cur = con.cursor()
        print("Ping reachability check on DNAC topology devices")
        cur.execute('select ipaddress, snmpread from DEVICES where topology="DNAC-TOP-2"')
        iplist = [row for row in cur]
        print(iplist)
        for ip in iplist:
            response = os.system("ping -c 1 " + str(ip[0]))
            response_2 = os.system("snmpwalk -v2c -c " + str(ip[1]) + " " + str(ip[0]) + " 1.3.6.1.2.1.1.1")
            print(response_2)

            if response == 0:
                print("Reachability of IP address " + ip[0] + ": " + "Reachable")
                cur.execute('update DEVICES set reachability="Reachable" where ipaddress=? and topology="DNAC-TOP-2"',
                            [ip[0]])
                con.commit()
            else:
                print("Reachability of IP address " + ip[0] + ": " + "Unreachable")
                cur.execute('update DEVICES set reachability="Unreachable" where ipaddress=? and topology="DNAC-TOP-2"',
                            [ip[0]])
                con.commit()
            if response_2 == 0:
                print("Reachability of IP address " + ip[0] + ": " + "Reachable")
                cur.execute('update DEVICES set snmpstatus="Reachable" where ipaddress=? and topology="DNAC-TOP-2"',
                            [ip[0]])
                con.commit()
            else:
                print("Reachability of IP address " + ip[0] + ": " + "Unreachable")
                cur.execute('update DEVICES set snmpstatus="Unreachable" where ipaddress=? and topology="DNAC-TOP-2"',
                            [ip[0]])
                con.commit()

    def get_dnac_data_1(self, con):
        cur = con.cursor()
        print("Fetching DNAC topology data")
        dnac=cur.execute('select count(*), count(DISTINCT component),'
                         'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                         'sum(case when snmpstatus = "Unreachable" then 1 else 0 end), '
                         'sum(case when telnetstatus = "Unreachable" then 1 else 0 end) '
                         'from DEVICES where topology="DNAC-TOP-1"')
        return dnac.fetchone()

    def get_dnac_data_2(self, con):
        cur = con.cursor()
        print("Fetching DNAC topology data")
        dnac=cur.execute('select count(*), count(DISTINCT component),'
                         'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                         'sum(case when snmpstatus = "Unreachable" then 1 else 0 end), '
                         'sum(case when telnetstatus = "Unreachable" then 1 else 0 end) '
                         'from DEVICES where topology="DNAC-TOP-2"')
        return dnac.fetchone()

    def mail(self, con):
        cur = con.cursor()
        cur.execute('select distinct component  from DEVICES where topology="DNAC-TOP-2"')
        return cur

    def get_component_dataset(self, con, componen):
        cur = con.cursor()
        print("Fetching Component wise data" + str(componen))
        comp = cur.execute('select count (ipaddress), '
                           'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                    'sum(case when telnetstatus = "Unreachable" then 1 else 0 end), '
                    'sum(case when snmpstatus = "Unreachable" then 1 else 0 end) from DEVICES where component=? and topology="DNAC-TOP-1"', [componen])
        compdata = comp.fetchone()


        comp = cur.execute('select count (ipaddress), '
                   'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                   'sum(case when telnetstatus = "Unreachable" then 1 else 0 end), '
                   'sum(case when snmpstatus = "Unreachable" then 1 else 0 end) from DEVICES where component=? and topology="DNAC-TOP-2"',
                   [componen])
        compdata = compdata + comp.fetchone()
        return compdata

    def get_component_data_set1(self, con, component):
        cur = con.cursor()
        print("Fetching DNAC Component: " + component +"data")
        cur.execute('select devicetype,rvsv, ipaddress, productid, reachability, snmpstatus, telnetstatus from DEVICES where component=? AND topology="DNAC-TOP-1"', [component])
        return list(cur)

    def get_component_data_set2(self, con, component):
        cur = con.cursor()
        print("Fetching DNAC Component: " + component +"data")
        cur.execute('select devicetype,rvsv, ipaddress, productid, reachability, snmpstatus, telnetstatus from DEVICES where component=? AND topology="DNAC-TOP-2"', [component])
        return list(cur)

if __name__ == "__main__":

    with open("/home/esadna/KCLAB/myprojectenv/sendmail.txt") as f:
        with open("/home/esadna/KCLAB/myprojectenv/Report.py", "w") as f1:
            for line in f:
                f1.write(line)


    Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", "a")
    Summary ="<html><<head><style>table{align:left;border-collapse: collapse;border: 2px solid black;}.table, th, td{width: 100px;font-size: 16px;text-align: center;height: 3vh;border: 1px solid #ddd;}table tr:nth-child(even){background-color: #f2f2f2;}table th{pading: 8px;text-align:center;background-color: #4CAF50;color: white;border: 1px solid black;}</style></head><header><b>DNAC Device Summary</b></header><table class=dataframe><tr><th>DNAC</th><th>Total</th><th>Ping Fail</th><th>SNMP Fail</th><th>Telnet Fail</th></tr>"

    obj_1 = ping()

    conn = obj_1.connect_db()

    '''sudoPassword = 'cisco123'
    command = 'route del -net 35.1.1.0/24'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 48.0.0.0/8'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 175.175.0.0/16'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    command = 'route add -net 175.175.0.0/16 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 48.0.0.0/8 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 35.1.1.0/24 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    
    thread_1 = threading.Thread(target=obj_1.ping_dnacset1(conn))
    thread_2 = threading.Thread(target=obj_1.dnac_telnet_set1(conn))

    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()


    command = 'route del -net 35.1.1.0/24'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 48.0.0.0/8'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 175.175.0.0/16'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    command = 'route add -net 175.175.0.0/16 gw 10.197.124.254'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 48.0.0.0/8 gw 10.197.124.254'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 35.1.1.0/24 gw 10.197.124.254'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    thread_1 = threading.Thread(target=obj_1.ping_dnacset2(conn))
    thread_2 = threading.Thread(target=obj_1.dnac_telnet_set2(conn))

    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()

    command = 'route del -net 35.1.1.0/24'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 48.0.0.0/8'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route del -net 175.175.0.0/16'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    command = 'route add -net 175.175.0.0/16 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 48.0.0.0/8 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'route add -net 35.1.1.0/24 gw 175.175.40.1'
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))'''


    complist = obj_1.mail(conn)

    """DNAC Device Summary"""
    dnacset1 = obj_1.get_dnac_data_1(conn)
    dnacset2 = obj_1.get_dnac_data_2(conn)
    print(complist)
    print(dnacset1)
    print(dnacset2)

    Summary_Comp = "<tr><td> DNAC-SET-1</td><td>" + str(dnacset1[0]) + "</td><td>" + str(dnacset1[2]) + "</td><td>" + str(dnacset1[3]) + "</td><td>" + str(
        dnacset1[4]) + "</td></tr>"
    Summary = Summary + Summary_Comp
    Summary_Comp = "<tr><td> DNAC-SET-2</td><td>" + str(dnacset2[0]) + "</td><td>" + str(dnacset2[2]) + "</td><td>" + str(dnacset2[3]) + "</td><td>" + str(
        dnacset2[4]) + "</td></tr></table><br>"
    Summary = Summary + Summary_Comp

    """Component Summary"""
    Summary_Comp = "<header><b>Component Summary</b></header><table class=dataframe><tr><th>Sr.No</th><th>Component</th><th colspan=4>DNAC-SET-1</th><th colspan=4>DNAC-SET-2</th></tr><tr><th></th><th></th><th>Total Devices</th><th>Ping</th><th>SNMP</th><th>Telnet</th><th>Total Devices</th><th>Ping</th><th>SNMP</th><th>Telnet</th></tr>"
    Summary = Summary + Summary_Comp

    new_dnac_comp = [value[0] for value in complist]
    print(new_dnac_comp)

    obj_2 = ping()
    conn = obj_2.connect_db()

    dict_component = {}
    for row in list(new_dnac_comp):
        value = obj_2.get_component_dataset(conn, row)
        dict_component.update({row: list(value)})
        print(dict_component)

    y = 0
    for key, value in dict_component.items():
        y = y + 1
        print(key, value)
        Summary_Comp = "<tr><td>" + str(y) + "</td><td>" + str(key) + "</td><td>" + str(value[0]) + "</td><td>" + str(value[1]) + "</td><td>" + str(value[3]) + "</td><td>" + str(value[2]) + "</td><td>" + str(value[4]) + "</td><td>" + str(value[5]) + "</td><td>" + str(value[7]) + "</td><td>" + str(value[6]) + "</td></tr>"
        Summary = Summary + Summary_Comp

    Summary = Summary + "</table><p></p>"
    Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", 'a')
    Topo.write(Summary)
    Topo.close()

    for component in new_dnac_comp:
        compwise = obj_2.get_component_data_set1(conn, str(component))
        compwise2 = obj_2.get_component_data_set2(conn, str(component))
        y = 0
        Comphtml ="<header><b>" + str(component) + "</b></header><table><tr><th></th><th></th><th></th><th></th><th colspan=3>DNAC SET-1</th><th colspan=3>DNAC SET-2</th></tr><tr><th>Sr.No</th><th>Device Type</th><th>Real/SIM</th><th>IP Address</th><th>Ping</th><th>SNMP</th><th>Telnet</th><th>Ping</th><th>SNMP</th><th>Telnet</th></tr>"

        for value in compwise:
            for value2 in compwise2:
                if value[2] == value2[2]:
                    print(value)
                    y = y + 1
                    WriteTable = "<tr><td>" + str(y) + "</td><td>" + str(value[0]) + "</td><td>" + str(value[1]) + "</td><td>" + str(value[2]) + "</td><td>" + str(value[4]) + "</td><td>" + str(value[5]) + "</td><td>" + str(value[6]) + "</td><td>" + str(value2[4]) + "</td><td>" + str(value2[5]) + "</td><td>" + str(value2[6]) + "</td></tr>"
                    Comphtml = Comphtml + WriteTable
                    break
                else:
                    print("IP Not matching")

        Comphtml = Comphtml + "</table><p></p>"
        Topo = open("/home/esadna/KCLAB/myprojectenv/Report.py", 'a')
        Topo.write(Comphtml)
        Topo.close()

    Report = open("/home/esadna/KCLAB/myprojectenv/Report.py", "a")
    Report.write("</html>")
    Report.close()

    with open("/home/esadna/KCLAB/myprojectenv/sendmail_2.txt") as f:
        with open("/home/esadna/KCLAB/myprojectenv/Report.py", "a") as f1:
            for line in f:
                f1.write(line)

    os.system('python /home/esadna/KCLAB/myprojectenv/Report.py')
    #print(','.join(map(str, chain.from_iterable(value))))


    print("Done")
