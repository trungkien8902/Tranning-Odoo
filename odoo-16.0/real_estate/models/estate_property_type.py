from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char(string="Type Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    partner_id = fields.Many2one('res.partner','Partner')
    # property type name: Phải là duy nhất.
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The type name must be unique.')
    ]