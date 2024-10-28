import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class QualityManagementComplaint(models.Model):
    _name = 'qm.complaint'
    _description = 'Complaints'
    _inherit = ['mail.thread']

    name = fields.Char()

    active = fields.Boolean(
        default=True,
        copy=False,
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('at_work', 'At work'),
            ('investigation', 'Investigation'),
            ('completed', 'Completed'),
            ('canceled', 'Cancelled'),
        ],
        default='draft',
    )

    description = fields.Text(
        index=True,
        translate=True,
    )

    comment = fields.Text(
        string='Comment',
        translate=True,
    )

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Responsible',
        default=lambda self: self.env.user.partner_id.id,
        copy=False,
        required=True,
    )

    discovery_date = fields.Date(
        string='Date of discovery',
        required=True,
    )

    deadline_date = fields.Date(
        string='Deadline',
        required=True,
    )

    source_information_id = fields.Many2one(
        comodel_name='qm.source.information',
        default=lambda self: self.env.ref(
            'quality_management.complaint_from_client'
            ),
        required=True,
    )

    counterparty_id = fields.Many2one(
        comodel_name='res.partner',
        string='Counterparty',
    )

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )

    claim_ids = fields.One2many(
        comodel_name='qm.claim',
        inverse_name='complaint_id',
        string='Claims',
    )

    internal_investigation_ids = fields.One2many(
        comodel_name='qm.internal.investigation',
        inverse_name='complaint_id',
        string='Internal investigations',
    )
