import logging

from odoo import models, fields, api, exceptions, Command

_logger = logging.getLogger(__name__)


class QualityManagementFormAnInvestigations(models.TransientModel):
    _name = 'qm.form.investigations.wizard'
    _description = 'Mass create investigations'

    complaint_id = fields.Many2one(
        comodel_name='qm.complaint',
        string='Complaint'
    )

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Responsible for investigation'
    )

    classification = fields.Selection(
        selection=[
            ('critical', 'Critical'),
            ('major', 'Major'),
            ('other', 'Other'),
        ],
        default='major',
    )

    investigation_ids = fields.Many2many(
        comodel_name='qm.internal.investigation',
        readonly=True,
    )

    claim_ids = fields.One2many(
        comodel_name='qm.claim',
        inverse_name='complaint_id',
        string='Claims',
        readonly=True,
    )

    def create_investigations(self):
        self.ensure_one()
        investigation_ids = self.env['qm.internal.investigation'].search(domain=[('complaint_id', '=', self.complaint_id)])
        if len(investigation_ids):
            raise exceptions.UserError(
                ("Investigations already exist. Choose another complaint.")
            )
        claim_ids = self.env['qm.claim'].search(domain=[('complaint_id', '=', self.complaint_id)])
        if not len(claim_ids):
            raise exceptions.UserError(
                ("There are no Claims in current Complaint.")
            )
        count = 0
        for claim in claim_ids:
            count += 1
            self.env['qm.internal.investigation'].create({
                'name': 'INV-' + count + ' / ' + self.complaint_id.name,
                'complaint_id': self.complaint_id,
                'performer_id': self.res_partner_id,
                'reason_description': claim.description,
                'classification': self.classification,
            })

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')
        complaint_id = self.env[active_model].browse(active_ids)[0]
        res['complaint_id'] = complaint_id

        res_invest_ids = self.env['qm.internal.investigation'].search(domain=[('complaint_id', '=', complaint_id.id)])
        print(res_invest_ids)
        for invest in res_invest_ids:
            self['investigation_ids'] = Command.link(invest.id)
        return res
