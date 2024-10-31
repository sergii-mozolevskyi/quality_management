import logging
import string

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class QualityManagementInternalInvestigation(models.Model):
    _name = 'qm.costs'
    _description = 'Costs'

    name = fields.Char(
        string='Number',
        compute='_compute_name',
        store=True,
        index='trigram',
    )

    investigation_id = fields.Many2one(
        comodel_name='qm.internal.investigation',
        required=True,
    )

    amount = fields.Float(
        string='Ammount',
        digits=[15, 2],
        required=True,
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True,
        store=True,
        readonly=False,
        default=lambda self: self.env.ref('base.USD'),
    )

    consumption = fields.Char(
        string='Consumption',
    )

    @api.depends('investigation_id')
    def _compute_name(self):
        for costs in self:
            if not costs.name:
                costs_name = string.Template('$pref$number')
                costs.name = costs_name.substitute(
                    pref='COS-',
                    number=str(costs.id).zfill(5),
                )
