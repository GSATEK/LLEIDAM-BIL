from odoo import models, fields, api, _
import logging

logger = logging.getLogger(__name__)

class SubTemplateWizard(models.Model):
    _name = 'bank.financing.type'
    _description = 'Bank financing model'

    FINANCING_TYPES = [
        ('mensual', 'Mensual'),
        ('quarterly', 'Quarterly'),
        ('biannual', 'Biannual'),
        ('anual', 'Anual'),
        ('variable','variable'),
        ('tin','TIN'),
        ('tae','TAE')
    ]
        
    name = fields.Char(string="Name")
    bank_id = fields.Many2one(comodel_name="res.bank", string="Bank",required=True)
    bank_reference = fields.Char(string="Reference")
    type =  fields.Selection(FINANCING_TYPES, string="Type", default="tin")
    interest = fields.Float(string="Interest")
    initial_amount = fields.Float(string="Initial amount %")
    min_amount = fields.Float(string="Min amount")
    max_amount = fields.Float(string="Max amount")
    month_duration = fields.Integer(string="Duration")
    start_date = fields.Date(string="Start date")
    finish_date = fields.Date(string="Valid date")

    
                                
                    
        
    