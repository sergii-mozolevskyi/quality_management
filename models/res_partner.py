import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    complaint_ids = fields.One2many(
        comodel_name='qm.complaint',
        inverse_name='res_partner_id',
        string='Complaints',
    )

    internal_investigation_ids = fields.One2many(
        comodel_name='qm.internal.investigation',
        inverse_name='performer_id',
        string='Internal investigations',
    )
