import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    claim_count = fields.Integer(
        compute='_compute_claims_count',
        string='Claims',
        )

    def open_claims(self):
        """
        Opens a list of selected Claims for this product, grouped by complaints
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'List of Claims',
            'res_model': 'qm.claim',
            'target': 'current',
            'view_mode': 'list',
            'view_type': 'form',
            'domain': [
                ('product_id', '=', self.id)
            ],
            'context': {'group_by': 'complaint_id'},
        }

    def _compute_claims_count(self):
        """
        Calculates the number of claims about this product
        """
        self.claim_count = self.env['qm.claim'].search_count(
            domain=[
                ('product_id', '=', self.id)
            ]
        )
