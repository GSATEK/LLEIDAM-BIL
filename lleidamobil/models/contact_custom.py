from odoo import fields, models, api


class ContractContract(models.Model):
    _inherit = 'res.partner'

    domicili = fields.Char(string='Domicili', required=False, placeholder='0')
    poblacio = fields.Char(string='Poblacio', required=False, placeholder='0')
    telf = fields.Integer(string='Telf. Feina', required=False, placeholder='0')
    fax = fields.Integer(string='FAX', required=False, placeholder='0')
    comercial = fields.Char(string='Nom Comercial', required=False, placeholder='0')
    parella = fields.Char(string='Nom Parella', required=False, placeholder='0')
    contacte = fields.Char(string='Persona Contacte', required=False, placeholder='0')

