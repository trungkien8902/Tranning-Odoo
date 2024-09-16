from email.policy import default

from reportlab.graphics.transform import inverse
from reportlab.platypus.tableofcontents import delta

from odoo import fields, models, api
from datetime import timedelta
from odoo.addons.test_impex.models import field
from odoo.tools.populate import compute


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status", required=True, default='refused'
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(default=7, string="Validity (Days)", store=True)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

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
                date_deadline_renew = (record.date_deadline - record.create_date).days
                record.validity = date_deadline_renew
