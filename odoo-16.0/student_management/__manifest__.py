{
    'name': "Student Management",
    'version': '1.0',
    'author': 'Trung Kien',
    'category': 'Human Resources',
    'summary': 'Module Quản lý học sinh',
    'description': 'Module Quản lý học sinh',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menus.xml',
        'views/res_partner_views.xml',
        # 'views/student_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}