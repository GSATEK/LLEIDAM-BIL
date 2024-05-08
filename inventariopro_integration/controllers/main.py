# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
from odoo.http import request
import base64
from odoo import http

class InventarioproIntegration(http.Controller):
    

    @http.route(['/integration'], type='http', auth="public") 
    def integration(self):
        request.env['product.template'].integration_inventariopro()
        return request.redirect("/")