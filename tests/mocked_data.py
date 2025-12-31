mocked_single_contact = dict(
    reply=dict(
        contact=dict(
            first_name="First",
            last_name="Last",
            email="some.email@some.domain.com",
            phone="003816050005000",
            address="Fake Address 18",
            city="Zrenjanin",
            state="Vojvodina",
            country="RS",
            zip="23000",
            contact_id="500",
        ),
        code=300,
        detail="",
    )
)


mocked_data_domain_info = {
    "reply": {
        "code": 300,
        "created": "2025-12-31",
        "expires": "2026-12-31",
        "auto_renew": "No",
        "locked": "Yes",
        "private": "Yes",
        "status": "",
        "traffic_type": "Custom DNS",
        "nameservers": [
            {"nameserver": "gina.ns.cloudflare.com", "position": 1},
            {"nameserver": "will.ns.cloudflare.com", "position": 2},
        ],
        "contact_ids": {
            "registrant": "153920",
            "administrative": "153920",
            "technical": "153920",
            "billing": "153920",
        },
    }
}

mocked_data = {
    "reply": {
        "code": 300,
        "detail": "",
        "balance": "500",
        "new_balance": "505",
        "available": [],
        "contact": [
            dict(
                first_name="First",
                last_name="Last",
                email="some.email@some.domain.com",
                phone="003816050005000",
                address="Fake Address 18",
                city="Zrenjanin",
                state="Vojvodina",
                country="RS",
                zip="23000",
                contact_id="500",
            )
        ],
        "domains": [
            {
                "domain": "some-domain.com",
                "expires": "2025-08-15 00:00:00",
                "created": "2023-08-15 00:00:00",
            },
        ],
        "resource_record": [
            {
                "record_id": "e3f383786a647e83c49c6082c7ce8015",
                "type": "A",
                "host": "some-domain.com",
                "value": "107.161.23.204",
            }
        ],
        "record_id": "e3f383786a647e83c49c6082c7ce8014",
    }
}
