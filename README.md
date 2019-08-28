# registerservice
#基于zookeeper服务注册中心实现注册中心模块。
#可用于注册服务的提供者和消费者
#动态获取服务提供者和消费者的列表

from registerservice import RegisterCenter

#初始化连接
rs = RegisterCenter("192.168.1.2:2181")

#服务提供方服务启动前注册
#服务提供方注册服务:服务名：fill   注册类型： provider 是服务提供方，服务提供方地址：{"ip": "192.168.1.33", "port": "8000"}
rs.service_register("fill", "provider", {"ip": "192.168.1.33", "port": "8000"})

#服务消费方调用服务前注册
#服务消费方注册服务:服务名：fill   注册类型：consumer 是服务消费方，服务提供方地址：{"ip": "192.168.2.33", "port": "9000"}
rs.service_register("fill", "provider", {"ip": "192.168.2.33", "port": "9000"})

#获取服务fill提供者列表
rc.get_register("fill","provider")

#获取服务fill消费方列表
rc.get_register("fill","consumer")
