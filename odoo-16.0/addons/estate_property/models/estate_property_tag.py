from pkg_resources import require

from odoo import fields, models
from odoo.addons.test_convert.tests.test_env import field


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Name of Tag", required=True)
    color = fields.Integer(string="Color")