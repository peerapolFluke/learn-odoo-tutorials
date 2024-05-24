from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'selling price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100.00
                }),
            ]
        })
        return res
