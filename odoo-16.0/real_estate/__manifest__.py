{
    'name': "Real Estate Management",
    'version': '1.0',
    'author': 'Trung Kien',
    'category': 'Technology',
    'summary': 'Module Bất động sản',
    'description': 'Module Quản lý bất động sản',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/offer_views.xml',
        'views/tag_views.xml',
        'views/type_views.xml',
        # 'views/test.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}