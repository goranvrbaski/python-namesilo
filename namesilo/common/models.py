from datetime import datetime
from dataclasses import dataclass

__author__ = "goran.vrbaski"

from typing import List


class Contact:
    def __init__(self, data):
        self.administrative = data["administrative"]
        self.billing = data["billing"]
        self.registrant = data["registrant"]
        self.technical = data["technical"]


@dataclass
class DomainInfo:
    auto_renew: bool
    created: datetime
    expires: datetime
    locked: bool
    private: bool
    status: str
    traffic_type: str
    name_servers: List[str]
    contacts: "Contact"

    @classmethod
    def from_api(cls, data: dict) -> "DomainInfo":
        reply = data["reply"]
        # test = {
        #     'code': 300,
        #     'detail': 'success',
        #     'created': '2025-12-31',
        #     'expires': '2026-12-31',
        #     'status': 'Active',
        #     'locked': 'Yes',
        #     'private': 'Yes',
        #     'auto_renew': 'No',
        #     'traffic_type': 'Custom DNS',
        #     'email_verification_required': 'No',
        #     'portfolio': 'N/A',
        #     'forward_url': 'N/A',
        #     'forward_type': 'N/A',
        #     'nameservers': [{'nameserver': 'gina.ns.cloudflare.com', 'position': 1}, {'nameserver': 'will.ns.cloudflare.com', 'position': 2}],
        #     'contact_ids': {'registrant': '153920', 'administrative': '153920', 'technical': '153920', 'billing': '153920'}
        # }

        return cls(
            auto_renew=reply["auto_renew"],
            created=datetime.fromisoformat(reply["created"]),
            expires=datetime.fromisoformat(reply["expires"]),
            locked=reply["locked"],
            private=reply["private"],
            status=reply["status"],
            traffic_type=reply["traffic_type"],
            name_servers=NameServers.process(reply["nameservers"]),
            contacts=Contact(reply["contact_ids"]),
        )


class NameServers:
    @staticmethod
    def process(data):
        ns_list = []
        for name_server in data:
            ns_list.append(name_server["nameserver"])
        return ns_list
