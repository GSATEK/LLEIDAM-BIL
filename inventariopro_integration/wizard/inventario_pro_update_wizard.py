from odoo import models, fields, api
import json

class InventarioproUpdateWizard(models.TransientModel):
    _name='inventariopro.update.wizard'
    _description = 'Wizard to update stock'
    

    def action_update_stock(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Ask inventariopro url",
            'url': '/integration',
            'target': 'self',
        }