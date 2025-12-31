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
