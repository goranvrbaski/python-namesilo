__author__ = 'goran.vrbaski'


class DomainInfo:
    def __init__(self, data):
        self.auto_renew = data['namesilo']['reply']['auto_renew']
        self.created = data['namesilo']['reply']['created']
        self.expires = data['namesilo']['reply']['expires']
        self.locked = data['namesilo']['reply']['locked']
        self.private = data['namesilo']['reply']['private']
        self.status = data['namesilo']['reply']['status']
        self.traffic_type = data['namesilo']['reply']['traffic_type']
        self.name_servers = NameServers.process(data['namesilo']['reply']['nameservers'])
        self.contacts = Contact(data['namesilo']['reply']['contact_ids'])


class NameServers:
    @staticmethod
    def process(data):
        ns_list = []
        for name_server in data['nameserver']:
            ns_list.append(name_server['#text'])
        return ns_list


class Contact:
    def __init__(self, data):
        self.administrative = data['administrative']
        self.billing = data['billing']
        self.registrant = data['registrant']
        self.technical = data['technical']
