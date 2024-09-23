# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeManagement(http.Controller):
#     @http.route('/employee_management/employee_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_management/employee_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_management.listing', {
#             'root': '/employee_management/employee_management',
#             'objects': http.request.env['employee_management.employee_management'].search([]),
#         })

#     @http.route('/employee_management/employee_management/objects/<model("employee_management.employee_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_management.object', {
#             'object': obj
#         })
