
from f5.bigip import ManagementRoot
from f5.bigip.tm.net.vlan import Vlan

# Connect to the BigIP and configure the basic objects
mgmt = ManagementRoot("x.x.x.x", "admin", "password")

#print(dir(mgmt.tm.net.vlans))

class createVlan(object):
   def __init__(self,**kwargs):
       self.name= kwargs.get('name')
       self.partion = kwargs.get('partition')


f5Vlans = mgmt.tm.net.vlans.get_collection()
f5Interfaces = mgmt.tm.net.interfaces.get_collection()

#print(dir(mgmt.tm.net.vlans.vlan.create))


print(list(z.raw for z in mgmt.tm.net.vlans.vlan.load(name="VLAN_INT_1681").interfaces_s.get_collection()))

#VLAN creation
mgmt.tm.net.vlans.vlan.create(
name= 'VLAN_APITEST_1722',
description= 'VLAN APITEST 1722',
tag = '1722').interfaces_s.interfaces.create(name='Internal',tagged=True)







# print(dir(mgmt.tm.net.vlans.items))
# print("")
# print(mgmt.tm.net.vlans.items)
#print(dir(f5Interfaces))


def printObjects (f5Object):
   for x in f5Object:
       #print(dir(x))
       print(x.raw) # Full output of VLan Config
       print(" VLAN Name: {}  VLAN ID: {}".format(x.name,x.tag))

#printObjects(f5Interfaces)
#print('\n\n\nVlans')
#printObjects(f5Vlans)
