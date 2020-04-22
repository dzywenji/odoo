from odoo import models, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _name = "validate.account.move"
    _description = "Validate Account Move"

    def validate_move(self):
        context = dict(self._context or {})
        moves = self.env['account.move'].browse(context.get('active_ids'))
<<<<<<< HEAD
        move_to_post = moves.filtered(lambda m: m.state == 'draft').sorted(lambda m: (m.date, m.ref or '', m.id))
=======
        move_to_post = moves.filtered(lambda m: m.state == 'draft')
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
        if not move_to_post:
            raise UserError(_('There are no journal items in the draft state to post.'))
        move_to_post.post()
        return {'type': 'ir.actions.act_window_close'}
