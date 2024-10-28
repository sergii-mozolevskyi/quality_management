from dateutil.relativedelta import relativedelta

from odoo.addons.quality_management.tests.common import TestCommon
from odoo.exceptions import UserError
from datetime import datetime


class TestBaseModelActions(TestCommon):

    def test_01_demo(self):
        my_bool =True
        self.assertTrue(my_bool,
                        msg='Test ok')