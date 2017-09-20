import urllib3
from f5.bigip import ManagementRoot

urllib3.disable_warnings()

mgmt = ManagementRoot("x.x.x.x", "username", "password")
ltm = mgmt.tm.ltm
pools = ltm.pools
virtual_address = ltm.virtual_address_s
virtual_servers = ltm.virtuals
get_nodes = ltm.nodes.get_collection()

#unpack collection
# for server in virtual_servers.get_collection():
#     print(server.raw)

# for node in ltm.nodes.get_collection():
#     print(node.raw)


# existing_nodes = mgmt.tm.ltm.nodes.get_collection()


#build node
# test_jason_node = ltm.nodes.node.create(partition='CDE-DMZ',name='test_jason01', address='10.98.10.254', description='this is a test node created via the SDK')
# print(test_jason_node.raw)

def build_node(f5_partition,node_name,node_address,node_desc):
    '''
    build a node for F5
    :param f5_partition:
    :param node_name:
    :param node_address:
    :param node_desc:
    :return:
    '''
    try:
        existing_nodes = mgmt.tm.ltm.nodes.get_collection()
    except ValueError:
        print("Could not connect to F5")
    else:
        node_list = [node.name for node in existing_nodes]
        if node_name in node_list:
            print("{} exists".format(node_name))
        else:
            node = mgmt.tm.ltm.nodes.node.create(partition=f5_partition, name=node_name, address=node_address,description=node_desc)
            return node.raw


def build_pool(f5_partition, pool_name, pool_desc):
    # create pool

    try:
        existing_pools = mgmt.tm.ltm.pools.get_collection()
    except ValueError:
        print("Could not connect to F5")
    else:
        pool_list = [pool.name for pool in existing_pools]
        if pool_name in pool_list:
            print("{} exists".format(pool_name))
        else:

            pool = mgmt.tm.ltm.pools.pool.create(partition=f5_partition, name=pool_name, description=pool_desc)
            return pool.raw


f5_partition = 'CDE-DMZ'
node_name = 'test_jason01'
node_address = '10.98.10.254'
node_desc = 'this is a test node created via the SDK'
pool_name = 'test_jason_http_80'
pool_desc = 'this is a test pool created via the SDK'

# ww = build_node(f5_partition,node_name,node_address,node_desc)
#
# print(ww)
zz = build_pool(f5_partition, pool_name, pool_desc)
print(zz)


# x = mgmt.tm.ltm.pools.get_collection()
#
# for y in x:
#     print(y.raw)




    # print(test_jason_pool.raw)

#load an existing pool
# test_jason_pool = mgmt.tm.ltm.pools.pool.load(partition='CDE-DMZ', name='test_jason_http_80')
# test_jason_pool_member = test_jason_pool.members_s.members

#add node to pool
# test_jason_pool_member_add = test_jason_pool_member.create(partition='CDE-DMZ', name='test_jason01:80')

#get pool memebers
# get_test_jason_pool_members = test_jason_pool.members_s.get_collection()
# print(test_jason_pool_member.raw)

#build VIP and add pool
# test_jason_vip = ltm.virtuals.virtual.create(partition='CDE-DMZ', name='test_jason_http-80', description='this is a test VIP created via the SDK', destination='/CDE-DMZ/10.98.0.254%10:80', pool='/CDE-DMZ/test_jason_http_80')
#print(test_jason_vip.raw)





