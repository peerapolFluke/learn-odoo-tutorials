from odoo import fields, models, api, _


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char(string="Name")
    sequence = fields.Integer(default=1)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')

    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_offers(self):
        return {
            "name": _("Related Offers"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "estate.property.offer",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }
