from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unsplash_app_id = fields.Char(
        string="Unsplash App ID",
        config_parameter='hr_employee.unsplash_app_id'
    )
