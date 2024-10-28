import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class QualityManagementInternalInvestigation(models.Model):
    _name = 'qm.costs'
    _description = 'Costs'

    name = fields.Char()

    investigation_id = fields.Many2one(
        comodel_name='qm.internal.investigation',
    )

    amount = fields.Float(
        string='Ammount',
        digits=[15, 2],
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
