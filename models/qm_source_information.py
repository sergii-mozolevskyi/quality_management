import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class QualityManagementSourceInformation(models.Model):
    _name = 'qm.source.information'
    _description = 'Source of information'

    name = fields.Char(
        string='Name',
    )

    active = fields.Boolean(
        default=True,
        copy=False,
    )

    description = fields.Text(
        index=True,
        translate=True,
    )
