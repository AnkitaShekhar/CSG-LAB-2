
from netmiko import ConnectHandler
import class_database
import devices_db
from netaddr import IPAddress,IPNetwork


class tel_ssh():

    def tel_router(self,ip, user):
        print(ip)
        print(user)
        mailid = user + "@cisco.com"
        print(mailid)
        #iplist = ["10.104.240.68", "Smart", "Smart123", "Smart123", "karachan", "cisco123"]

        """Fetching User Credentials from CREDENTIALS DB"""
        obj_cred = class_database.getcredentials()
        con = obj_cred.connectdb()
        cur = con.cursor()

        cur.execute('select * from CREDENTIALS where mail=?', [mailid])
        credentials = list(cur)
        print(credentials[0][2], credentials[0][3])

        """Fetching Device Credentials from DEVICES DB"""
        obj_device = devices_db.devices()
        conn = obj_device.connectdb()
        cur = conn.cursor()
        cur.execute('select username, password, enablepassword, ipaddress from DEVICES where ipaddress=?', [ip])
        devcredentials = list(cur)
        print(devcredentials)
        iplist=[ip, devcredentials[0][0], devcredentials[0][1], devcredentials[0][2], user, credentials[0][3]]
        print(iplist)


        if mailid in credentials[0] and ip in devcredentials[0]:
            response = 0
            try:
                device = ConnectHandler(device_type='cisco_ios_telnet', ip=iplist[0] ,username=iplist[1], password=iplist[2], secret=iplist[3])
                print("Device Connected")
                output0 = device.find_prompt()
                print(output0)
                cmd1 = "username " + iplist[4] + " privilege 15 password " + iplist[5]
                cmd2 = "enable secret " + iplist[5]
                cmd3 = "snmp-server community " + iplist[4] + "-ro ro"
                cmd4 = "snmp-server community " + iplist[4] + "-rw rw"
                cmd5 = "no username " + iplist[1]
                cmd0 = device.send_config_set([cmd1, cmd2, cmd3, cmd4, cmd5])
                print(cmd0)
                device.disconnect()
            except Exception as e:
                print(e)
                response = 1
        else:
            response = 1
        return response

    def rel_router_switch(self, ip, user):

        print(ip)
        print(user)
        mailid = user + "@cisco.com"
        print(mailid)

        """Fetching User Credentials from CREDENTIALS DB"""
        obj_cred = class_database.getcredentials()
        con = obj_cred.connectdb()
        cur = con.cursor()

        cur.execute('select * from CREDENTIALS where mail=?', [mailid])
        credentials = list(cur)
        print(credentials[0][2], credentials[0][3])

        """Fetching Device Credentials from DEVICES DB"""
        obj_device = devices_db.devices()
        conn = obj_device.connectdb()
        cur = conn.cursor()

        cur.execute('select username, password, enablepassword, ipaddress from DEVICES where ipaddress=?', [ip])
        devicredentials = list(cur)
        print(devicredentials)
        iplist = [ip, devicredentials[0][0], devicredentials[0][1], devicredentials[0][2], user, credentials[0][3]]
        print(iplist)

        if mailid in credentials[0] and ip in devicredentials[0]:
            response = 0
            try:
                device = ConnectHandler(device_type='cisco_ios_telnet', ip=iplist[0] ,username=iplist[4], password=iplist[5], secret=iplist[5])
                print("Device Connected")
                output0 = device.find_prompt()
                print(output0)
                cmd1 = "username " + iplist[1] + " privilege 15 password " + iplist[2]
                cmd2 = "enable secret " + iplist[3]
                cmd3 = "no snmp-server community " + iplist[4] + "-ro ro"
                cmd4 = "no snmp-server community " + iplist[4] + "-rw rw"
                cmd5 = "no username " + iplist[4]
                cmd0 = device.send_config_set([cmd1, cmd2, cmd3, cmd4, cmd5])
                print(cmd0)
                device.disconnect()
            except Exception as e:
                print(e)
                response = 1
        else:
            response = 1
        return response

        return 0

    def tel_switch(self, ip, user):
        print(ip)
        print(user)
        mailid = user + "@cisco.com"
        print(mailid)
        # iplist = ["10.104.240.68", "Smart", "Smart123", "Smart123", "karachan", "cisco123"]

        """Fetching User Credentials from CREDENTIALS DB"""
        obj_cred = class_database.getcredentials()
        con = obj_cred.connectdb()
        cur = con.cursor()

        cur.execute('select * from CREDENTIALS where mail=?', [mailid])
        credentials = list(cur)
        print(credentials[0][2], credentials[0][3])

        """Fetching Device Credentials from DEVICES DB"""
        obj_device = devices_db.devices()
        conn = obj_device.connectdb()
        cur = conn.cursor()
        cur.execute('select username, password, enablepassword, ipaddress from DEVICES where ipaddress=?', [ip])
        devcredentials = list(cur)
        print(devcredentials)
        iplist = [ip, devcredentials[0][0], devcredentials[0][1], devcredentials[0][2], user, credentials[0][3]]
        print(iplist)

        """Connecting with device"""
        if mailid in credentials[0] and ip in devcredentials[0]:
            response = 0
            try:
                device = ConnectHandler(device_type='cisco_ios_telnet', ip=iplist[0], username=iplist[1],
                                        password=iplist[2])
                print("Device Connected")
                output0 = device.find_prompt()
                print(output0)
                cmd1 = "username " + iplist[4] + " password " + iplist[5]
                cmd2 = "enable secret " + iplist[5]
                cmd3 = "snmp-server community " + iplist[4] + "-ro ro"
                cmd4 = "snmp-server community " + iplist[4] + "-rw rw"
                cmd5 = "no username " + iplist[1]
                cmd0 = device.send_config_set([cmd1, cmd2, cmd3, cmd4, cmd5])
                print(cmd0)
                device.disconnect()
            except Exception as e:
                print(e)
                response = 1
        else:
            response = 1
        return response

    def tel_nexus(self):
        return 0

    def tel_wlc(self):
        return 0

"""obj_telnet = tel_ssh()

response = obj_telnet.tel_router("10.104.240.68", "karachan")
print(response)"""
