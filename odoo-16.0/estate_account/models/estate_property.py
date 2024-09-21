from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Gọi phương thức gốc để đảm bảo logic ban đầu vẫn hoạt động
        super(EstateProperty, self).action_sold()

        for record in self:
            # Kiểm tra xem người mua đã được chỉ định chưa
            if not record.buyer_id:
                raise UserError("Cannot create an invoice without a buyer.")

            # Tạo hóa đơn với thông tin khách hàng và loại hóa đơn
            invoice_vals = {
                'partner_id': record.buyer_id.id,  # Người mua từ estate.property
                'move_type': 'out_invoice',  # Hóa đơn bán hàng (Customer Invoice)
                'invoice_date': fields.Date.today(),  # Ngày tạo hóa đơn
                'invoice_line_ids': [
                    # Dòng hóa đơn 6% giá bán
                    (0, 0, {
                        'name': 'Selling Price - 6%',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,  # 6% của giá bán
                    }),
                    # Dòng hóa đơn phí hành chính 100.00
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,  # Phí hành chính cố định
                    }),
                ]
            }

            # Tạo bản ghi account.move với các dòng hóa đơn
            self.env['account.move'].create(invoice_vals)
