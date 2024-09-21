{
    'name': 'Estate Account',
    'version': '1.0',
    'depends': ['real_estate', 'account'],  # Module estate và account là bắt buộc
    'author': 'Trung Kien',
    'category': 'Real Estate',
    'description': """
    This module links the estate module with the account module.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml'
    ],
    'installable': True,
    'application': False,
}
