from pyVim.connect import SmartConnect, Disconnect
import ssl
import upd_datacenter

class vcenter ():
    def __init__(self):
        self.vcenterdict = {"10.104.240.44": ["Administrator@vsphere.local", "Pidnac@123"]
                         }
        self.esxilist = []

    def get_vm_detail(self, vm):
        vmdetail = [vm.guest.ipAddress, vm.guest.guestFullName, vm.runtime.powerState, vm.summary.quickStats.uptimeSeconds, vm.datastore[0].name, vm.summary.config.numCpu, vm.summary.config.memorySizeMB, vm.summary.storage.unshared]
        print("IPAddress : " + str(vm.guest.ipAddress))
        print("OS : " + str(vm.guest.guestFullName))
        print("Power State : " + str(vm.runtime.powerState))
        print("CPU: " + str(vm.summary.config.numCpu))
        print("Memory: " + str(vm.summary.config.memorySizeMB))
        print("Hardisk: " + str(vm.summary.storage.unshared))
        print("UP Time : " + str(vm.summary.quickStats.uptimeSeconds))
        return vmdetail

    def get_esxi(self, datacenter):
        esxilist = []
        esxiobjectlist = datacenter.hostFolder.childEntity
        print("###############" + datacenter.name +"########################")
        for esxi in esxiobjectlist:
            print("### ESXI : " + esxi.name)
            esxilist.append(esxi.name)
            self.esxilist.append(esxi.name)
        return esxilist, esxiobjectlist

    def get_vm(self, host):
        for vmfolder in host:
            vmobjectlist = vmfolder.vm
            vmlist = []
            for vm in vmobjectlist:
                print("### VM : " + vm.name)
                vmlist.append(vm.name)
        return vmlist, vmobjectlist

    def getdatacenter(self, key, value):

        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE

        try:
            c = SmartConnect(host=key, user=value[0], pwd=value[1])
            print('Valid certificate')
        except:
            c = SmartConnect(host=key, user=value[0], pwd=value[1], sslContext=s)
            print('Invalid or untrusted certificate')

        datacenternamelist = []
        datacenterobjectlist = []
        print("#################" + key + "#####################")
        for datacenter in c.content.rootFolder.childEntity:
            print("### datacenter : " + datacenter.name)
            try:
                for dc in datacenter.childEntity:
                    tmp_dc = (datacenter.name + "/" + dc.name)
                    datacenternamelist.append(tmp_dc)
                    datacenterobjectlist.append(dc)
            except:
                datacenternamelist.append(datacenter.name)
                datacenterobjectlist.append(datacenter)

        return datacenternamelist, datacenterobjectlist, c

"""Datacenter"""
vcenterdict = {}
datacenterobjectlist = []


Obj_vcenter = vcenter()
for key, value in Obj_vcenter.vcenterdict.items():
    datacenternamelist, datacenterobjectlist, c = Obj_vcenter.getdatacenter(key, value)
    vcenterdict.update({key: datacenternamelist})
    print(datacenternamelist)
    print(vcenterdict)

datacenterdict = {}
tot_esxiobjectlist = []

"""ESXI"""
for datacenter in datacenterobjectlist:
    print("Datacenter-->" + str(datacenter))
    esxilist, esxiobjectlist = Obj_vcenter.get_esxi(datacenter)
    datacenterdict.update({datacenter.name:esxilist})
    tot_esxiobjectlist = tot_esxiobjectlist + esxiobjectlist

totvmlist = []
totvmobjectlist = []
esxidict = {}
for esxiobj in tot_esxiobjectlist:
    print("###############" + esxiobj.name + "########################")
    vmlist, vmobjectlist = Obj_vcenter.get_vm(esxiobj.host)
    esxidict.update({esxiobj.name:vmlist})
    totvmlist = totvmlist + vmlist
    totvmobjectlist = totvmobjectlist + vmobjectlist

vmdict = {}
totvmdetail = []
for vm in totvmobjectlist:
    print("###############" + vm.name + "########################")
    vm_detail = Obj_vcenter.get_vm_detail(vm)
    totvmdetail = totvmdetail + vm_detail
    vmdict.update({vm.name:vm_detail})

Disconnect(c)

newvmdict_1 = {}

for vmkey, vmvalue in vmdict.items():
    for esxikey, esxivalue in esxidict.items():
        if vmkey in esxivalue:
            newvmdict_1.update({vmkey: (vmvalue + [esxikey])})

print("*******newvmdict_1********")
print(newvmdict_1)
print(datacenterdict)


newvmdict_1_2 = {}
for vmkey, vmvalue in newvmdict_1.items():
    for dckey, dcvalue in datacenterdict.items():
        if vmvalue[8] in dcvalue:
            newvmdict_1_2.update({vmkey:(vmvalue + [dckey])})

print("*******newvmdict_1_2********")
print(newvmdict_1_2)
newvmdict_1_3 = {}

for vmkey, vmvalue in newvmdict_1_2.items():
    for vckey, vcvalue in vcenterdict.items():
        if list(filter(lambda x: vmvalue[9] in x, vcvalue)):
            newvmdict_1_3.update({vmkey:(vmvalue + [vckey])})
            print(newvmdict_1_3)

print("*******newvmdict_1_3********")
print(newvmdict_1_3)

Obj_vcenter = upd_datacenter.vcenter_db()
conn = Obj_vcenter.connectdb()
Obj_vcenter.insert_vcenter_db(conn,newvmdict_1_3)
conn.commit()
