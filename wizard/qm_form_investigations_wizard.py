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


    def create_investigations(self):
        self.ensure_one()
        investigation_ids = self.env['qm.internal.investigation'].search(
            domain=[('complaint_id', '=', self.complaint_id.id)]
        )
        if len(investigation_ids):
            raise exceptions.UserError(
                ("Investigations already exist. Choose another complaint.")
            )
        claim_ids = self.env['qm.claim'].search(
            domain=[('complaint_id', '=', self.complaint_id.id)]
        )
        if not len(claim_ids):
            raise exceptions.UserError(
                ("There are no Claims in current Complaint.")
            )
        count = 0
        for claim in claim_ids:
            count += 1
            self.env['qm.internal.investigation'].create({
                'name': 'INV-' + str(count) + ' / ' + self.complaint_id.name,
                'complaint_id': self.complaint_id.id,
                'performer_id': self.res_partner_id.id,
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
        return res

class QualityManagementInvestigationLinesWizard(models.TransientModel):
    _name='qm.investigation.lines.wizard'
    name = fields.Char()
