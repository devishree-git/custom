# -*- coding: utf-8 -*-
from odoo import models, api


class IrUiView(models.Model):
    _inherit = 'ir.ui.menu'

    @api.multi
    def unlink(self):
        res = super(IrUiView, self).unlink()
        self.env['res.users.shortcut'].search([('menu_id', '=', False)]).unlink()
        return res
