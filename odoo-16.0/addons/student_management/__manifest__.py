{
    'name': 'Student Management',
    'version': '1.0',
    'author': 'Trung Kien',
    'category': 'Education',
    'summary': 'Module quản lý sinh viên',
    'description': 'Module này dùng để quản lý thông tin sinh viên trong hệ thống Odoo.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/contact_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
