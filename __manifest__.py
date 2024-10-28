# Copyright © 2024
# @author: Sergii Mozolevskyi (<mozolevskyi2010@gmail.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Quality management',
    'version': '17.0.1.0.0',
    'description': (
        'Document management Complaint.\n'
        'Conducting and recording investigations.\n'
        'Work with clients.'
        ),
    'author': 'Sergii Mozolevskyi',
    'category': 'Human Resources',
    'license': 'OPL-1',

    'depends': {
        'base',
        'product',
    },

    'data': [
        'security/ir.model.access.csv',

        'data/source_information_data.xml',
        'data/event_reason_data.xml',

        'wizard/qm_form_investigations_wizard_views.xml',

        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/quality_management_menu.xml',
        'views/qm_complaint_views.xml',
        'views/qm_source_information_views.xml',
        'views/qm_event_reason_views.xml',
        'views/qm_claim_views.xml',
        'views/qm_internal_investigation_views.xml',
        'views/qm_costs_views.xml',

        'report/qm_act_of_investigation.xml',
    ],

    'demo': [
        'demo/res_partner_demo.xml',
        'demo/product_template_demo.xml',
        'demo/qm_complaint_demo.xml',
        'demo/qm_claim_demo.xml',
        'demo/qm_internal_investigation_demo.xml',
        'demo/qm_costs_demo.xml',
    ],

    'summary': (
        'Document management Complaint.\n'
        'Conducting and recording investigations.\n'
        'Work with clients.'
        ),
    'support': 'mozolevskyi2010@gmail.com',

    'external_dependencies': {
        'python': [],
    },

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'auto_install': False,
}
