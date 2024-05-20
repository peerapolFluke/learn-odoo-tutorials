from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char(string="Name")
    sequence = fields.Integer(default=1)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
