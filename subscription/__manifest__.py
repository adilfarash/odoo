{
    'name':"Recurring Subscription ",
    'author':'odoo',
    'version':'17.0.4.0',
    'category':'reccuring',
    'summary':'Subscription',
    'depends':['base',
               'product',
               'contacts',
               'crm',
               ],
    'license': 'GPL-2',
    'sequence':-104,
    'installation': True,
    'application': True,
    'data':[
        'security/ir.model.access.csv',
        'views/recurring_subscription_views.xml',
        'views/recurring_credit_views.xml',
        'data/seq_recurring_subscription.xml',
        'views/billing_schedule_views.xml',
        'views/partner_account_id_views.xml',
        'views/subscription_partner_views.xml',
        'views/subscription_crm_views.xml',
        ],
}