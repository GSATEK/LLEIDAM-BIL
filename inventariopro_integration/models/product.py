from odoo import models, fields, api
import requests
import xml.etree.ElementTree as ET
import base64

DISCARD_TAGS = [
        'id',
        'dealername',
        'dealerid',
        'email',
        'title',
        'content',
        'price',
        'financed_price',
        'monthly financing_fee',
        'vat',
        'vin',
        'month',
        'availability',
        'store',
        'city',
        'postcode',
        'region',
        'address',
        'pictures',
        'date',
        'last_update',
        'interior_360',
        'exterior_360',
        'uso_comercial',
        'video',
        'jato_id',
        'guarantee',
        'numberplate',
        'equipment'
        
    ]

class ProductTemplate(models.Model):
    _inherit = [
        "product.template",
    ]

    extra_details = fields.Boolean(string="Extra details", default=False)
    technical_details = fields.Many2many(relation='product_template_product_attribute_line_financing_extra_rel',comodel_name="product.template.attribute.line.financing",string="Tecnical details")

    @api.model
    def integration_inventariopro(self):
        res = requests.get(self.env['ir.config_parameter'].sudo().get_param('inventariopro_integration.inventario_pro_url') or '')
        if res.status_code == 200:
            file =  open('/tmp/stock_update.xml', 'w').close()
            file =  open('/tmp/stock_update.xml', 'r+')
            file.write(res.text)
            file.close()
            parser = ET.XMLParser(encoding="iso-8859-1")
            tree = ET.parse('/tmp/stock_update.xml', parser=parser)
            root = tree.getroot()
            ids = []

            for child in root:
                values = {}
                image = False
                lines = self.env['product.template.attribute.line.financing']
                for record in child:
                    values[record.tag] = record.text
                    if record.tag == 'pictures':
                        image = record[0][0].text
                image = base64.b64encode(requests.get(image).content)
                ids.append(values['id'])
                for val in values:
                    if val not in DISCARD_TAGS:
                        container = val.split('_')
                        att_name = ''
                        for record in container:
                            if att_name != '':
                                att_name += ' '
                            att_name += record
                        att = self.env['product.attribute'].search([('inventario_pro_code','=', att_name)])
                        if not att and att_name != '':
                            att = self.env['product.attribute'].create({
                                'name': att_name,
                                'inventario_pro_code': att_name,
                            })
                        att_value = self.env['product.attribute.value'].search([('name','=', values[val]),('attribute_id',"=", att.id)])
                        if not att_value:
                            if values[val]:
                                if len(values[val]) > 2700:
                                    values[val] = values[val][0:2700]
                                attribute_value = self.env['product.attribute.value'].search([('name','=',values[val]),('attribute_id','=',att.id)])
                                if not attribute_value:
                                    att_value = self.env['product.attribute.value'].create({
                                        'name': values[val],
                                        'attribute_id': att.id
                                    })
                                
                        if values[val]:
                            lines += self.env['product.template.attribute.line.financing'].create({
                                        'value_ids': att_value,
                                        'attribute_id': att.id
                                    })

                product = self.env['product.template'].search([('barcode','=', values['id']),('active','=',True)])
                if not product:
                    template = self.env['product.template'].create({
                                'name': values['title'],
                                'detailed_type': 'product',
                                'type':'product',
                                'list_price': values['price'],
                                'sale_ok': True,
                                'purchase_ok': False,
                                'has_configurable_attributes': False,
                                'barcode': values['id'],
                                'default_code': values['numberplate'],
                                'extra_details': True,
                                'technical_details': lines,
                                'taxes_id': self.env.company.account_sale_tax_id,
                                'image_1920': image,
                                'warranty': values['guarantee'],
                                'warranty_type': 'month'
                            })
                    
                    variant  = self.env['product.product'].search([('product_tmpl_id','=', template.id)])
                    warehouse = self.env['stock.warehouse'].search(
                        [('company_id', '=', self.env.company.id)], limit=1
                    )
                    # Before creating a new quant, the quand `create` method will check if
                    # it exists already. If it does, it'll edit its `inventory_quantity`
                    # instead of create a new one.
                    self.env['stock.quant'].with_context(inventory_mode=True).create({
                        'product_id': variant.id,
                        'location_id': warehouse.lot_stock_id.id,
                        'inventory_quantity': 1,
                    })._apply_inventory()
                else:
                    product.write({
                                'name': values['title'],
                                'list_price': values['price'],
                                'barcode': values['id'],
                                'default_code': values['numberplate'],
                                'technical_details': lines,
                                'image_1920': image,
                                'extra_details': True,
                                'warranty': values['guarantee'],
                                'warranty_type': 'month',
                                'taxes_id': self.env.company.account_sale_tax_id
                            })

            file =  open('/tmp/stock_update.xml', 'w').close()
            products = self.env['product.template'].search([('barcode','!=','')])
            for product in products:
                if product.barcode not in ids:
                    product.write({'active': False})        
        

class ProductTemplateAttributeLineFinancing(models.Model):
    _name="product.template.attribute.line.financing"
    _description = 'Product Template Attribute Line Financing'

    attribute_id = fields.Many2one(comodel_name="product.attribute",string="Attribute")
    value_ids = fields.Many2many(comodel_name="product.attribute.value", domain="[('attribute_id','=', attribute_id)]",string="Value",
                                 relation='product_template_product_attribute_line_financing_rel')

class ProductAttribute(models.Model):
    _inherit = [
        "product.attribute",
    ]

    inventario_pro_code = fields.Char(string="Code")

    
    _sql_constraints = [
        ('inventario_pro_code_uniq', 'unique(inventario_pro_code)', "Only one attribute can be imported with the same code."),
    ]
   