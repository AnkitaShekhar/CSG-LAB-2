#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for,session, g, flash
import class_database
import devices_db
#import telnet_ssh
import upd_datacenter
import insert_db
import os
import history
import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)

"""Main Login"""
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('role', None)
        g.newuser = request.form['username']

        """Input from Login form for Login"""
        loginlist = [request.form['username'], request.form['password']]

        """Fetching User detail from db"""
        Obj1 = class_database.credentials_database(loginlist)
        conn = Obj1.connectdb()
        credentialcheck = Obj1.getcredentials(conn)

        """converting tupple to list"""
        userdetail = [row for row in list(credentialcheck)]
        print(userdetail)

        """login"""
        if len(userdetail) is 1:
            session['user'] = request.form['username']
            session['role'] = userdetail[0][4]

            return redirect(url_for('dashboard'))
        else:
            message="Wrong Credendtials"
            return render_template("Login.html", message=message)

    return render_template("Login.html")

@app.before_request
def before_request():
    g.user = None
    g.role = None

    if 'user' in session:
        g.user = session['user']
        g.role = session['role']

        obj_session = class_database.getcredentials()
        con = obj_session.connectdb()
        name = obj_session.get_name(con, g.user)
        g.name = name[0]
        g.lastname = name[1]
        print(g.name, g.lastname)


"""New User Registration"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        """Input from Register form for adding Credentials"""
        registerlist = [request.form['name'], request.form['lname'], request.form['email'], request.form['password']]
        print(registerlist)

        """Creating object to connect with db"""
        Obj1 = class_database.credentials_database(registerlist)
        conn = Obj1.connectdb()

        """Inserting Credentials into database"""
        Status = Obj1.insert_credentials(conn)
        print(Status)
        if Status == "SUCCESS":
            return redirect(url_for('login'))
        else:
            return render_template("Register.html", message="Error: User is already registered with same mail id")

    return render_template("Register.html")

"""Dashboard to see all data"""
@app.route('/Dashboard.html', methods=['GET', 'POST'])
def dashboard():

    print(g.role)
    """Creating object to connect with db"""
    Obj_Dash = devices_db.devices()
    conn = Obj_Dash.connectdb()
    dict_dash = {}
    devicetype = ["Router", "Switch", "WLC", "Nexus"]
    for dtype in devicetype:
        value = Obj_Dash.get_dashboard_data(conn, dtype)
        print(list(value))
        dict_dash.update({dtype:list(value)})
    print(dict_dash)

    dnac = Obj_Dash.get_dnac_data(conn)
    print(dnac)

    Obj_Dash = upd_datacenter.vcenter_db()
    conn = Obj_Dash.connectdb()
    vcenter = Obj_Dash.dashboard_data(conn)

    if g.user and g.role == 'admin':
        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
        return render_template("Dashboard.html", Dash=dict_dash, dnac=dnac, page=page_admin, vcenter=vcenter)
    else:
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        return render_template("Dashboard.html", Dash=dict_dash, dnac=dnac, page=page, vcenter=vcenter)

"""LAB: Router data"""
@app.route('/Router.html', methods=['GET', 'POST'])
def router():

    page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]

    Obj_Router = devices_db.devices()
    conn = Obj_Router.connectdb()
    cur = Obj_Router.get_router_data(conn)
    page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]

    if g.user and g.role is not "admin":
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        return render_template("Router.html", route=cur, page=page)
    else:
        return redirect(url_for('router_admin'))

@app.route('/Router/search', methods=['GET', 'POST'])
def search():
    #print(name)
    print(request.form['search'])
    obj_search = devices_db.devices()
    conn = obj_search.connectdb()
    cur = obj_search.getsearch(conn, request.form['search'])

    page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
    page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
    if g.user and g.role is not "admin":
        return render_template("Router.html", route=cur, page=page)
    else:
        return redirect(url_for('router_admin'))

"""LAB: Router data with admin access"""
@app.route('/Router_admin.html', methods=['GET', 'POST'])
def router_admin():
    if g.user:
        Obj_Router = devices_db.devices()
        conn = Obj_Router.connectdb()
        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]

        if request.method == 'POST' and request.form['Action'] == "Assign":
            print(request.form['Action'])
            cred = Obj_Router.get_credentials(conn, request.form['assignid'])

            """Telnet into router"""
            obj_tel = telnet_ssh.tel_ssh(list(cred))
            response = obj_tel.tel_router(request.form['userid'], request.form['assignid'])

            if response == 0:
                print("Updating database with User, Assign Date, Release Date")
                today = datetime.datetime.today().strftime("%d-%m-%Y")
                R_day = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
                device_data = [request.form['assignid'], request.form['userid'], today, R_day]
                update_db = insert_db.insert()
                conn = update_db.connectdb()
                update_db.upd_assign_device(conn, device_data)

                print("Updating history with User, Assign Date, Release Date")
                print(device_data)
                history_db = history.history()
                conn = history_db.connectdb()
                history_db.history(conn, device_data)
                print("Device Assigned Successfully")

                data = Obj_Router.getipdata(conn, request.form['assignid'])
                ipdata = [row for row in data]
                print(ipdata)

                print("Sending Mail...")
                mailsender = insert_db.insert()
                mailsender.Send_Mail_Assign_Device(ipdata)


                device_assign = {
                    "Device Series": ipdata[3],
                    "Device Model": ipdata[8],
                    "Credentials": ipdata[15] + "/" + ipdata[15] + "/" + ipdata[15],
                    "SNMP" : ipdata[15] + "-ro / " + ipdata[15] + "-rw",
                    "Release Date": ipdata[17]
                }
                return render_template("Device_Assignment.html", Assign=device_assign, header="Assignment", devIP=request.form['assignid'])

            else:
                print("Device credentials wrong or telnet issue")
                error = "Credentials Wrong. Not able to Assign device."
                return render_template("Device_Assignment.html", error=error, header="Assignment",
                                       devIP=request.form['assignid'])


        elif request.method == 'POST' and request.form['Action'] == "Release":
            print(request.form['Action'])
            print(request.form['assignid'])
            tmpuser = Obj_Router.get_user(conn, request.form['assignid'])
            user = [row[0] for row in tmpuser]
            print(user)

            data = Obj_Router.getipdata(conn, request.form['assignid'])
            ipdata = [row for row in data]
            print(ipdata)

            Obj_Router = telnet_ssh.tel_ssh(user)
            response = Obj_Router.rel_router_switch(user, request.form['assignid'])
            print(response)

            if response == 0:
                print("Removing User, Assign Date, Release Date from database")
                device_assign = {
                    "Device Series": ipdata[3],
                    "Device Model": ipdata[8],
                    "User": ipdata[15],
                    "Release Date": ipdata[17]
                }
                print("Sending Mail...")
                mailsender = insert_db.insert()
                mailsender.Send_Mail_Release_Device(ipdata)

                print("Updating database...")
                update_db = insert_db.insert()
                conn = update_db.connectdb()
                update_db.upd_release_device(conn, request.form['assignid'])

                return render_template("Device_Assignment.html", header="Released", devIP=request.form['assignid'], Assign=device_assign)
            else:
                print("Device credentials wrong or telnet issue")
                error = "Credentials changed. Not able to release device."
                return render_template("Device_Assignment.html", error=error, header="Released",
                                       devIP=request.form['assignid'])

        elif request.method == 'POST' and request.form['Action'] == "Extend":
            print(request.form['Action'])
            print(request.form['assignid'])
            R_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
            update_db = insert_db.insert()
            conn = update_db.connectdb()
            update_db.upd_extend_device(conn, request.form['assignid'], R_day)
            return render_template("Device_Assignment.html")

        else:
            cur = Obj_Router.get_router_data(conn)
        return render_template("Router_admin.html", route=cur, page=page_admin)

    else:
        return redirect(url_for('login'))

"""LAB: Switch data"""
@app.route('/Switch.html', methods=['GET', 'POST'])
def switch():
    if g.user:
        Obj_Switch = devices_db.devices()
        conn = Obj_Switch.connectdb()
        cur = Obj_Switch.get_switch_data(conn)
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        return render_template("Switch.html", switch=cur, page=page)
    else:
        return redirect(url_for('login'))

"""LAB: Switch data with admin access"""
@app.route('/Switch_admin.html', methods=['GET', 'POST'])
def switch_admin():

    if g.user:
        obj1_switch = devices_db.devices()
        conn = obj1_switch.connectdb()
        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]

        if request.method == 'POST' and request.form['Action'] == "Assign":
            print(request.form['Action'])
            cred = obj1_switch.get_credentials(conn, request.form['assignid'])

            """Telnet into Switch"""
            obj_switch = telnet_ssh.tel_ssh(list(cred))
            response = obj_switch.tel_router(request.form['userid'], request.form['assignid'])

            if response == 0:
                print("Updating database with User, Assign Date, Release Date")
                today = datetime.datetime.today().strftime("%d-%m-%Y")
                R_day = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
                device_data = [request.form['assignid'], request.form['userid'], today, R_day]
                update_db = insert_db.insert()
                conn = update_db.connectdb()
                update_db.upd_assign_device(conn, device_data)

                print("Updating history with User, Assign Date, Release Date")
                history_db = history.history()
                conn = history_db.connectdb()
                history_db.history(conn, device_data)


                data = obj1_switch.getipdata(conn, request.form['assignid'])
                ipdata = [row for row in data]
                print(ipdata)

                print("Sending Mail...")
                mailsender = insert_db.insert()
                mailsender.Send_Mail_Assign_Device(ipdata)

                print("Device Assigned Successfully")

                device_assign = {
                    "Device Series": ipdata[3],
                    "Device Model": ipdata[8],
                    "Credentials": ipdata[15] + "/" + ipdata[15] + "/" + ipdata[15],
                    "SNMP": ipdata[15] + "-ro / " + ipdata[15] + "-rw",
                    "Release Date": ipdata[17]
                }
                return render_template("Device_Assignment.html", Assign=device_assign, header="Assignment", devIP=request.form['assignid'])

            else:
                print("Device credentials wrong or telnet issue")
                error = "Credentials Wrong. Not able to Assign device."
                return render_template("Device_Assignment.html", error=error, header="Assignment",
                                       devIP=request.form['assignid'])

        elif request.method == 'POST' and request.form['Action'] == "Release":
            print(request.form['Action'])
            print(request.form['assignid'])
            tmpuser = obj_switch.get_user(conn, request.form['assignid'])
            user = [row[0] for row in tmpuser]
            print(user)

            data = obj1_switch.getipdata(conn, request.form['assignid'])
            ipdata = [row for row in data]
            print(ipdata)

            obj_switch = telnet_ssh.tel_ssh(user)
            response = obj_switch.rel_router_switch(user, request.form['assignid'])
            print(response)

            if response == 0:
                print("Removing User, Assign Date, Release Date from database")
                device_assign = {
                    "Device Series": ipdata[3],
                    "Device Model": ipdata[8],
                    "User": ipdata[15],
                    "Release Date": ipdata[17]
                }

                print("Sending Mail...")
                mailsender = insert_db.insert()
                mailsender.Send_Mail_Release_Device(ipdata)

                print("Updating database...")
                update_db = insert_db.insert()
                conn = update_db.connectdb()
                update_db.upd_release_device(conn, request.form['assignid'])

                return render_template("Device_Assignment.html", header="Released", devIP=request.form['assignid'], Assign=device_assign)
            else:
                print("Device credentials wrong or telnet issue")
                error = "Credentials changed. Not able to release device."
                return render_template("Device_Assignment.html", error=error, header="Released", devIP=request.form['assignid'])

        elif request.method == 'POST' and request.form['Action'] == "Extend":
            print(request.form['Action'])
            print(request.form['assignid'])
            R_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
            update_db = insert_db.insert()
            conn = update_db.connectdb()
            update_db.upd_extend_device(conn, request.form['assignid'], R_day)
            return render_template("Device_Assignment.html")

        else:
            cur = obj1_switch.get_switch_data(conn)
            return render_template("Switch_admin.html", switch=cur, page=page_admin)

    else:
        return redirect(url_for('login'))

"""LAB: WLC data"""
@app.route('/Wireless.html', methods=['GET', 'POST'])
def wireless():

    if g.user:
        Obj_WLC = devices_db.devices()
        conn = Obj_WLC.connectdb()
        cur = Obj_WLC.get_wlc_data(conn)
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        return render_template("Wireless.html", wireless=cur, page=page)
    else:
        return redirect(url_for('login'))

"""LAB: WLC data with admin access"""
@app.route('/Wireless_admin.html', methods=['GET', 'POST'])
def wireless_admin():
    if g.user:
        Obj_WLC = devices_db.devices()
        conn = Obj_WLC.connectdb()
        cur = Obj_WLC.get_wlc_data(conn)
        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
        return render_template("Wireless_admin.html", wireless=cur, page=page_admin)
    else:
        return redirect(url_for('login'))
"""LAB: Nexus data"""
@app.route('/Nexus.html', methods=['GET', 'POST'])
def nexus():

    if g.user:
        Obj_Nexus = devices_db.devices()
        conn = Obj_Nexus.connectdb()
        cur = Obj_Nexus.get_nexus_data(conn)
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        return render_template("Nexus.html", nexus=cur, page=page)
    else:
        return redirect(url_for('login'))

"""LAB: Nexus  with admin access"""
@app.route('/Nexus_admin.html', methods=['GET', 'POST'])
def nexus_admin():
    if g.user:
        Obj_Nexus = devices_db.devices()
        conn = Obj_Nexus.connectdb()
        cur = Obj_Nexus.get_nexus_data(conn)
        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
        return render_template("Nexus_admin.html", nexus=cur, page=page_admin)
    else:
        return redirect(url_for('login'))

"""LAB: DNAC data"""
@app.route('/DNAC', methods=['GET', 'POST'])
def DNAC():
    if g.user:
        Obj_get_componet = devices_db.devices()
        conn = Obj_get_componet.connectdb()
        dnac_component = Obj_get_componet.get_dnac_component(conn)
        new_dnac_comp = [row[0] for row in dnac_component]
        print(new_dnac_comp)
        dnac = Obj_get_componet.get_dnac_data_1(conn)
        dnac_2 = Obj_get_componet.get_dnac_data_2(conn)
        print(dnac)
        print(dnac_2)
        dict_component = {}

        for row in list(new_dnac_comp):
            value = Obj_get_componet.get_componentwise_data(conn, row)
            dict_component.update({row:list(value)})
            print(dict_component)

        page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
        page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
        if g.role == "admin":
            return render_template("DNAC.html", comp_table=new_dnac_comp, comp_wise=dict_component, dnac=dnac, dnac2=dnac_2, page=page_admin)
        else:
            return render_template("DNAC.html", comp_table=new_dnac_comp, comp_wise=dict_component, dnac=dnac,
                                   dnac2=dnac_2, page=page )
    else:
        return redirect(url_for('login'))

"""LAB: DNAC data"""
@app.route('/DNAC/<component>', methods=['GET', 'POST'])
def dnac_component(component):
    print(component)
    page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
    page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
    if g.user:

        if component == "Dashboard.html" and request.method =='GET':
            return redirect(url_for("dashboard"))

        elif g.role == "admin" and component == "Router_admin.html":
            return redirect(url_for("router_admin"))
        elif g.role == "admin" and component == "Switch_admin.html":
            return redirect(url_for("switch_admin"))
        elif g.role == "admin" and component == "Wireless_admin.html":
            return redirect(url_for("wireless_admin"))
        elif g.role == "admin" and component == "Nexus_admin.html":
            return redirect(url_for("nexus_admin"))
        elif component == "Router.html":
            return redirect(url_for("router"))
        elif component == "Switch.html":
            return redirect(url_for("switch"))
        elif component == "Wireless.html":
            return redirect(url_for("wireless"))
        elif component == "Nexus.html":
            return redirect(url_for("nexus"))

        elif component == "Blades.html":
            return redirect(url_for("Blades.html"))
        elif component == "Other":
            return redirect(url_for("other"))
        elif component == "DNAC":
            return redirect(url_for("DNAC"))
        elif "set" in component:
            Obj_get_componet = devices_db.devices()
            conn = Obj_get_componet.connectdb()

            dnac = Obj_get_componet.get_dnac_data_1(conn)
            dnac_2 = Obj_get_componet.get_dnac_data_2(conn)

            dnac_component = Obj_get_componet.get_dnac_component(conn)
            new_dnac_comp = [row[0] for row in dnac_component]

            data = Obj_get_componet.get_set_data(conn, component)
            set_data = [row for row in data]
            print(set_data)
            if g.role == "admin":
                return render_template("DNAC.html", comp_table=new_dnac_comp, setdata=set_data, value="set", dnac=dnac,
                                       dnac2=dnac_2, page=page_admin)
            else:
                return render_template("DNAC.html", comp_table=new_dnac_comp, setdata=set_data, value="set", dnac=dnac,
                                       dnac2=dnac_2, page=page)
        elif "diff" in component:
            print(component)
            Obj_get_componet = devices_db.devices()
            conn = Obj_get_componet.connectdb()
            dnac_component = Obj_get_componet.get_dnac_component(conn)
            new_dnac_comp = [row[0] for row in dnac_component]

            dnac = Obj_get_componet.get_dnac_data_1(conn)
            dnac_2 = Obj_get_componet.get_dnac_data_2(conn)

            obj_get_diff = devices_db.devices()
            conn = obj_get_diff.connectdb()
            dict_set = {}

            for row in list(new_dnac_comp):
                dnacset_1 = obj_get_diff.getdnacset1data(conn, row)
                dnacset_2 = obj_get_diff.getdnacset2data(conn, row)

                set = dnacset_1.fetchone() + dnacset_2.fetchone()

                print(set)
                dict_set.update({row: list(set)})
                print(dict_set)
            if g.role == "admin":
                return render_template("DNAC.html", comp_table=new_dnac_comp, dnac=dnac, dnac2=dnac_2, value="diff", comp_wise=dict_set, page=page_admin)
            else:
                return render_template("DNAC.html", comp_table=new_dnac_comp, dnac=dnac, dnac2=dnac_2, value="diff",
                                       comp_wise=dict_set, page=page)

        elif component and request.method =='GET':
            Obj_get_componet = devices_db.devices()
            conn = Obj_get_componet.connectdb()
            dnac_component = Obj_get_componet.get_dnac_component(conn)
            new_dnac_comp = [row[0] for row in dnac_component]
            comp_data = Obj_get_componet.get_component_data(conn, component)
            if g.role == "admin":
                return render_template("component.html", comp_table=new_dnac_comp, data=comp_data, page=page_admin)
            else:
                return render_template("component.html", comp_table=new_dnac_comp, data=comp_data, page=page)
    else:
        return redirect(url_for('login'))

"""LAB: Blades data"""
@app.route('/vCenter', methods=['GET','POST'])
def blades():
    page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
    page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]
    if g.user:
        Obj_get_vm = upd_datacenter.vcenter_db()
        conn = Obj_get_vm.connectdb()
        vmdata = Obj_get_vm.get_vm(conn)
        new_vmdata = [row for row in vmdata]
        print(new_vmdata)
        if g.role == "admin":
            return render_template("Blades.html", vm=new_vmdata, page=page_admin)
        else:
            return render_template("Blades.html", vm=new_vmdata, page=page)
    else:
        return redirect(url_for('login'))

"""LAB: Blades data"""
@app.route('/vCenter/<name>', methods=['GET','POST'])
def blades_name(name):
    print(name)
    page_admin = ["Router_admin.html", "Switch_admin.html", "Wireless_admin.html", "Nexus_admin.html"]
    page = ["Router.html", "Switch.html", "Wireless.html", "Nexus.html"]

    if g.user:

        if name == "Dashboard.html" and request.method =='GET':
            return redirect(url_for("dashboard"))

        elif g.role == "admin" and name == "Router_admin.html":
            return redirect(url_for("router_admin"))
        elif g.role == "admin" and name == "Switch_admin.html":
            return redirect(url_for("switch_admin"))
        elif g.role == "admin" and name == "Wireless_admin.html":
            return redirect(url_for("wireless_admin"))
        elif g.role == "admin" and name == "Nexus_admin.html":
            return redirect(url_for("nexus_admin"))
        elif name == "Router.html":
            return redirect(url_for("router"))
        elif name == "Switch.html":
            return redirect(url_for("switch"))
        elif name == "Wireless.html":
            return redirect(url_for("wireless"))
        elif name == "Nexus.html":
            return redirect(url_for("nexus"))

        elif name == "vmdata":
            print("Data for: " + name)
            return redirect(url_for("blades"))

        elif name == "vCenter":
            return redirect(url_for("blades"))
        elif name == "Other":
            return redirect(url_for("other"))
        elif name == "DNAC":
            return redirect(url_for("DNAC"))

        elif name == "esxi" and request.method == 'GET':
            print("Data for: " + name)
            Obj_get_vm = upd_datacenter.vcenter_db()
            conn = Obj_get_vm.connectdb()
            esxidata = Obj_get_vm.get_esxi(conn)
            if g.role == "admin":
                return render_template("ESXi_data.html", esxi=esxidata, page=page_admin)
            else:
                return render_template("ESXi_data.html", esxi=esxidata, page=page)

        elif name == "datacenter" and request.method == 'GET':
            print("Data for: " + name)
            Obj_get_dc = upd_datacenter.vcenter_db()
            conn = Obj_get_dc.connectdb()
            esxidata = Obj_get_dc.dc_data(conn)
            if g.role == "admin":
                return render_template("ESXi_data.html", esxi=esxidata, page=page_admin, value="datacenter")
            else:
                return render_template("ESXi_data.html", esxi=esxidata, page=page, value = "datacenter")


        return render_template("Blades.html", mydict=mydict, name=name, length=dictlen)



@app.route('/Other')
def other():
    return render_template("Other.html")

@app.route('/Other/<name>', methods=['GET', 'POST'])
def other_name(name):
    print(name)

    if name == "Dashboard.html" and request.method =='GET':
        return redirect(url_for("dashboard"))
    elif name == "Router.html":
        return redirect(url_for("router"))
    elif name == "Switch.html":
        return redirect(url_for("switch"))
    elif name == "Wireless.html":
        return redirect(url_for("wireless"))
    elif name == "Nexus.html":
        return redirect(url_for("nexus"))
    elif name == "Blades.html":
        return redirect(url_for("Blades.html"))
    elif name == "DNAC":
        return redirect(url_for("DNAC"))
    elif name == "Other":
        return redirect(url_for("other"))
    elif name == "adddevice" and request.method =='GET':
        return render_template("adddevice.html")
    elif name == "deletedevice" and request.method =='GET':
        return render_template("deletedevice.html")
    elif name == "console" and request.method =='GET':
        return render_template("console.html")

    if name == "adddevice" and request.method == 'POST':
        print(request.form['component'])
        addlist = []
        if request.form['topology'] == "LAB":
            addlist = [request.form['ipaddress'],
                       request.form['topology'],
                       request.form['deviceseries'],
                       request.form['productid'],
                       request.form['username'],
                       request.form['password'],
                       request.form['enpass'],
                       request.form['snmpread'],
                       request.form['snmpwrite'],
                       request.form['Device Type'],
                       "LAB",
                       request.form['rvsv']]

        elif request.form['topology'] == "DNAC-TOP-1" and request.form['component']:
            addlist = [request.form['ipaddress'],
                       request.form['topology'],
                       request.form['deviceseries'],
                       request.form['productid'],
                       request.form['username'],
                       request.form['password'],
                       request.form['enpass'],
                       request.form['snmpread'],
                       request.form['snmpwrite'],
                       request.form['Device Type'],
                       "DNAC",
                       "DNAC",
                       request.form['component'],
                       request.form['rvsv']]

        elif request.form['topology'] == "DNAC-TOP-2" and request.form['component'] :
            addlist = [request.form['ipaddress'],
                       request.form['topology'],
                       request.form['deviceseries'],
                       request.form['productid'],
                       request.form['username'],
                       request.form['password'],
                       request.form['enpass'],
                       request.form['snmpread'],
                       request.form['snmpwrite'],
                       request.form['Device Type'],
                       "DNAC",
                       "DNAC",
                       request.form['component'],
                       request.form['rvsv']]
        else:
            flash("Enter Component")
            return render_template("adddevice.html")

        print("Adding into list" + str(addlist))
        Obj_ins_device = insert_db.insert()
        conn = Obj_ins_device.connectdb()
        cur = Obj_ins_device.insert_device(conn, addlist, request.form['topology'])
        if cur == True:
            flash('Device added successfully in database')
            return render_template("adddevice.html")
        else:
            flash("Wrong Credentials or Device already present in database")
            return render_template("adddevice.html")

    elif name == "deletedevice" and request.method =='POST':
        ipaddress = request.form['ipaddress']
        Obj_del_device = insert_db.insert()
        conn = Obj_del_device.connectdb()
        cur = Obj_del_device.delete_device(conn, ipaddress)
        print(cur)
        if cur == True:
            flash('Device deleted successfully')
            return render_template("deletedevice.html")
        else:
            return render_template("deletedevice.html")

    elif name == "console" and request.method =='POST':
        ipaddress = request.form['ipaddress']
        Obj_del_device = insert_db.insert()
        conn = Obj_del_device.connectdb()
        cur = Obj_del_device.delete_device(conn, ipaddress)
        print(cur)
        if cur == True:
            flash('Device deleted successfully')
            return render_template("deletedevice.html")
        else:
            return render_template("deletedevice.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
