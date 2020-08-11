# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsersShortcut(models.Model):
    _name = 'res.users.shortcut'
    _description = 'Shortcut menu'
    _order = 'priority asc, create_date asc'

    _sql_constraints = [
        ('shortcut_unique', 'unique(menu_id,action_id,active_id,user_id)',
         'Shortcut for this action already exists!'),
    ]

    name = fields.Char('Shortcut Name', size=64)
    icon = fields.Char(default='fa-bolt')
    priority = fields.Integer('Priority', default=1)
    user_id = fields.Many2one('res.users', 'User Ref.', required=True,
                              ondelete='cascade', index=True, default=lambda s: s._uid)
    menu_id = fields.Many2one('ir.ui.menu', ondelete='cascade')
    action_id = fields.Many2one('ir.actions.act_window', ondelete='cascade')
    active_id = fields.Integer('Active ID', default=0)

    @api.multi
    def action_remove(self):
        self.unlink()
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': self._name,
            'res_id': False,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('user_id','=', self._uid)],
            'target': 'new',
        }

    @api.model
    def get_shortcut_data(self):
        res = {
            'shortcuts': [],
            'transient_models': [],
        }
        shortcuts = self.search([('user_id', '=', self._uid)])
        transient_models = self.env['ir.model'].sudo().search([('transient', '=', True)])
        res['transient_models'] = [model.model for model in transient_models]
        for shortcut in shortcuts.filtered('menu_id'):
            _name = shortcut.menu_id.name_get()
            _name = _name[0][1] if len(_name) else ''
            _id = shortcut.menu_id.id
            res['shortcuts'].append({
                'id': shortcut.id,
                'name': shortcut.name,
                'icon': shortcut.icon,
                'menu_id': (_id, _name),
                'action_id': shortcut.action_id.id,
                'active_id': shortcut.active_id,
            })
        return res
