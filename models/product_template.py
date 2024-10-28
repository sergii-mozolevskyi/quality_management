import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    claim_count = fields.Integer(
        compute='_compute_claims_count',
        string='Claims',
        )

    def _compute_sales_count(self):
        self.claim_count = self.env['qm.claim'].search_count(
            domain=[
                ('product_id', '=', self.id)
            ]
        )
