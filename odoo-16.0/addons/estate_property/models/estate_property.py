from pkg_resources import require
from odoo import fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    address = fields.Char(string="Address")
    expected_price = fields.Float(string="Expected Price", required=True)

    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90),
        copy=False
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    active = fields.Boolean(string="Active", default=True)

    # Thêm trường state với giá trị mặc định là "New"
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string="Status",
        required=True,
        default='new',  # Giá trị mặc định là "New"
        copy=False  # Không sao chép khi tạo bản sao
    )

