import sqlite3
import json
import datetime
import xlrd
con = sqlite3.connect("KCLAB.db")
cur = con.cursor()
#cur.execute('select component,ipaddress FROM DEVICES where rvsv="VIRL" order by component asc')
#cur.execute(' select count(component) FROM DEVICES where component="Network Programmer"')
#cur.execute(' select count(component),   DEVICES where component="Network Programmer"')
#cur.execute('select * from DEVICES where component="Network Programmer"')
#cur.execute(' select count(component) from  DEVICES where component="Network Programmer"')
#cur.execute(' select count(component) from  DEVICES where component="Network Programmer" & reachability="Reachable"')
#cur.execute(' select count(component) from  DEVICES where component="Network Programmer" & telnetstatus="None"')

#cur.execute('''insert into CREDENTIALS (name, lastname, mail, password) VALUES('Karan', 'Chandrawanshi', 'karachan@cisco.com', 'PiTest123')''')
#name = "Karan"
#abc = cur.execute('select * from CREDENTIALS')

#cur.execute('select * from DEVICES where assigntag="enable"')
#cur.execute("Insert into DEVICES (usertextstatus) VALUES(?)",["enable"])
#cur.execute('update DEVICES set assigntag=null, extendtag="disabled", releasetag="disabled" where component="LAB"' )
#abc = cur.execute('select username, password, enablepassword from DEVICES where ipaddress ="175.175.179.101"')

#cur.execute('select * from DEVICES where ipaddress="10.106.190.85"')
#cur.execute('update DEVICES set reachability="Unreachable" where ipaddress="10.106.190.85" ')

#cur.execute('select count(topology), sum(case when component = "Template Programmer" then 1 else 0 end) from DEVICES where topology ="DNAC-TOP-1"')
#cur.execute('select sum(case when component = "LAB" then 1 else 0 end), sum(case when component =  then 1 else 0 end) from DEVICES where topology ="DNAC-TOP-1"')

#Dashboard
#cur.execute('select count(*), sum(case when status="Reserved" then 1 else 0 end), sum(case when status is NULL then 1 else 0 end), sum(case when reachability = "Unreachable" then 1 else 0 end) from DEVICES where devicetype="Router" AND component="LAB"')
#cur.execute('select deviceseries, productid, ipaddress, status status, user,releasedate from DEVICES where component="LAB" AND devicetype="Router"')
#cur.execute('select count(DISTINCT rvsv) from DEVICES where topology="DNAC-TOP-1"')

#cur.execute('select count(*), count(DISTINCT component), sum(case when rvsv = "Real" then 1 else 0 end), sum(case when rvsv = "VIRL" then 1 else 0 end), sum(case when reachability = "Unreachable" then 1 else 0 end) from DEVICES where topology="DNAC-TOP-1"')
#cur.execute('select * from DEVICES where ipaddress LIKE')
#cur.execute('ALTER TABLE DEVICES ADD column releasetag TEXT')
#cur.execute('select devicetype, productid, ipaddress, reachability, telnetstatus, snmpstatus from DEVICES where component="Licensing"')
#today = datetime.datetime.today().strftime("%d-%m-%Y")
#R_day = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
#cur.execute('update DEVICES set groups="DNAC" where topology="DNAC-TOP-1"')
#ip = "10.104.62.179"
#cur.execute('update DEVICES set reachability="Reachable" where ipaddress=?', [ip])
#cur.execute('insert into DEVICES (groups, topology, component, rvsv, deviceseries, devicetype, productid, ipaddress, username, password, enablepassword, snmpread, snmpwrite)'
#            'select "DNAC", "DNAC-TOP-2", component, rvsv, deviceseries, devicetype, productid, ipaddress, username, password, enablepassword, snmpread, snmpwrite from DEVICES '
#           'where component="SWIM" and ipaddress="175.175.195.8"')

cur.execute('delete from CREDENTIALS where name="Nandha"')
con.commit()

#cur.execute('select distinct * into #tmp from DEVICE where topology="DNAC-TOP-1" & rvsv="Sapro')
#DELETE FROM "main"."DEVICES" WHERE _rowid_ IN ('884', '883', '882', '881', '880', '879', '878', '877', '876', '875', '874', '873', '872', '871', '870', '869', '868', '867', '866', '865', '864', '863', '862', '861', '860', '859', '858', '857', '856', '855', '854', '853', '852', '851', '850', '849', '848', '847', '846', '845', '844', '843', '842', '841', '840', '839', '838', '837', '836', '835', '834', '833', '832', '831', '830', '829', '828', '827', '826', '825', '824', '823', '822', '821', '820', '819', '818', '817', '816', '815', '814', '813', '812', '811', '810', '809', '808', '807', '806', '805', '804', '803', '802', '801', '800', '799', '798', '797', '796', '795', '794', '793', '792', '791', '790', '789', '788', '787', '786', '785', '784', '783', '782', '781', '780', '779', '778', '777', '776', '775', '774', '773', '772', '771', '770', '769', '768', '767', '766', '765', '764', '763', '762', '761', '760', '759', '758', '757', '756', '755', '754', '753', '752', '751', '750', '749', '748', '747', '746', '745', '744', '743', '742', '741', '740', '739', '738');

#user = cur.execute('select user from DEVICES where ipaddress ="10.104.249.159"')
#y = abc.fetchone()

#cur.execute("select * from datacenter ")
#addlist = ["10.104.240.6", "Router"]
#cur.execute('select * from DEVICES where ipaddress=? AND devicetype=?' , [addlist[0], addlist[1]])
#cur.execute('DELETE from datacenter where powerstate="poweredOn"')
#con.commit()
#abc = cur.execute('delete from CREDENTIALS where name="Karan"')
#cur.execute('select * from DEVICES')
#y = abc.fetchone()[1]
#print(y)
#print(y[1])
#cur.execute("insert into CREDENTIALS (name, lastname, mail, password) VALUES(?,?,?,?)",("Bibhu", "Kar", "bkar@cisco.com", "cisco123"))
#print(cur.fetchone())

#cur.execute('select assigntag from DEVICES where component="LAB" AND reachability="Unreachable"')
#cur.execute('update DEVICES set user="None" where component="LAB"')
#cur.execute('select * from DEVICES where ipaddress="175.175.175.30"')

#strr = [row[0] for row in user]
#print(strr)
for value in cur:
    print(str(value))



#print(my_dict)
#colnames = cur.description
#for row in colnames:
#    print(row[0])

#row = cur.fetchone()
#names = row.keys()
