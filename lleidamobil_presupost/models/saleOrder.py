# -*- coding: utf-8 -*-
from odoo import models, fields, api


class saleOrder(models.Model):
    _inherit = "sale.order"

    comercial = fields.Many2one(
        "res.partner", string="Comercial", domain="[('is_comercial', '=', True)]"
    )
