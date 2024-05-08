# Copyright 2023 Aarón Misis Esteban <www.mises.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Financing",
    "category": "Sale",
    "license": "AGPL-3",
    "author": "Aarón Misis",
    "version": "15.0.1.0.0",
    "website": "www.mises.es",
    "summary": "Allows define a financing in a sale order.",
    "depends": [
        "sale",
        "account",
        "base",
        "product_warranty"
    ],
    "data": [
        'views/bank_financing_views.xml',
        'views/menues.xml',
        'views/sale_order.xml',
        'views/sale_report_templates.xml',
        'security/ir.model.access.csv'
    ],
    "installable": True,
}
