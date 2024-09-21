from pkg_resources import require
from odoo import fields, models, api
from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tools.populate import compute
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    address = fields.Char(string="Address")
    expected_price = fields.Float(string="Expected Price", required=True)

    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

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

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (m²)")
    living_area = fields.Float(string="Living Area (m²)")

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    garden = fields.Boolean(string="Has a Garden")
    garden_area = fields.Float(stirng="Garden Area (m²)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    # expected_price: Phải lớn hơn 0.
    # selling_price: Phải lớn hơn hoặc bằng 0.
    # property tag name: Phải là duy nhất.
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    #  giá bán (selling price) không được thấp hơn 90% giá kỳ vọng (expected price)
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            # Kiểm tra nếu giá bán không phải là 0 (tránh kiểm tra cho giá trị mặc định 0)
            if not float_is_zero(record.selling_price, precision_digits=2):
                # So sánh giá bán với 90% của giá kỳ vọng
                min_selling_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_selling_price, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.00

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be canceled.')
            record.state = 'canceled'

    def action_offer_received(self):
        for record in self:
            record.state = 'offer_received'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('A canceled property cannot be sold.')
            record.state = 'sold'

    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties in 'New' or 'Canceled' state.")