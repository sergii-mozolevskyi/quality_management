import logging
import string

from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)


class QualityManagementComplaint(models.Model):
    _name = 'qm.complaint'
    _description = 'Complaints'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Number',
        readonly=True,
        compute='_compute_name',
        store=True,
        index='trigram',
    )

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
            ('canceled', 'Canceled'),
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

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        """
        A check that does not allow you to delete records
        with claims or investigations.
        """
        self.ensure_one()
        if self.claim_ids or self.internal_investigation_ids:
            raise exceptions.UserError(
                ("You cannot delete document with claims and investigations."))

    @api.depends('state')
    def _compute_name(self):
        """
        Generates the document number according to the given algorithm
        """
        for complaint in self:
            complaint_has_name = complaint.name
            if not complaint_has_name:
                complaint_name = string.Template('$pref$number')
                complaint.name = complaint_name.substitute(
                    pref='COM-',
                    number=str(complaint.id).zfill(5),
                )

    @api.constrains('state')
    def _constrains_state(self):
        """
        Does not allow closing or canceling complaints
        with open investigations
        """
        self.ensure_one()
        if self.state == 'completed' or self.state == 'canceled':
            inv_count = self.env['qm.internal.investigation'].search_count(
                domain=[
                    ('complaint_id', '=', self.id),
                    ('state', '=', 'at_work'),
                ]
            )
            if inv_count:
                raise exceptions.UserError(
                    ("Invalid operation! Investigations did not closed!"))
