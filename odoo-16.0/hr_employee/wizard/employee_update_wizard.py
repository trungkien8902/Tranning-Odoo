from odoo import models, fields, api
from odoo.exceptions import UserError


class EmployeeUpdateWizard(models.TransientModel):
    _name = 'employee.update.wizard'
    _description = 'Employee Update Wizard'

    department_id = fields.Many2one('hr.department', string="Department")
    job_id = fields.Many2one('hr.job', string="Job Position")
    min_experience = fields.Integer(string="Minimum Years of Experience", default=0)

    certification_id = fields.Many2one('employee.certification', string='Certification to Add')
    skill_id = fields.Many2one('employee.skill', string='Skill to Add')

    employee_ids = fields.Many2many('hr.employee', string="Employees")

    @api.onchange('department_id', 'job_id', 'min_experience')
    def _onchange_filter_employees(self):
        domain = [('active', '=', True)]

        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.job_id:
            domain.append(('job_id', '=', self.job_id.id))
        if self.min_experience:
            domain.append(('years_of_experience', '>=', self.min_experience))

        employees = self.env['hr.employee'].search(domain)
        self.employee_ids = [(6, 0, employees.ids)]

        if not employees:
            raise UserError("No employees found for the selected criteria.")

    def action_update_employees(self):
        if not self.employee_ids:
            raise UserError('No employees selected.')

        updated_count = 0
        for employee in self.employee_ids:
            if employee.years_of_experience >= 5:
                if self.certification_id:
                    employee.certification_ids = [(4, cert.id) for cert in self.certification_id]
                if self.skill_id:
                    employee.skill_ids = [(4, skill.id) for skill in self.skill_id]
                updated_count += 1
            else:
                raise UserError("Only employees with more than 5 years of experience can be updated.")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{updated_count} employees updated successfully.',
                'type': 'success',
                'sticky': False,
            }
        }

