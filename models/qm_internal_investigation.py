import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class QualityManagementInternalInvestigation(models.Model):
    _name = 'qm.internal.investigation'
    _description = 'Internal investigations'
    _inherit = ['mail.thread']

    name = fields.Char()

    complaint_id = fields.Many2one(
        comodel_name='qm.complaint',
        string='Complaint'
    )

    performer_id = fields.Many2one(
        comodel_name='res.partner',
        string='The performer',
    )

    participants_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Participants',
        help='Participants in the investigation of the incident',
        relation='qm_investigation_res_partner_rel',
        column1='qm_internal_investigation_id',
        column2='res_partner_id',
    )

    act_number = fields.Char(
        string='Act number',
    )

    act_date = fields.Date(
        string='Act date',
    )

    reason_description = fields.Text(
        string='The reason for the discrepancy',
    )

    classification = fields.Selection(
        selection=[
            ('critical', 'Critical'),
            ('major', 'Major'),
            ('other', 'Other'),
        ],
        default='major',
    )

    result_description = fields.Text(
        string='The result of the investigation',
    )

    costs_ids = fields.One2many(
        comodel_name='qm.costs',
        string='Costs',
        inverse_name='investigation_id',
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('at_work', 'At work'),
            ('done', 'Done'),
            ('canceled', 'Canceled'),
        ],
        default='draft',
    )
