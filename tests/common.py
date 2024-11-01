from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase
from datetime import datetime


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        self.qm_responsible_test = self.env['res.partner'].create({
            'name': 'John Dou',
        })
        self.qm_event_reason_test = self.env['qm.event.reason'].create({
            'name': 'Test event reason',
            'description': 'Test event reason for run tests!',
        })
        self.qm_source_info_test = self.env['qm.source.information'].create({
            'name': 'Test source info',
            'description': 'Test source information for run tests!',
        })
        self.qm_complaint_test = self.env['qm.complaint'].create({
            'state': 'investigation',
            'res_partner_id': self.qm_responsible_test.id,
            'discovery_date': datetime.now(),
            'deadline_date': datetime.now() + relativedelta(days=31),
            'source_information_id': self.qm_source_info_test.id,
        })
        self.qm_claim_test = self.env['qm.claim'].create({
            'complaint_id': self.qm_complaint_test.id,
            'invoice_number': 'INV-123456',
            'batch_number': '456-1',
            'event_reason_id': self.qm_event_reason_test.id,
            'description': 'Test text!',
        })
        self.qm_investigation_test = self.env[
            'qm.internal.investigation'
        ].create({
            'complaint_id': self.qm_complaint_test.id,
            'performer_id': self.qm_responsible_test.id,
            'act_number': 'Test0001',
            'act_date': datetime.now() + relativedelta(days=12),
            'classification': 'critical',
            'state': 'at_work',
        })
        self.qm_cost_test = self.env['qm.costs'].create({
            'investigation_id': self.qm_investigation_test.id,
            'amount': 75,
            'consumption': 'Test consumption',
        })
