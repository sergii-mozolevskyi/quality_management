from os import write

from odoo.addons.quality_management.tests.common import TestCommon
from odoo.exceptions import UserError


class TestBaseModelActions(TestCommon):

    def test_01_complaint_state_completed(self):

        with self.assertRaises(UserError):
            self.qm_complaint_test.write({'state': 'completed'})

    def test_02_complaint_state_canceled(self):

        with self.assertRaises(UserError):
            self.qm_complaint_test.write({'state': 'canceled'})

    def test_03_complaint_compute_name(self):
        name_compute = self.qm_complaint_test.name != ''
        self.assertTrue(name_compute,
                        msg='Complaint name computed')

    def test_04_claim_compute_name(self):
        name_compute = self.qm_claim_test.name != ''
        self.assertTrue(name_compute,
                        msg='Claim name computed')

    def test_05_costs_compute_name(self):
        name_compute = self.qm_cost_test.name != ''
        self.assertTrue(name_compute,
                        msg='Costs name computed')

    def test_06_investigation_state_at_work(self):
        self.qm_investigation_test.write({'state': 'draft'})
        self.qm_complaint_test.write({'state': 'canceled'})

        with self.assertRaises(UserError):
            self.qm_investigation_test.write({'state': 'at_work'})

    def test_07_investigation_state_at_work(self):
        self.qm_investigation_test.write({'state': 'draft'})
        self.qm_complaint_test.write({'state': 'completed'})

        with self.assertRaises(UserError):
            self.qm_investigation_test.write({'state': 'at_work'})
