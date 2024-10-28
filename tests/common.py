from dateutil.relativedelta import relativedelta

from odoo import Command
from odoo.tests.common import TransactionCase
from datetime import datetime


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
