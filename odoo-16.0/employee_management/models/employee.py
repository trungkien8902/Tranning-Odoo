

from odoo import fields, models
from odoo.addons.test_impex.models import field


class Employee(models.Model):
    _inherit = 'hr'

    years_of_experience = fields.Char(string="Experience Year")
    certifications = fields.Char(string="Certifications")
    skills = fields.Char(string="Skills")
