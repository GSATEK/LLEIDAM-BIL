from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventario_pro_url = fields.Char(
        string="Integration URL",
        config_parameter='inventariopro_integration.inventario_pro_url',
    )
