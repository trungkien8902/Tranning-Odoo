from odoo import fields, models, api
from odoo.api import ondelete
from odoo.fields import Many2one, Boolean


class EmployeeCertifications(models.Model):
    _name = "employee.certifications"
    _description = "Employee Certifications"

    name = fields.Char(string="Certification Name", required=True)
    description = fields.Char(string="Certification Description")
    date_received = fields.Date(string="Date Received")
    years = fields.Integer(string="Years Contributed", help="Years of experience contributed by this certification")
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')