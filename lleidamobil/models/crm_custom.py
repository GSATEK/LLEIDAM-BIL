from odoo import fields, models, api


class ContractContract(models.Model):
    _inherit = 'crm.lead'

    # Extra contract fields
    oferta1 = fields.Char(string='Oferta1:', required=False)
    poferta1 = fields.Float(string='Preu:', required=False, placeholder='0')
    color1 = fields.Char(string='Color:', required=False)
    pcolor1 = fields.Float(string='Preu Color:', required=False, placeholder='0')
    descompte1 = fields.Float(string='Descompte:', required=False, placeholder='0')
    pfinal1 = fields.Float(string='Preu Final:', required=False, placeholder='0', compute="_compute_get_subtotal1")
    oferta2 = fields.Char(string='Oferta2:', required=False)
    poferta2 = fields.Float(string='Preu:', required=False, placeholder='0')
    color2 = fields.Char(string='Color:', required=False)
    pcolor2 = fields.Float(string='Preu Color:', required=False, placeholder='0')
    descompte2 = fields.Float(string='Descompte:', required=False, placeholder='0')
    pfinal2 = fields.Float(string='Preu Final:', required=False, placeholder='0', compute="_compute_get_subtotal2")


    @api.onchange('poferta1')
    def _compute_get_subtotal1(self):
        for line in self:
            line.pfinal1 = line.poferta1 + line.pcolor1 - line.descompte1

    @api.onchange('poferta2')
    def _compute_get_subtotal2(self):
        for line in self:
            line.pfinal2 = line.poferta2 + line.pcolor2 - line.descompte2

    def generar_presupuesto(self):

        crm_product = self.env['product.product'].search([('name', '=', 'CRM')], limit=1)
        if not crm_product:
            crm_product = self.env['product.product'].create({
                'name': 'CRM',
                'type': 'service',
                'sale_ok': True,
                'purchase_ok': False,
            })

        sale_order_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [],
        }

        if self.oferta1:
            sale_order_vals['order_line'].append((0, 0, {
                'name': self.oferta1,
                'product_id': crm_product.id,
                'product_uom_qty': 1,
                'price_unit': self.pfinal1,
            }))

        if self.oferta2:
            sale_order_vals['order_line'].append((0, 0, {
                'name': self.oferta2,
                'product_id': crm_product.id,
                'product_uom_qty': 1,
                'price_unit': self.pfinal2,
            }))

        if sale_order_vals['order_line']:

            sale_order = self.env['sale.order'].create(sale_order_vals)

            self.quotation_count  = self.quotation_count+ 1


            return {
                'name': 'Presupuesto Creado',
                'view_mode': 'form',
                'view_id': self.env.ref('sale.view_order_form').id,
                'res_model': 'sale.order',
                'res_id': sale_order.id,
                'type': 'ir.actions.act_window',
            }
        else:
            return {
                'name': 'Advertencia',
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Advertencia',
                    'type': 'warning',
                    'message': 'Ambas ofertas están vacías. No se crearon líneas de pedido.',
                    'sticky': False,
                }
            }

