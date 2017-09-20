import urllib3
from f5.bigip import ManagementRoot

urllib3.disable_warnings()

mgmt = ManagementRoot("x.x.x.x", "username", "password")
ltm = mgmt.tm.ltm
pools = ltm.pools
virtual_address = ltm.virtual_address_s
virtual_servers = ltm.virtuals
get_nodes = ltm.nodes.get_collection()


# unpack collection
# for server in virtual_servers.get_collection():
#     print(server.raw)

# for node in ltm.nodes.get_collection():
#     print(node.raw)


# existing_nodes = mgmt.tm.ltm.nodes.get_collection()


# build node
# test_jason_node = ltm.nodes.node.create(partition='CDE-DMZ',name='test_jason01', address='10.98.10.254', description='this is a test node created via the SDK')
# print(test_jason_node.raw)

def build_node(f5_partition, node_name, node_address):
    """
    builds an F5 node
    :param f5_partition:
    :param node_name:
    :param node_address:
    :param node_desc:
    :return:
    """
    try:
        existing_nodes = mgmt.tm.ltm.nodes.get_collection()
    except ValueError:
        print("Could not connect to F5")
    else:
        node_list = [node.name for node in existing_nodes]
        if node_name in node_list:
            print("{} exists".format(node_name))
        else:
            node_desc = '{}.werner.com'.format(node_name)
            node = mgmt.tm.ltm.nodes.node.create(partition=f5_partition, name=node_name, address=node_address,
                                                 description=node_desc)
            return node.raw


def build_pool(f5_partition, pool_name, node_list, allow_nat, allow_snat, ramp_time, monitor):
    """
    builds F5 pool and adds nodes specified in list to pool
    :param f5_partition:
    :param pool_name:
    :param node_list:
    :return:
    """
    # create pool and add nodes
    try:
        existing_pools = mgmt.tm.ltm.pools.get_collection()
    except ValueError:
        print("Could not connect to F5")
    else:
        pool_list = [pool.name for pool in existing_pools]
        if pool_name in pool_list:
            print("{} exists".format(pool_name))
        else:
            pool_desc = '{}.werner.com'.format(pool_name)
            monitor_path = '/Common/{}'.format(monitor)
            pool = mgmt.tm.ltm.pools.pool.create(partition=f5_partition, name=pool_name, description=pool_desc,allowNat=allow_nat,allowSnat=allow_snat, slowRampTime=ramp_time, monitor=monitor_path)
            my_pool = mgmt.tm.ltm.pools.pool.load(partition=f5_partition, name=pool_name)
            for node in node_list:
                add_nodes = my_pool.members_s.members.create(partition=f5_partition, name=node)
                test = my_pool.members_s.get_collection()
                for x in test:
                    print(x.raw)

                print('{} was added to {}'.format(add_nodes.name, pool.name))


# return pool.raw




def build_vip(f5_partition, vip_name, vip_ip, vip_port, pool_name):
    try:
        existing_vips = mgmt.tm.ltm.virtuals.get_collection()
    except ValueError:
        print("Could not connect to F5")
    else:
        vip_list = [vip.name for vip in existing_vips]
        if vip_name in vip_list:
            print("{} exists".format(vip_name))
        else:
            vip_desc = '{}.werner.com'.format(vip_name)
            vip_pool = '/{}/{}'.format(f5_partition, pool_name)
            vip_dest = '/{}/{}%10:{}'.format(f5_partition, vip_ip, vip_port)

            # node = mgmt.tm.ltm.nodes.node.create(partition=f5_partition, name=node_name, address=node_address,description=vip_desc)
            vip = ltm.virtuals.virtual.create(partition=f5_partition, name=vip_name, description=vip_desc,
                                              destination=vip_dest, pool=vip_pool)
            return vip.raw


# test_jason_vip = ltm.virtuals.virtual.create(partition='CDE-DMZ', name='test_jason_http-80', description='this is a test VIP created via the SDK', destination='/CDE-DMZ/10.98.0.254%10:80', pool='/CDE-DMZ/test_jason_http_80')

# existing_nodes = mgmt.tm.ltm.virtuals.get_collection()
#
#
# for node in existing_nodes:
#     print(node.name)






# load an existing pool
# test_jason_pool = mgmt.tm.ltm.pools.pool.load(partition='CDE-DMZ', name='test_jason_http_80')
# test_jason_pool_member = test_jason_pool.members_s.members

#

# add node to pool
# test_jason_pool_member_add = test_jason_pool_member.create(partition='CDE-DMZ', name='test_jason01:80')
# test_jason_pool.members_s.members.create(partition='CDE-DMZ', name='test_jason01:80')
# get pool memebers
# get_test_jason_pool_members = test_jason_pool.members_s.get_collection()
# print(test_jason_pool_member.raw)



# test = mgmt.tm.ltm.pools.get_collection()
#
# for pool in test:
#
#     print(pool.name)
#     for member in pool.members_s.get_collection():
#
#         print(member.name)


f5_partition = 'CDE-DMZ'
node_dict = {'test_jason01': '10.98.10.252', 'test_jason02': '10.98.10.253', 'test_jason03': '10.98.10.254'}
pool_name = 'test_jason_http_80'
node_list = ['test_jason01:80', 'test_jason02:443']
vip_name = 'test_jason_http-80'
vip_ip = '10.98.0.254'
vip_port = '80'

allow_nat = 'no'
allow_snat = 'no'
ramp_time = '5'
monitor = 'tcp'

# test_jason_vip = ltm.virtuals.virtual.create(partition='CDE-DMZ', name='test_jason_http-80', description='this is a test VIP created via the SDK', destination='/CDE-DMZ/10.98.0.254%10:80', pool='/CDE-DMZ/test_jason_http_80')

# loop to build nodes
for node_name, node_address in node_dict.items():
    building_nodes = build_node(f5_partition, node_name, node_address)
    #print(building_nodes)

#zz = build_pool(f5_partition, pool_name, node_list)
zz = build_pool(f5_partition, pool_name, node_list, allow_nat, allow_snat, ramp_time, monitor)

print(zz)

# vip = build_vip(f5_partition, vip_name, vip_ip, vip_port, pool_name)

vip = build_vip(f5_partition, vip_name, vip_ip, vip_port, pool_name)
print(vip)


# existing_pools = mgmt.tm.ltm.pools.get_collection()
#
#
# for pool in existing_pools:
#     print(pool.raw)






# load an existing pool
# test_jason_pool = mgmt.tm.ltm.pools.pool.load(partition='CDE-DMZ', name='test_jason_http_80')
# test_jason_pool_member = test_jason_pool.members_s.members

# add node to pool
# test_jason_pool_member_add = test_jason_pool_member.create(partition='CDE-DMZ', name='test_jason01:80')

# get pool memebers
# get_test_jason_pool_members = test_jason_pool.members_s.get_collection()
# print(test_jason_pool_member.raw)

# build VIP and add pool
# test_jason_vip = ltm.virtuals.virtual.create(partition='CDE-DMZ', name='test_jason_http-80', description='this is a test VIP created via the SDK', destination='/CDE-DMZ/10.98.0.254%10:80', pool='/CDE-DMZ/test_jason_http_80')
# print(test_jason_vip.raw)
