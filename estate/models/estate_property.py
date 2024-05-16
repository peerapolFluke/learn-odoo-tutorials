from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property Description"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled")
        ],
        required=True, copy=False, default="new"
    )
    active = fields.Boolean(default=True)
    total_area = fields.Integer(compute='_calTotalArea')
    best_price = fields.Float(compute='_findBestPrice')

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    tag_ids = fields.Many2many('estate.property.tag')

    _sql_constraints = [
        ('expected_price_positive', 'CHECK (expected_price>0)', 'Expected price must be positive'),
        ('selling_price_positive', 'CHECK (selling_price>=0)', 'Selling price must be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _calTotalArea(selfs):
        for rec in selfs:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _findBestPrice(selfs):
        for rec in selfs:
            rec.best_price = max(rec.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(selfs):
        for estate in selfs:
            if not estate.garden:
                estate.garden_area = 0
                estate.garden_orientation = None

    @api.onchange('date_availability')
    def _onchange_date_availability(selfs):
        for estate in selfs:
            if estate.date_availability < fields.Date.today():
                return {
                    "warning": {
                        "title": "Warning",
                        "message": "You select date in past"
                    }
                }

    @api.constrains('selling_price')
    def _check_selling_price(selfs):
        for estate in selfs:
            if estate.selling_price > estate.expected_price * 0.9 or float_is_zero(estate.selling_price,
                                                                                   precision_rounding=2):
                raise ValidationError(_("Selling price must be greater than expected price (90%)"))

    def action_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("You can't be canceled on sold property"))
        self.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("You can't be sold on canceled property"))
        self.state = "canceled"
        return True
