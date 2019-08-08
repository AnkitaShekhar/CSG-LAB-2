import sqlite3

class credentials_database():

    def __init__(self, list):
        self.newlist = list

    """ create a database connection to the SQLite database"""
    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    """ Insert Credentials into the SQLite database"""
    def insert_credentials(self, con):
        cur = con.cursor()
        print("Adding Credentials in database: " + self.newlist[1])
        cred_out1 = cur.execute("select * from CREDENTIALS where mail=?", [self.newlist[2]])
        print(cred_out1.fetchone())
        if cred_out1.fetchone() is None:
            cur.execute("insert into CREDENTIALS (name, lastname, mail, password) VALUES(?,?,?,?)",(self.newlist[0], self.newlist[1], self.newlist[2], self.newlist[3]))
            con.commit()
            print("Credentials added successfully")
            return "SUCCESS"
        else:
            return "FAIL"

    def search_credentials(self, con):
        cur = con.cursor()
        count = cur.execute('select count(mail) from CREDENTIALS where mail=""')

    def getcredentials(self, con):
        cur = con.cursor()
        print("Fetching Credentials detail for User: " + str(self.newlist[0]))
        output = cur.execute("select * from Credentials where mail=? AND password=?", [self.newlist[0], self.newlist[1]])
        return output


class getcredentials():
    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def get_name(self, con, mailid):
        cur = con.cursor()
        print("Fetching Name & Surname ")
        output = cur.execute("select name, lastname from Credentials where mail=?", [mailid])
        name = []
        for val in output:
            name.append(val[0])
            name.append(val[1])
        print(name)
        return name
