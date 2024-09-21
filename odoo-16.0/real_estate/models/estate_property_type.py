from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name asc'
    # Sắp xếp theo sequence trước rồi mới đến tên

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Type Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    partner_id = fields.Many2one('res.partner','Partner')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Number of Offers", compute='_compute_offer_count')

    # property type name: Phải là duy nhất.
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The type name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
