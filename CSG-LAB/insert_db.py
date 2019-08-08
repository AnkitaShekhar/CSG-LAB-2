import sqlite3
import subprocess

class insert():

    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def insert_device(self, con, addlist, component):
        cur = con.cursor()
        print("Adding device into database")
        cur.execute('select * from DEVICES where ipaddress=? AND topology=?', [addlist[0], addlist[1]])
        if cur.fetchone():
            print("Device already present in db")
            return False
        else:
            print("Device successfully added in database")
            if component == "LAB":
                cur.execute('Insert into DEVICES (ipaddress, topology, deviceseries, productid, username, password, enablepassword, '
                            'snmpread, snmpwrite, devicetype, groups, rvsv, status) '
                            'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        [addlist[0], addlist[1], addlist[2], addlist[3],addlist[4], addlist[5], addlist[6], addlist[7],
                         addlist[8], addlist[9],addlist[10],addlist[11],"Free"])
            elif component == "DNAC-TOP-1" or component == "DNAC-TOP-2":
                cur.execute('Insert into DEVICES (ipaddress, topology, deviceseries, productid, username, password, enablepassword, '
                            'snmpread, snmpwrite, devicetype, product, groups, component, rvsv) '
                            'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [addlist[0], addlist[1], addlist[2], addlist[3], addlist[4], addlist[5], addlist[6], addlist[7],
                     addlist[8], addlist[9], addlist[10], addlist[11], addlist[12], addlist[13]])
            con.commit()
            return True

    def delete_device(self, con, ipaddress):
        cur = con.cursor()
        print("Deleting device from database")
        cur.execute('select * from DEVICES where ipaddress=?', [ipaddress])
        if cur.fetchone():
            cur.execute('DELETE from DEVICES where ipaddress=?', [ipaddress])
            con.commit()
            return True
        else:
            return False

    def upd_assign_device(self, con, device_data):
        cur = con.cursor()
        print("Updating Assigned device data into database")
        cur.execute('update DEVICES set user=?, status=?, releasedate=?, assigndate=?, assigntag="disabled", releasetag="", extendtag="" where ipaddress=?',
                    [device_data[1],
                     "Reserved",
                     device_data[3],
                     device_data[2],
                     device_data[0]])
        con.commit()

    def upd_release_device(self, con, ipaddress):
        cur = con.cursor()
        print("Updating Released device data into database")
        cur.execute('update DEVICES set user="None", status="Free", releasedate="", assigndate="", assigntag="", releasetag="disabled", extendtag="disabled" where ipaddress=?',
                    [ipaddress])
        con.commit()

    def upd_extend_device(self, con, ipaddress, extenddate):
        cur = con.cursor()
        print("Updating Assigned device data into database")
        cur.execute('update DEVICES set releasedate=?, assigntag="disabled", releasetag="", extendtag="" where ipaddress=?',
                    [extenddate,
                     ipaddress])
        con.commit()


    def Send_Mail_Assign_Device(self, row_value):
        print(row_value)
        print("Sending Mail to " + row_value[15])
        mail = open("Mail_Content.txt", "w")
        mail.write("Subject: Device Assignment\n")
        mail.write("\n")
        mail.write("Hi, \n\nDevice" + "\n")
        mail.write("*********************" + "\n")
        mail.write("IP Address: " + row_value[9] + "\n")
        mail.write("PID: " + ": " + row_value[8] + "\n")
        if row_value[7] == "WLC":
            mail.write("Credentials: " + row_value[10] + "/" + row_value[10] + "@123\n")
        else:
            mail.write("Credentials: " + row_value[15] + "/" + row_value[15] + "/" + row_value[15] + "\n")

        mail.write("SNMP: " + row_value[15] + "-ro/" + row_value[15] + "-rw" + "\n")
        mail.write("Release Date: " + "5.00 PM, " + row_value[17] + "\n" + "\n")
        mail.write("Thanks,\npi-lab-support-blr")
        mail.close()

        mail_2 = open("Mail.sh", "w")
        mail_2.write("#!/bin/sh" + "\n")
        mail_2.write("sendmail -f pi-lab-support-blr@cisco.com -t " + row_value[
            15] + "@cisco.com karachan@cisco.com < Mail_Content.txt")
        mail_2.close()
        subprocess.call('./Mail.sh')

    def Send_Mail_Extend_Device(self, row_value):
        print(row_value)
        print("Sending Mail to " + row_value[12])
        mail = open("Mail_Content.txt", "w")
        mail.write("Subject: Device Extended\n")
        mail.write("\n")
        mail.write("Hi, \n\nDevice" + "\n")
        mail.write("*********************" + "\n")
        mail.write("IP Address: " + row_value[6] + "\n")
        mail.write(row_value[3] + ": " + row_value[2] + "\n")
        mail.write("New Release Date: " + "5.00 PM, " + row_value[12] + "\n" + "\n")
        mail.write("Thanks,\npi-lab-support-blr")
        status = mail.close()

        mail_2 = open("Mail.sh", "w")
        mail_2.write("#!/bin/sh" + "\n")
        mail_2.write("sendmail -f pi-lab-support-blr@cisco.com -t " + row_value[
            10] + "@cisco.com karachan@cisco.com < Mail_Content.txt")
        mail_2.close()
        subprocess.call('./Mail.sh')

    def Send_Mail_Release_Device(self, row_value):
        print(row_value)
        print("Sending Mail to " + row_value[15])
        mail = open("Mail_Content.txt", "w")
        mail.write("Subject: Device Released\n")
        mail.write("\n")
        mail.write("Hi, \n\nDevice" + "\n")
        mail.write("*********************" + "\n")
        mail.write("IP Address: " + row_value[9] + "\n")
        mail.write("PID: " + ": " + row_value[8] + "\n")
        mail.write("Release Date: " + "5.00 PM, " + row_value[17] + "\n" + "\n")
        mail.write("Thanks,\npi-lab-support-blr")
        mail.close()

        mail_2 = open("Mail.sh", "w")
        mail_2.write("#!/bin/sh" + "\n")
        mail_2.write("sendmail -f pi-lab-support-blr@cisco.com -t " + row_value[
            15] + "@cisco.com nanramas@cisco.com < Mail_Content.txt")
        mail_2.close()
        subprocess.call('./Mail.sh')

    def Send_Mail():
        mail = open("Mail.sh", "w")
        mail.write("#!/bin/sh" + "\n")
        mail.write("/usr/sbin/sendmail -f pi-lab-support-blr@cisco.com -t " + row_value[
            10] + "@cisco.com karachan@cisco.com karachan@cisco.com < Reachability.txt")
        mail.close()
        subprocess.call('./Mail.sh')
