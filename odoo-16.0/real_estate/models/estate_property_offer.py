
from odoo import fields, models, api
from datetime import timedelta
from odoo.addons.test_impex.models import field
from odoo.exceptions import UserError
from odoo.tools.populate import compute


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'),
                  ('refused', 'Refused'),
                  ('pending', 'Pending')],
        string="Status", required=True, default='pending'
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True,
                                       string="Property Type")

    validity = fields.Integer(default=7, string="Validity (Days)", store=True)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    # offer price: Phải lớn hơn 0.
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                date_deadline = (record.date_deadline - record.create_date.date()).days
                record.validity = date_deadline

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("Only one offer can be accepted for a property.")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            estate_property = self.env['estate.property'].browse(property_id)

            # Kiểm tra nếu có đề nghị hiện tại nào cao hơn đề nghị mới
            if estate_property.offer_ids.filtered(lambda o: o.price >= vals.get('price')):
                raise UserError(
                    "You cannot create an offer with a lower or equal amount than an existing offer.")

            # Cập nhật trạng thái của bất động sản thành ‘Offer Received’
            estate_property.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)