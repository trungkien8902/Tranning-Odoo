{
    'name': "Estate Property",
    'version': '1.0',
    'author': 'Trung Kien',
    'category': 'Technology',
    'summary': 'Module Bất động sản',
    'description': 'Module Quản lý bất động sản',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}