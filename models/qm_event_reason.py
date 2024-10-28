import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class QualityManagementEventReason(models.Model):
    _name = 'qm.event.reason'
    _description = 'Cause of the event'

    name = fields.Char(
        string='Name',
    )

    active = fields.Boolean(
        default=True,
    )

    description = fields.Text(
        index=True,
        translate=True,
    )
