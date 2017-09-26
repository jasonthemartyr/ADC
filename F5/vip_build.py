import urllib3, configparser, os

from f5.bigip import ManagementRoot

urllib3.disable_warnings()

def build_node(f5_partition,
               **kwargs):
    output = []
    try:
        existing_nodes = mgmt.tm.ltm.nodes.get_collection()
    except ValueError:
        error = "Could not connect to F5: {}".format(ValueError)
        output.append(error)
    else:
        for node_name, node_address in kwargs.items():
            node_list = [(node.address).split('%')[0] for node in existing_nodes]
            if node_address in node_list:
                exists = "{} exists".format(node_address)
                output.append(exists)
            else:
                node_desc = '{}.werner.com'.format(node_name)
                node = mgmt.tm.ltm.nodes.node.create(partition=f5_partition,
                                                     name=node_name,
                                                     address=node_address,
                                                     description=node_desc)
                output.append(node.raw)
        return output


def build_pool(f5_partition,
               name,
               node_dict,
               allow_nat,
               allow_snat,
               ramp_time,
               monitor,
               node_priority,
               pool_port):
    output = []
    try:
        existing_pools = mgmt.tm.ltm.pools.get_collection()
    except ValueError:
        error = "Could not connect to F5: {}".format(ValueError)
        output.append(error)
    else:
        pool_list = [pool.name for pool in existing_pools]
        if pool_port == '80':
            pool_name = '{}_{}_pool'.format(name,
                                            pool_port)
        elif pool_port == '443':
            pool_name = '{}_{}_pool'.format(name,
                                            pool_port)
        else:
            pool_name = '{}_{}_pool'.format(name,
                                            pool_port)

        if pool_name in pool_list:
            exists = "{} exists".format(pool_name)
            output.append(exists)
        else:
            pool_desc = '{}.werner.com'.format(pool_name)
            monitor_path = '/Common/{}'.format(monitor)
            pool = mgmt.tm.ltm.pools.pool.create(partition=f5_partition,
                                                 name=pool_name,
                                                 description=pool_desc,
                                                 allowNat=allow_nat,
                                                 allowSnat=allow_snat,
                                                 slowRampTime=ramp_time,
                                                 monitor=monitor_path)

            my_pool = mgmt.tm.ltm.pools.pool.load(partition=f5_partition,
                                                  name=pool_name)
            node_list = ['{}:{}'.format(name, pool_port) for name, ip in node_dict.items()]
            node_zip = zip(node_list, node_priority)

            # for node in node_list:
            for node, priority in node_zip:
                # need to figure out priortyGroup settings

                add_nodes = my_pool.members_s.members.create(partition=f5_partition,
                                                             name=node,
                                                             priorityGroup=priority)
                test = my_pool.members_s.get_collection()
                for x in test:
                    print(x.raw)

                node_msg = '{} was added to {}'.format(add_nodes.name,
                                                       pool.name)
                output.append(node_msg)
        return output


def build_vip(f5_partition,
              name,
              vip_ip,
              vip_port,
              irules,
              pool_port):

    output = []

    try:
        existing_vips = mgmt.tm.ltm.virtuals.get_collection()
    except ValueError:
        error = "Could not connect to F5: {}".format(ValueError)
        output.append(error)
    else:
        if vip_port == '80':
            vip_name = '{}-http-{}'.format(name,
                                           vip_port)
        elif vip_port == '443':
            vip_name = '{}-https-{}'.format(name,
                                            vip_port)
        else:
            vip_name = '{}-{}'.format(name,
                                      vip_port)

        vip_list = [vip.name for vip in existing_vips]

        if vip_name in vip_list:
            exists = "{} exists".format(vip_name)
            output.append(exists)
        else:
            vip_desc = '{}.werner.com'.format(name)
            vip_pool = '/{}/{}_{}_pool'.format(f5_partition,
                                               name,
                                               pool_port)

            vip_dest = '/{}/{}%10:{}'.format(f5_partition,
                                             vip_ip,
                                             vip_port)
            vip_protocol = 'tcp'

            vip = ltm.virtuals.virtual.create(partition=f5_partition,
                                              name=vip_name,
                                              description=vip_desc,
                                              destination=vip_dest,
                                              pool=vip_pool,
                                              ipProtocol=vip_protocol,
                                              sourceAddressTranslation={'type': 'automap'},
                                              profiles='http',
                                              rules=irules)
            output.append(vip.raw)
        return output

def lets_print_this_bitch(some_list):

    for thingamob in some_list:
        return thingamob

mgmt = ManagementRoot("x.x.x.x",
                      "username",
                      "password")
ltm = mgmt.tm.ltm


ini_file = configparser.ConfigParser()
savepath = '/Users/jmarter/PycharmProjects/ADC/F5/'
filename = 'test.ini'
fullpath = os.path.join(savepath, filename)

ini_file.read(fullpath)
config_read = ini_file.read(fullpath)

#general settings from ini
general = ini_file['general']
name = general.get('name')
f5_partition = general.get('f5_partition')

#build node from ini
nodes = ini_file['nodes']
node_list = [nodes.get(field) for field in nodes]
node_name = node_list[0::3]
node_priority = node_list[1::3]
node_ips = node_list[2::3]
node_dict = dict(zip(node_name,
                     node_ips))





#build pool from ini
pool = ini_file['pool']
pool_list = [pool.get(field) for field in pool]
allow_nat = pool_list[0]
allow_snat = pool_list[1]
ramp_time = pool_list[2]
monitor = pool_list[3]
pool_port = pool_list[4]



#build vip from ini
vip = ini_file['vip']
irules = ini_file['irules']
vip_list = [vip.get(field) for field in vip]
vip_ip = vip_list[0]
vip_port = vip_list[1]
irules_list = [irules.get(field) for field in irules]



build_node = build_node(f5_partition,
                        **node_dict)

for node in build_node:
    print(node)

build_pool = build_pool(f5_partition,
                name,
                node_dict,
                allow_nat,
                allow_snat,
                ramp_time,
                monitor,
                node_priority,
                pool_port)

for pool in build_pool:
    print(pool)



build_vip = build_vip(f5_partition,
                      name,
                      vip_ip,
                      vip_port,
                      irules_list,
                      pool_port)

lets_print_this_bitch(build_vip)
#

