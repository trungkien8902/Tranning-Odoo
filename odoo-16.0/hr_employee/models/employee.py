from email.policy import default

from odoo import fields, models, api
from odoo.exceptions import UserError, AccessError
from odoo.tools.populate import compute


class Employee(models.Model):
    _inherit = "hr.employee"

    certification_count = fields.Integer(compute='_compute_certification_count', string="Certifications")
    skill_count = fields.Integer(compute='_compute_skill_count', string="Skills")

    years_of_experience = fields.Integer(compute="_compute_years_of_experience", string="Experience Year")
    certification_ids = fields.Many2many(
        'employee.certification',
        'employee_certification_rel',
        'employee_id',
        'certification_id',
        string="Certifications"
    )
    skill_ids = fields.Many2many(
        'employee.skill',
        'employee_skill_rel',
        'employee_id',
        'skill_id',
        string="Skills"
    )

    manage_certifications = fields.Boolean(
        string="Manage Certifications",
        groups="hr.group_hr_manager"
    )
    manage_skills = fields.Boolean(
        string="Manage Skills",
        groups="hr.group_hr_manager"
    )

    @api.depends('certification_ids')
    def _compute_certification_count(self):
        for employee in self:
            employee.certification_count = len(employee.certification_ids)

    @api.depends('skill_ids')
    def _compute_skill_count(self):
        for employee in self:
            employee.skill_count = len(employee.skill_ids)

    def action_view_certifications(self):
        self.ensure_one()
        return {
            'name': 'Certifications',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'employee.certification',
            'domain': [('employee_ids', 'in', self.id)],
            'context': {
                'default_employee_ids': [(6, 0, [self.id])],
                'create': True,
            },
            'target': 'current',
        }

    def action_view_skills(self):
        self.ensure_one()
        return {
            'name': 'Skills',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'employee.skill',
            'domain': [('employee_ids', 'in', self.id)],
            'context': {
                'default_employee_ids': [(6, 0, [self.id])],
                'create': True,
            },
            'target': 'current',
        }

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for employee in self:
            years_of_experience = 0
            if employee.certification_ids:
                for cert in employee.certification_ids:
                    if cert.date_received:
                        years_of_experience += (fields.Date.today().year - cert.date_received.year)
            for skill in employee.skill_ids:
                if skill.proficiency_level == 'beginner':
                    years_of_experience += 1
                    # print(self.env.ref('hr_employee.group_employee_experience_manager_advanced').id)
                elif skill.proficiency_level == 'intermediate':
                    years_of_experience += 2
                elif skill.proficiency_level == 'advanced':
                    years_of_experience += 3
                elif skill.proficiency_level == 'expert':
                    years_of_experience += 4
            employee.years_of_experience = years_of_experience

    def action_update_employee_skills(self):
        if not self.skill_ids:
            raise UserError("Please select at least one skill to update.")

        for skill in self.skill_ids:
            if skill not in self.skill_ids:
                self.skill_ids = [(4, skill.id)]

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Skills updated successfully for this employee.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_update_employee_certifications(self):
        if not self.certification_ids:
            raise UserError("Please select at least one certification to update.")

        for certification in self.certification_ids:
            if certification not in self.certification_ids:
                self.certification_ids = [(4, certification.id)]

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Certifications updated successfully for this employee.',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.onchange('years_of_experience', 'certification_ids', 'skill_ids')
    def _check_manage_certification_permissions(self):
        for employee in self:
            if employee.certification_count >= 3:
                employee.manage_certifications = True
            else:
                employee.manage_certifications = False

    def _check_manage_skill_permissions(self):
        for employee in self:
            if employee.skill_count >= 3 and any(skill.name == 'manage' for skill in employee.skill_ids):
                employee.manage_skills = True
            else:
                employee.manage_skills = False

    def unlink(self):
        if self.env.user.has_group('hr.group_hr_manager'):
            raise AccessError("You do not have permission to delete employees.")
        return super(Employee, self).unlink()

