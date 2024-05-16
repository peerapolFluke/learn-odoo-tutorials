from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Estate Property Tag name must be unique'),
    ]
