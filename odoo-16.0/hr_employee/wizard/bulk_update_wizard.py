from odoo import models, fields, api


class EmployeeBulkUpdateWizard(models.TransientModel):
    _name = 'employee.bulk.update.wizard'
    _description = 'Employee Bulk Update Wizard'

    # Các tiêu chí lọc nhân viên
    department_id = fields.Many2one('hr.department', string="Department")
    job_id = fields.Many2one('hr.job', string="Job Position")
    min_experience = fields.Integer(string="Minimum Years of Experience", default=0)

    # Dữ liệu để cập nhật
    certification_id = fields.Many2one('employee.certification', string='Certification to Add')
    skill_id = fields.Many2one('employee.skill', string='Skill to Add')

    # Chọn nhân viên dựa trên tiêu chí
    employee_ids = fields.Many2many('hr.employee', string="Employees", compute="_compute_employees")

    @api.depends('department_id', 'job_id', 'min_experience')
    def _compute_employees(self):
        for wizard in self:
            domain = [('years_of_experience', '>=', wizard.min_experience)]
            if wizard.department_id:
                domain.append(('department_id', '=', wizard.department_id.id))
            if wizard.job_id:
                domain.append(('job_id', '=', wizard.job_id.id))
            wizard.employee_ids = self.env['hr.employee'].search(domain)

    def action_update_employees(self):
        for wizard in self:
            if not wizard.employee_ids:
                return

            for employee in wizard.employee_ids:
                # Kiểm tra điều kiện cập nhật, ví dụ: chỉ cập nhật nếu nhân viên có kinh nghiệm > 5 năm
                if employee.years_of_experience > 5:
                    if wizard.certification_id:
                        employee.certification_ids = [(4, wizard.certification_id.id)]

                    if wizard.skill_id:
                        if wizard.skill_id not in employee.skill_ids:
                            employee.skill_ids = [(4, wizard.skill_id.id)]
