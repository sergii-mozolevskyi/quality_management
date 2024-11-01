import logging
import string

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class QualityManagementClaim(models.Model):
    _name = 'qm.claim'
    _description = 'Claims'

    name = fields.Char(
        string='Number',
        compute='_compute_name',
        store=True,
        index='trigram',
    )

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
        """
        Does not allow specifying negative values
        """
        self.ensure_one()
        if self.quantity < 0:
            self.quantity *= -1

    @api.depends('invoice_number')
    def _compute_name(self):
        """
        Generates the document number according to the given algorithm
        """
        for claim in self:
            claim_has_name = claim.name and claim.name != '/'
            if not claim_has_name:
                claim_name = string.Template('$pref$number/$invoice')
                claim.name = claim_name.substitute(
                    pref='CL-',
                    number=claim.id,
                    invoice=claim.invoice_number or '0',
                )
