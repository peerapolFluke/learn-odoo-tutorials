from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Estate Property Tag name must be unique'),
    ]
    _order = 'name asc'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
