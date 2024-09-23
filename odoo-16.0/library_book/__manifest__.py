{
    'name': "Library Book",
    'version': '1.0',
    'author': 'Trung Kien',
    'category': 'Human Resources',
    'summary': 'Module Quản lý sách',
    'description': 'Module Quản lý sách',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_list_views.xml',
        'views/library_book_views.xml',
        'views/library_book_menus.xml',
        # 'views/res_partner_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}