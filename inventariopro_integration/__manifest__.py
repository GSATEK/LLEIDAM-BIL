# Copyright 2017-2019 MuK IT GmbH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Inventariopro integration for Odoo",
    "summary": """Pluging for integrate Inventariopro API with Odoo 15""",
    "version": "15.0.1.8.2",
    "category": "Inventory",
    "license": "LGPL-3",
    "website": "www.mises.es",
    "author": "Aarón Misis",
    "depends": [
        "stock","product_warranty"
    ],
    "data": [ 
        'views/stock_menu_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/inventario_pro_update_wizardview.xml',
        'views/product_views.xml',
        'views/sale_report_templates.xml',
        'security/ir.model.access.csv',
        'data/integration_crons.xml'
    ],
    "assets": {
    },
    "demo": [
    ],
    "images": [
        
    ],
    "application": False,
}
