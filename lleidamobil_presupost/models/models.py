# -*- coding: utf-8 -*-
from odoo import models, fields, api


# class lleidamobil_presupost(models.Model):
#     _name = 'lleidamobil_presupost.lleidamobil_presupost'
#     _description = 'lleidamobil_presupost.lleidamobil_presupost'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class resPartner(models.Model):
    _inherit = "res.partner"

    is_comercial = fields.Boolean(string="Es comercial", default=False)
