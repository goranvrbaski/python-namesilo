mocked_single_contact = dict(
    namesilo=dict(
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
                contact_id="500"
            ),
            code=300,
            detail=""
            )
        )
    )

mocked_data = {
    'namesilo': {
        'reply': {
            'code': 300,
            'detail': '',
            'balance': '500',
            'new_balance': "505",
            'available': [],
            'contact': [
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
                    contact_id="500"
                )
            ],
            'auto_renew': True,
            'created': '',
            'expires': '',
            'locked': '',
            'private': '',
            'status': '',
            'traffic_type': '',
            'nameservers': {
                'nameserver': [
                    {
                        '#text': 'name-server-1'
                    },
                    {
                        '#text': 'name-server-2'
                    },
                    {
                        '#text': 'name-server-3'
                    }
                ]
            },
            'contact_ids': {
                'administrative': '',
                'billing': '',
                'registrant': '',
                'technical': ''
            },
            'domains': {
                'domain': ['some-example-domain.com', 'example.com']
            },
            'resource_record': [
                {
                    'record_id': 'e3f383786a647e83c49c6082c7ce8015',
                    'type': 'A',
                    'host': 'some-domain.com',
                    'value': '107.161.23.204'
                }
            ],
            'record_id': 'e3f383786a647e83c49c6082c7ce8014'
        }
    }
}

