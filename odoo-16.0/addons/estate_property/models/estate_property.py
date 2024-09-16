from pkg_resources import require
from odoo import fields, models, api
from datetime import datetime, timedelta

from odoo.tools.populate import compute


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

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
