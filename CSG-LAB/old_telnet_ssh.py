import telnetlib

class tel_ssh():

    def __init__(self, credlist):
        self.newlist = credlist

    def tel_router(self, user, IP_address):
        print("Credentials: " + str(self.newlist))
        print(user)
        print(IP_address)
        #try:
        tn = telnetlib.Telnet(IP_address)
        tn.read_until(b"Username: ", 5)
        tn.write(self.newlist[0].encode('ascii') + b"\r")
        tn.read_until(b"Password: ", 5)
        tn.write(self.newlist[1].encode('ascii') + b"\r")
        response = tn.read_until(b">", 5)
        tmp = 2
        print(tmp)
        if b"#" in response:
            tn.write(b"config t" + b"\r")
            # tn.write(b"username " + user.encode('ascii') + b" password " + user_pass.encode('ascii') + b"\r")
            tn.write(b"username " + user.encode('ascii') + b" password " + user.encode('ascii') + b"\r")
            tn.write(b"enable password " + user.encode('ascii') + b"\r")
            tn.write(b"snmp-server community " + user.encode('ascii') + b"-ro ro\r")
            tn.write(b"snmp-server community " + user.encode('ascii') + b"-rw rw\r")
            tn.write(b"no username " + self.newlist[0].encode('ascii') + b"\r")
            tn.write(b"\r")
            tn.write(b"end\n")
            tn.write(b"exit\r")
            print(tn.read_all().decode('ascii'))
            tn.close()
            tmp = 0
            print(tmp)
            return tmp
        elif b">" in response:
            tn.write(b"enable" + b"\r")
            tn.read_until(b"Password: ", 5)
            tn.write(self.newlist[2].encode('ascii') + b"\r")
            response2 = tn.read_until(b"#", 5)
            tmp = 1
            print(tmp)
            if b"#" in response2:
                tn.write(b"config t" + b"\r")
                # tn.write(b"username " + user.encode('ascii') + b" password " + user_pass.encode('ascii') + b"\r")
                tn.write(b"username " + user.encode('ascii') + b" password " + user.encode('ascii') + b"\r")
                tn.write(b"enable password " + user.encode('ascii') + b"\r")
                tn.write(b"snmp-server community " + user.encode('ascii') + b"-ro ro\r")
                tn.write(b"snmp-server community " + user.encode('ascii') + b"-rw rw\r")
                tn.write(b"no username " + self.newlist[0].encode('ascii') + b"\r")
                tn.write(b"\r")
                tn.write(b"end\n")
                tn.write(b"exit\r")
                print(tn.read_all().decode('ascii'))
                tn.close()
                tmp = 0
                print(user)
                print(tmp)
                return tmp
            else:
                print("Enable Password is wrong")
                tmp = 1
                return tmp
        else:
            print("Username or Password is wrong")
            tmp = 1
            return tmp


            #print("Device is not accessible through telnet")
            #tmp = 1
            #return tmp

    def tel_wlc(Device_Row, user, IP_Address):

        print("Credentials :" + str(self.newlist))
        print(Password)
        print(user)
        New_User = user.replace('@cisco.com', '')
        print(New_User)
        print(IP_Address)
        user_pass = fun_excel.Find_User_Return_Pass(user)
        print(user_pass)
        tmp = 6

        try:
            netconnect = ConnectHandler(device_type='cisco_wlc', host=IP_Address, username=Username,
                                        password=Password)
            print(netconnect.find_prompt())
            config_command = ['config mgmtuser add ' + user + ' ' + user + '@123 read-write']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community create ' + user + '-rw']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community accessmode rw ' + user + '-rw']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community mode enable ' + user + '-rw']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community create ' + user + '-ro']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community accessmode ro ' + user + '-ro']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community mode enable ' + user + '-ro']
            output = netconnect.send_config_set(config_command)
            print(output)
            tmp = 0
        except ValueError:
            print("Incorrect username or password")
        except Exception:
            print("Device not able to connect via SSH")

        return tmp

    def tel_nexus(Device_Row, user):
        Username = Device_Row[7]
        Password = Device_Row[8]
        IP_Address = Device_Row[6]

        print(Username)
        print(Password)
        print(IP_Address)
        print(user)
        New_User = user.replace('@cisco.com', '')
        print(New_User)
        user_pass = fun_excel.Find_User_Return_Pass(user)
        print(user_pass)
        tmp = 6
        try:
            netconnect = ConnectHandler(device_type='cisco_nxos', host=IP_Address, username=Username,
                                        password=Password)
            print(netconnect.find_prompt())
            config_command = ['config t']
            output = netconnect.send_config_set(config_command)
            config_command = ['username ' + New_User + ' role network-admin password ' + user_pass]
            output = netconnect.send_config_set(config_command)
            print(output)
            tmp = 0

        except socket.timeout:
            print("Incorrect username or password")
            return tmp
        except Exception:
            print("Device not able to connect via SSH")
            return tmp

        return tmp

    def rel_router_switch(self, user, IP_Address):
        print(user)
        tmp = 6
        try:
            tn = telnetlib.Telnet(IP_Address)
            tn.read_until(b"Username: ", 5)

            tn.write(user[0].encode('ascii') + b"\r")
            tn.read_until(b"Password: ", 5)
            tn.write(user[0].encode('ascii') + b"\r")
            response = tn.read_until(b">", 5)
            tmp = 2
            if b"#" in response:
                tn.write(b"write memory" + b"\r")
                tn.write(b"write erase" + b"\r")
                tn.write(b"\r")
                tn.write(b"reload" + b"\r")
                tn.write(b"\r")
                print(tn.read_all().decode('ascii'))
                tn.close()
                tmp = 0
                print(user)
                return tmp
            elif b">" in response:
                tn.write(b"enable" + b"\r")
                tn.read_until(b"Password: ", 5)
                tn.write(user[0].encode('ascii') + b"\r")
                response2 = tn.read_until(b"#", 5)
                tmp = 1

                if b"#" in response2:
                    tn.write(b"write memory" + b"\r")
                    tn.write(b"write erase" + b"\r")
                    tn.write(b"\r")
                    tn.write(b"reload" + b"\r")
                    tn.write(b"\r")
                    print(tn.read_all().decode('ascii'))
                    tn.close()
                    tmp = 0
                    print(user)
                    return tmp
                else:
                    print("Enable Password is wrong")
            else:
                print("Username or Password is wrong")

        except socket.timeout:
            pass
            print("Device is not accessible through telnet")
            tmp = 3

        return tmp

    def rel_wlc(Device_Row):
        IP_Address = Device_Row[6]
        user = Device_Row[10]
        print(user)
        print(IP_Address)
        tmp = 6
        New_User = user.replace('@cisco.com', '')
        print(New_User)
        user_pass = user + "@123"
        print(user_pass)
        try:
            netconnect = ConnectHandler(device_type='cisco_wlc', host=IP_Address, username=user,
                                        password=user_pass)
            print(netconnect.find_prompt())
            config_command = ['config snmp community delete ' + user + '-ro']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config snmp community delete ' + user + '-rw']
            output = netconnect.send_config_set(config_command)
            print(output)
            config_command = ['config mgmtuser delete ' + user]
            output = netconnect.send_config_set(config_command)
            print(output)
            tmp = 0

        except socket.timeout:
            print("Incorrect username or password")

        return tmp

    def rel_nexus(Device_Row, user):
        Username = Device_Row[7]
        Password = Device_Row[8]
        IP_Address = Device_Row[6]

        print(Username)
        print(Password)
        print(IP_Address)
        print(user)
        New_User = user.replace('@cisco.com', '')
        print(New_User)
        user_pass = fun_excel.Find_User_Return_Pass(user)
        print(user_pass)
        tmp = 6
        try:
            netconnect = ConnectHandler(device_type='cisco_nxos', host=IP_Address, username=Username,
                                        password=Password)
            print(netconnect.find_prompt())
            config_command = ['config t']
            output = netconnect.send_config_set(config_command)
            config_command = ['no username ' + New_User]
            output = netconnect.send_config_set(config_command)
            print(output)
            tmp = 0
        except socket.timeout:
            print("Incorrect username or password")
            return tmp
        return tmp

    def adddevice_router_switch(self):
        print(self.newlist)

        try:
            tn = telnetlib.Telnet(self.newlist[0])
            tn.read_until(b"Username: ")
            tn.write(self.newlist[1].encode('ascii') + b"\r")
            tn.read_until(b"Password: ")
            tn.write(self.newlist[2].encode('ascii') + b"\r")
            response = tn.read_until(b">", 5)
            tmp = 2
            if b"#" in response:
                tn.write(b"show inventory | include PID\r")
                tn.write(b"exit\r")
                response3 = (tn.read_all().decode('ascii'))
                tn.close()
                tmp = 0
                print(tmp)
                print(response3)

                file = open('host', 'w')
                file.write(response3.rstrip())
                file.close()
                f = open('host', 'r')
                lines = f.readlines()
                PID = ((lines[1].split(":"))[1].split(","))[0].strip()
                print(PID)
                f.close()
                return tmp, PID
            elif b">" in response:
                tn.write(b"enable" + b"\r")
                tn.read_until(b"Password: ", 5)
                tn.write(self.newlist[3].encode('ascii') + b"\r")
                response2 = tn.read_until(b"#", 5)
                tmp = 1
                print(tmp)
                if b"#" in response2:
                    tn.write(b"show inventory | include Karan\r")
                    tn.write(b"exit\r")
                    response3 = (tn.read_all().decode('ascii'))

                    tn.close()
                    tmp = 0
                    print(tmp)
                    print(response3)

                    file = open('host', 'w')
                    file.write(response3.rstrip())
                    file.close()
                    f = open('host', 'r')
                    lines = f.readlines()
                    PID = ((lines[1].split(":"))[1].split(","))[0].strip()
                    print(PID)
                    f.close()
                    return tmp, PID
                else:
                    print("Password is wrong")
                    tmp = 4
                    return 4
            else:
                print("Password is wrong")
                tmp = 4
                return tmp
        except socket.timeout:
            pass
            print("Device is not accessible through telnet")
            tmp = 3
            return tmp
