from pyVim.connect import SmartConnect, Disconnect
import ssl


s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

try:
    c = SmartConnect(host="10.126.218.50", user="root", pwd='esxi@123')
    print('Valid certificate')
except:
    #c = SmartConnect(host="10.104.240.42", user="Administrator@vsphere.local", pwd='PIapic@123', sslContext=s)
    c = SmartConnect(host="10.104.240.44", user="Administrator@vsphere.local", pwd='Pidnac@123', sslContext=s)
    print('Invalid or untrusted certificate')

datacenter = c.content.rootFolder.childEntity[0]
#print(datacenter)
#vms = datacenter.vmFolder

print(datacenter.name)
if hasattr(datacenter.childEntity)
    print()
child = datacenter.childEntity[0]
print(child.name)

esxilist = child.hostFolder.childEntity
for esxi in esxilist:
    print(esxi.name)

vmilist = child.vmFolder.childEntity
for vm in vmilist:
    print(vm.name)

print(c.CurrentTime())

Disconnect(c)