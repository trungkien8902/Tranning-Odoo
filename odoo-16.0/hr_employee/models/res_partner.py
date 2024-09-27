from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    payment_token_count = fields.Integer(
        string="Payment Token Count",  # Đảm bảo thuộc tính string được thêm vào
        compute="_compute_payment_token_count"
    )

    def _compute_payment_token_count(self):
        for partner in self:
            partner.payment_token_count = len(partner.payment_token_ids)
