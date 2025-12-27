from odoo import models, fields


class MaintenanceTeam(models.Model):
    _name = 'maintenance.team'
    _description = 'Maintenance Team'
    _rec_name = 'name'

    name = fields.Char(string='Team Name', required=True, tracking=True)
    member_ids = fields.Many2many('res.users', string='Team Members', tracking=True)
    equipment_ids = fields.One2many('maintenance.equipment', 'team_id',
                                    string='Equipment Assigned')
    request_ids = fields.One2many('maintenance.request', 'team_id',
                                  string='Maintenance Requests')
