from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _description = 'Maintenance Request'
    _rec_name = 'name'

    name = fields.Char(string='Request ID', compute='_compute_name', store=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment',
                                   required=True, tracking=True)

    request_type = fields.Selection([
        ('corrective', 'Corrective (Breakdown)'),
        ('preventive', 'Preventive (Routine Checkup)')
    ],  default='corrective', string='Request Type', tracking=True)

    subject = fields.Char(string='Subject/Issue',  tracking=True)
    description = fields.Text(string='Description')
    team_id = fields.Many2one('maintenance.team', string='Assigned Team', tracking=True)
    assigned_to = fields.Many2one('res.users', string='Assigned Technician', tracking=True)
    stage = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap')
    ], default='new', string='Stage', tracking=True)
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now, readonly=True)
    scheduled_date = fields.Datetime(string='Scheduled Date', tracking=True)
    duration = fields.Float(string='Hours Spent', tracking=True)
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue', search='_search_overdue')
    equipment_category = fields.Selection([
        ('machine', 'Machine'),
        ('vehicle', 'Vehicle'),
        ('computer', 'Computer')
    ], related='equipment_id.category', string='Equipment Category')

    @api.depends('equipment_id')
    def _compute_name(self):
        """Generate request name from equipment"""
        for record in self:
            if record.equipment_id:
                record.name = f"MR-{record.equipment_id.name}-{record.id}" if record.id else f"MR-{record.equipment_id.name}"
            else:
                record.name = 'New Request'

    @api.onchange('equipment_id')
    def _onchange_equipment(self):
        """Auto-fill team and technician from equipment"""
        if self.equipment_id:
            self.team_id = self.equipment_id.team_id
            self.assigned_to = self.equipment_id.default_technician_id
            self.equipment_category = self.equipment_id.category

    @api.depends('scheduled_date', 'stage')
    def _compute_is_overdue(self):
        """Check if request is overdue (scheduled date passed and not completed)"""
        for record in self:
            if record.scheduled_date and record.stage not in ['repaired', 'scrap']:
                record.is_overdue = record.scheduled_date < datetime.now()
            else:
                record.is_overdue = False

    def _search_overdue(self, operator, value):
        """Search overdue requests"""
        if operator == '=' and value:
            return [('scheduled_date', '<', datetime.now()), ('stage', 'not in', ['repaired', 'scrap'])]
        return []

    def action_in_progress(self):
        """Move request to In Progress stage"""
        if self.stage != 'new':
            raise ValidationError("Only new requests can be moved to In Progress")
        self.stage = 'in_progress'

    def action_repair(self):
        """Move request to Repaired stage"""
        if self.stage != 'in_progress':
            raise ValidationError("Only in-progress requests can be marked as repaired")
        if not self.duration:
            raise ValidationError("Please enter hours spent before marking as repaired")
        self.stage = 'repaired'

    def action_scrap(self):
        """Move request to Scrap stage and mark equipment as inactive"""
        self.stage = 'scrap'
        if self.equipment_id:
            self.equipment_id.write({'active': False})

    @api.constrains('duration')
    def _check_duration(self):
        """Validate duration is positive"""
        for record in self:
            if record.duration and record.duration < 0:
                raise ValidationError("Hours spent cannot be negative")