# -*- coding: utf-8 -*-
# from odoo import http


# class LleidamobilPresupost(http.Controller):
#     @http.route('/lleidamobil_presupost/lleidamobil_presupost', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lleidamobil_presupost/lleidamobil_presupost/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lleidamobil_presupost.listing', {
#             'root': '/lleidamobil_presupost/lleidamobil_presupost',
#             'objects': http.request.env['lleidamobil_presupost.lleidamobil_presupost'].search([]),
#         })

#     @http.route('/lleidamobil_presupost/lleidamobil_presupost/objects/<model("lleidamobil_presupost.lleidamobil_presupost"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lleidamobil_presupost.object', {
#             'object': obj
#         })
