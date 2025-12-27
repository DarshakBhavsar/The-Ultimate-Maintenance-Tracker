{
    'name': 'GearGuard - Maintenance Tracker',
    'version': '18.0.1.0.0',
    'category': 'Maintenance',
    'author': 'Hackathon Team',
    'depends': ['base', 'web', 'hr'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/equipment_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_request_views.xml',
    ],
    'installable': True,
    'application': True,
}
