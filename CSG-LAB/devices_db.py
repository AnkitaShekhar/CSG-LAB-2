import sqlite3

class devices():

    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def getipdata(self, con, ipaddress):
        cur = con.cursor()
        print("Fetching data of " + ipaddress + " from db")
        ipdata = cur.execute('select * from DEVICES where ipaddress =?', [ipaddress])
        return ipdata.fetchone()

    def get_device_credentials(self, con, ipaddress):
        cur = con.cursor()
        print("Fetching credentials of " + ipaddress[0] + " from db")
        credentials = cur.execute('select username, password, enablepassword from DEVICES where ipaddress =?', [ipaddress[0]])
        #print(credentials.fetchone())
        return credentials.fetchone()

    def get_user(self, con, ipaddress):
        cur = con.cursor()
        print("Fetching User of " + ipaddress + " from db")
        user = cur.execute('select user from DEVICES where ipaddress =?', [ipaddress])
        return user

    def get_dashboard_data(self, con, device):
        cur = con.cursor()
        print("Fetching device data for daashboard")
        router = cur.execute('select count(*), sum(case when status="Reserved" then 1 else 0 end), '
                             'sum(case when status is NULL then 1 else 0 end), '
                             'sum(case when reachability = "Unreachable" then 1 else 0 end) '
                             'from DEVICES where devicetype=? AND component="LAB"', [device])
        return router.fetchone()

    def get_router_data(self, con):
        cur = con.cursor()
        print("Fetching LAB Router data")
        cur.execute('select deviceseries, productid, ipaddress, status, user, releasedate, usertextstatus, assigntag, extendtag, releasetag, reachability from DEVICES where component="LAB" AND devicetype="Router"')
        return cur

    def get_switch_data(self, con):
        cur = con.cursor()
        print("Fetching LAB Switch data")
        cur.execute('select deviceseries, productid, ipaddress, status, user, releasedate, usertextstatus, assigntag, extendtag, releasetag, reachability from DEVICES where component="LAB" AND devicetype="Switch"')
        return cur

    def get_wlc_data(self, con):
        cur = con.cursor()
        print("Fetching LAB WLC data")
        cur.execute('select deviceseries, productid, ipaddress, status, user, releasedate, usertextstatus, assigntag, extendtag, releasetag, reachability from DEVICES where component="LAB" AND devicetype="WLC"')
        return cur

    def get_nexus_data(self, con):
        cur = con.cursor()
        print("Fetching LAB Nexus data")
        cur.execute('select deviceseries, productid, ipaddress, status, user, releasedate, usertextstatus, assigntag, extendtag, releasetag, reachability from DEVICES where component="LAB" AND devicetype="Nexus"')
        return cur

    def get_dnac_component(self, con):
        cur = con.cursor()
        print("Fetching DNAC Components")
        cur.execute('select DISTINCT component from DEVICES where topology="DNAC-TOP-1"')
        return cur

    def get_componentwise_data(self, con, componen):
        cur = con.cursor()
        print("Fetching Component wise data" + str(componen))
        comp = cur.execute('select count (ipaddress), '
                           'sum(case when reachability = "Unreachable" then 1 else 0 end), '
                    'sum(case when telnetstatus = "Unreachable" then 1 else 0 end), '
                    'sum(case when snmpstatus = "Unreachable" then 1 else 0 end) from DEVICES where component=? AND topology="DNAC-TOP-1"', [componen])
        return comp.fetchone()

    def get_credentials(self, con, ip):
        cur = con.cursor()
        print("Fetching Credentials from database")
        credentials = cur.execute('select username, password, enablepassword from DEVICES where ipaddress=?', [ip])
        return credentials.fetchone()

    def get_dnac_data(self, con):
        cur = con.cursor()
        print("Fetching DNAC topology data")
        dnac=cur.execute('select count(*), count(DISTINCT component),'
                         'sum(case when rvsv = "Real" then 1 else 0 end), '
                         'sum(case when rvsv = "VIRL" then 1 else 0 end), '
                         'sum(case when rvsv = "Sapro" then 1 else 0 end), '
                         'sum(case when rvsv = "Virtual" then 1 else 0 end)'
                         'from DEVICES where groups="DNAC"')
        return dnac.fetchone()

    def get_dnac_data_1(self, con):
        cur = con.cursor()
        print("Fetching DNAC topology data")
        dnac=cur.execute('select count(*), count(DISTINCT component),'
                         'sum(case when rvsv = "Real" then 1 else 0 end), '
                         'sum(case when rvsv = "VIRL" then 1 else 0 end), '
                         'sum(case when rvsv = "Sapro" then 1 else 0 end), '
                         'sum(case when rvsv = "Virtual" then 1 else 0 end)'
                         'from DEVICES where topology="DNAC-TOP-1"')
        return dnac.fetchone()

    def get_dnac_data_2(self, con):
        cur = con.cursor()
        print("Fetching DNAC topology data")
        dnac=cur.execute('select count(*), count(DISTINCT component),'
                         'sum(case when rvsv = "Real" then 1 else 0 end), '
                         'sum(case when rvsv = "VIRL" then 1 else 0 end), '
                         'sum(case when rvsv = "Sapro" then 1 else 0 end), '
                         'sum(case when rvsv = "Virtual" then 1 else 0 end)'
                         'from DEVICES where topology="DNAC-TOP-2"')
        return dnac.fetchone()

    def get_component_data(self, con, component):
        cur = con.cursor()
        print("Fetching DNAC Component: " + component +"data")
        cur.execute('select devicetype, productid, ipaddress, rvsv, reachability, telnetstatus, snmpstatus from DEVICES where component=? AND topology="DNAC-TOP-1"', [component])
        return list(cur)


    def get_set_data(self, con, component):
        cur = con.cursor()
        print("Fetching DNAC data: " + component)
        if "set1" in component and "total" in component:
            cur.execute('select component, devicetype, ipaddress, reachability from DEVICES where topology="DNAC-TOP-1"')
            return list(cur)

        elif "set1" in component:
            type= component.split("-")[1]
            print(type)
            cur.execute('select component, devicetype, ipaddress, reachability from DEVICES where topology="DNAC-TOP-1" AND rvsv=?',[type])
            return list(cur)

        elif "set2" in component and "total" in component:
            cur.execute('select component, devicetype, ipaddress, reachability from DEVICES where topology="DNAC-TOP-2"')
            return list(cur)

        elif "set2" in component:
            type = component.split("-")[1]
            print(type)
            cur.execute('select component, devicetype, ipaddress, reachability from DEVICES where topology="DNAC-TOP-2" AND rvsv=?',[type])
            return list(cur)

    def getdnacset1data(self, con, component):
        print("Fetching DNAC Set data")
        cur = con.cursor()
        dnac = cur.execute('select count(*),'
                           'sum(case when rvsv = "Real" then 1 else 0 end), '
                           'sum(case when rvsv = "VIRL" then 1 else 0 end), '
                           'sum(case when rvsv = "Sapro" then 1 else 0 end), '
                           'sum(case when rvsv = "Virtual" then 1 else 0 end)'
                           'from DEVICES where topology="DNAC-TOP-1" AND component=?', [component])
        return dnac

    def getdnacset2data(self, con, component):
        print("Fetching DNAC Set data")
        cur = con.cursor()
        dnac = cur.execute('select count(*),'
                           'sum(case when rvsv = "Real" then 1 else 0 end), '
                           'sum(case when rvsv = "VIRL" then 1 else 0 end), '
                           'sum(case when rvsv = "Sapro" then 1 else 0 end), '
                           'sum(case when rvsv = "Virtual" then 1 else 0 end)'
                           'from DEVICES where topology="DNAC-TOP-2" AND component=?', [component])
        return dnac