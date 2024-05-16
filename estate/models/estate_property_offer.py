from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

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

    _sql_constraints = [
        ('check_price_positive', 'CHECK (price>0)', 'Offer price must be positive'),
    ]

    @api.depends('validity')
    def _computed_date_deadline(selfs):
        for offer in selfs:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(selfs):
        for rec in selfs:
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("This property is already accepted offer."))
        if self.property_id.selling_price > self.property_id.expected_price * 0.9 or float_is_zero(
                self.property_id.selling_price,
                precision_rounding=2):
            raise ValidationError(_("Selling price must be greater than expected price (90%)"))

        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = 'accepted'

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = 'refused'
