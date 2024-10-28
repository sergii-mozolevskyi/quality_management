import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class QualityManagementClaim(models.Model):
    _name = 'qm.claim'
    _description = 'Claims'

    name = fields.Char()  # invoice_number / product_id.name

    active = fields.Boolean(
        default=True,
        copy=False,
    )

    complaint_id = fields.Many2one(
        comodel_name='qm.complaint',
        string='Complaint'
    )

    discovery_date = fields.Date(
        related='complaint_id.discovery_date',
        store=True,
    )

    product_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
    )

    uom_name = fields.Char(
        string='Unit of Measure',
        related='product_id.uom_name',
        readonly=True)

    quantity = fields.Float(
        string='quantity',
    )

    invoice_number = fields.Char(
        string='Invoce number',
    )

    batch_number = fields.Char(
        string='Batch number',
    )

    event_reason_id = fields.Many2one(
        comodel_name='qm.event.reason',
        string='Event reason',
        required=True,
    )

    description = fields.Text(
        string='Description of non-conformity',
        index=True,
        translate=True,
    )

    @api.constrains('quantity')
    def _constraint_negative_value(self):
        self.ensure_one()
        if self.quantity < 0:
            self.quantity *= -1
