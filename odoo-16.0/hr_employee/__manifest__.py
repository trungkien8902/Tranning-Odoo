# -*- coding: utf-8 -*-
{
    'name': "Employee Management",
    'description': """
        Long description of module's purpose
    """,
    'author': "Trung Kien",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/employee_inherit_views.xml'
    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
