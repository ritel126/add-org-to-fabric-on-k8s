from kubernetes import client, config
 
 
class MyKubernetes(object):
    def __init__(self):
        self.k8s_url = 'https://10.114.201.78:6443'
        self.connect()
    def connect(self):
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = True
        with open('./ca.cert', 'r') as file:
            cacert = file.read().strip('\n')
        with open('./server.cert', 'r') as file:
            servercert = file.read().strip('\n')
        with open('./server.key', 'r') as file:
            serverkey = file.read().strip('\n')
        configuration.ssl_ca_cert = config.kube_config._create_temp_file_with_content(cacert)
        configuration.cert_file = config.kube_config._create_temp_file_with_content(servercert)
        configuration.key_file = config.kube_config._create_temp_file_with_content(serverkey)
        client.Configuration.set_default(configuration)
        self.v1 = client.CoreV1Api()
 
    def list_pods(self):
        ret = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
 
    def listnamespace(self):
        data = []
        for ns in self.v1.list_namespace().items:
          data.append(ns)
        print(data)
 
k = MyKubernetes()
k.list_pods()
k.listnamespace()
