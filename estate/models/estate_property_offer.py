from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _sql_constraints = [
        ('check_price_positive', 'CHECK (price>0)', 'Offer price must be positive'),
    ]
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_computed_date_deadline', inverse='_inverse_date_deadline')

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # Override create method
    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        for val in vals:
            property_rec = self.env['estate.property'].browse(
                val['property_id']
            )
            for data in property_rec:
                if val['price'] < max(data.offer_ids.mapped('price')):
                    raise UserError(_("This property is already have more valuable offer."))
            property_rec.write({
                'state': 'received'
            })
        return res

    @api.depends('validity')
    def _computed_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        self.ensure_one()
        print(self.price, self.property_id.expected_price * 0.9)
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("This property is already accepted offer."))
        if self.price < self.property_id.expected_price * 0.9:
            raise ValidationError(_("Selling price must be greater than expected price (90%)"))

        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = 'accepted'
        self.property_id.state = 'accepted'

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = 'refused'
