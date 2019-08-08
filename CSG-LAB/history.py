import sqlite3

class history():

    def connectdb(self):
        con = sqlite3.connect("KCLAB.db")
        return con

    def history(self, con, assignlist):
        cur= con.cursor()
        cur.execute('insert into history (ipaddress, user, assigndate, releasedate, extendate, credchange) VALUES(?,?,?,?,?,?)',
                    assignlist[0], assignlist[1], assignlist[2], assignlist[3], assignlist[4], assignlist[5])
        con.commit()
