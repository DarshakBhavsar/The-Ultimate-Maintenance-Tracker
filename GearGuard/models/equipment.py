import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,date


class Equipment(models.Model):
    _name = 'maintenance.equipment'
    _description = 'Equipment/Asset'
    _rec_name = 'name'

    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    category = fields.Selection([
        ('machine', 'Machine'),
        ('vehicle', 'Vehicle'),
        ('computer', 'Computer')
    ], required=True, string='Category', tracking=True)
    purchase_date = fields.Date(string='Purchase Date', tracking=True, required=True)
    warranty_end = fields.Date(string='Warranty End Date', tracking=True, required=True)
    location = fields.Char(string='Location', tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', tracking=True)
    employee_id = fields.Many2one('res.partner', string='Assigned Employee', tracking=True)
    team_id = fields.Many2one('maintenance.team', string='Maintenance Team',
                              required=True, tracking=True)
    default_technician_id = fields.Many2one('res.users', string='Default Technician', tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    maintenance_request_ids = fields.One2many('maintenance.request', 'equipment_id',
                                              string='Maintenance Requests')
    maintenance_count = fields.Integer(string='Open Maintenance Requests',
                                       compute='_compute_maintenance_count')

    @api.constrains('purchase_date', 'warranty_end')
    def _check_dates(self):
        for record in self:
            if record.purchase_date and record.warranty_end:
                if record.purchase_date > record.warranty_end:
                    raise ValidationError("Purchase Date must be before Warranty End Date.")

    @api.depends('maintenance_request_ids.stage')
    def _compute_maintenance_count(self):
        """Count open maintenance requests (not in scrap or repaired stage)"""
        for record in self:
            record.maintenance_count = len(
                record.maintenance_request_ids.filtered(
                    lambda r: r.stage in ['new', 'in_progress']
                )
            )

    def action_maintenance(self):
        self.ensure_one()

        Maintenance = self.env['maintenance.request']
        request = Maintenance.search([('equipment_id', '=', self.id)], limit=1)
        today = datetime.today()

        if not request:
            request = Maintenance.create({
                'name': f'Maintenance for {self.name}',
                'equipment_id': self.id,
                'request_type':"corrective",
                "subject": 'Hello'

            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Requests',
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,list,form',
            'domain': [('equipment_id', '=', self.id)],
            'target': 'current',
        }