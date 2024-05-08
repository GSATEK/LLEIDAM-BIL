# Copyright 2020 Akretion Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


FINANCING_TYPES = [
    ('mensual', 'Mensual'),
    ('quarterly', 'Quarterly'),
    ('biannual', 'Biannual'),
    ('anual', 'Anual'),
    ('variable','variable'),
    ('tin','TIN'),
    ('tae','TAE')
]

class SaleOrder(models.Model):
    _inherit = "sale.order"


    financing = fields.Boolean(string="Financing", default=False)
    bank_id = fields.Many2one(comodel_name="res.bank", string="Bank")
    bank_financing_id = fields.Many2one(comodel_name="bank.financing.type", string="Financing type", domain="[('bank_id','=',bank_id)]")
    financing_type =  fields.Selection(FINANCING_TYPES, string="Type", default="tin")
    month_duration = fields.Integer(string="Month duration")
    interest = fields.Float(string="Interest")
    initial_amount = fields.Monetary(string="Initial amount")
    monthly_fee = fields.Monetary(string="Monthly fee")
    financed_amount = fields.Monetary(string="Interest price")
    financed_price = fields.Monetary(string="Financed price")

    @api.depends('financed_price')
    def _compute_initial_amount(self):
        for record in self:
            if record.financed_price != record.amount_total:
                record.initial_amount = record.financed_price * record.bank_financing_id.initial_amount
            else:
                record.initial_amount = 0

    @api.depends('financed_price')
    def _compute_interest_price(self):
        for record in self:
            if record.financed_price != record.amount_total:
                record.financed_amount = record.financed_price - record.amount_total
            else:
                record.financed_amount = 0
                
    @api.depends('bank_financing_id','financed_price')
    def _compute_monthly_fee(self):
        for record in self:
            if record.financed_price != record.amount_total:
                record.monthly_fee = (record.financed_price - record.initial_amount) / record.month_duration
            else:
                record.monthly_fee = 0

    @api.depends('bank_financing_id','amount_total')
    def _compute_financed_price(self):
        for record in self:
            if record.financing:
                if record.financing_type == 'mensual':
                    record.financed_price = record.amount_total * ((1+record.interest)**record.month_duration)
                elif record.financing_type == 'quarterly':
                    record.financed_price = record.amount_total * ((1+record.interest)**(record.month_duration / 3))
                elif record.financing_type == 'biannual':
                    record.financed_price = record.amount_total * ((1+record.interest)**(record.month_duration / 6))
                elif record.financing_type == 'anual':
                    record.financed_price = record.amount_total * ((1+record.interest)**(record.month_duration / 12))
                elif record.financing_type == 'variable':
                    record.financed_price = record.amount_total * ((1+record.interest)**(record.month_duration / 12))
                else:
                    record.financed_price = record.amount_total
            else:
                record.financed_price = record.amount_total