from kazoo.client import KazooClient
import logging, time, json

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


class RegisterCenter(object):
    def __init__(self, hosts="127.0.0.1:2181"):
        self.hosts = hosts

    def connection_listener(self):
        if self.state == "LOST":
            logging.warning("zookeeper connect lost!")
        # Register somewhere that the session was lost
        elif self.state == "SUSPENDED":
            logging.warning("zookeeper connect disconnected!")
        # Handle being disconnected from Zookeeper
        else:
            logging.info("zookeeper connect connected!")
            # Handle being connected/reconnected to Zookeeper

    def connect(self):
        if self.hosts:
            zk = KazooClient(hosts=self.hosts)
        else:
            zk = KazooClient()
        zk.start()
        zk.add_listener(self.connection_listener)
        return zk

    def return_service_type(self,type):
        if type not in ["provider", "consumer"]:
            logging.warning("type is not provider or consumer!")
            raise Exception("type must be provider or consumer!")
        return 1

    def service_register(self, servicename, type, address):
        if self.return_service_type(type):
            zk = self.connect()
            zk.ensure_path("/%s/%s" % (servicename, type))
            zk.create("/%s/%s/ID" % (servicename, type), json.dumps(address).encode(), ephemeral=True, sequence=True)

    def get_register(self, servicename,type):
        if self.return_service_type(type):
            zk = self.connect()
            result = zk.get_children("/%s/%s" % (servicename,type))
            register = []
            if result:
                for i in result:
                    data, stat = zk.get("/%s/%s/%s" % (servicename,type,i))
                    register.append(data.decode("utf-8"))
            return register
        return []



