import logging
import string

from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)


class QualityManagementInternalInvestigation(models.Model):
    _name = 'qm.internal.investigation'
    _description = 'Internal investigations'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Number',
        compute='_compute_name',
        store=True,
        index='trigram',
    )

    complaint_id = fields.Many2one(
        comodel_name='qm.complaint',
        string='Complaint',
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

    def _get_report_base_filename(self):
        file_name = string.Template('$name($number_act - $date_act)')
        return file_name.substitute(
            name=self.name,
            number_act=self.act_number,
            date_act=self.act_date,
        )

    @api.depends('complaint_id')
    def _compute_name(self):
        for inv in self:
            if not inv.name:
                inv_name = string.Template('$pref$number')
                inv.name = inv_name.substitute(
                    pref='INV-',
                    number=str(inv.id).zfill(5),
                )

    @api.constrains('state')
    def _constrains_state(self):
        self.ensure_one()
        if not self.state == 'at_work':
            return True

        if not self.complaint_id:
            return True

        comp_state = self.complaint_id.state
        if comp_state == 'completed' or comp_state =='canceled':
            raise exceptions.UserError(
                ("Invalid operation! Complaint closed!"))
