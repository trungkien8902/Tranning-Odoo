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
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/wizard_views.xml',
        'views/employee_inherit_views.xml',
        'views/certification_views.xml',
        'views/skill_views.xml',

        # 'data/cron_job.xml'
        # 'views/res_partner_views.xml'
    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
