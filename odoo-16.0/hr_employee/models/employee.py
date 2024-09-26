from odoo import fields, models, api
from odoo.tools.populate import compute


class Employee(models.Model):
    _inherit = "hr.employee"

    years_of_experience = fields.Char(compute="_compute_years_of_experience", string="Experience Year")
    certification_ids = fields.One2many('employee.certification', 'employee_ids', string="Certifications")
    skill_ids = fields.One2many('employee.skill', 'employee_ids', string="Skills")

    # @api.depends('skills_id', 'certifications_id')
    # def _compute_years_of_experience(self):
    #     for record in self:
    #         experience_from_certs = sum(cert.years for cert in record.certifications_id)
    #         experience_from_skills = sum(skill.years_of_experience for skill in record.skills_id)
    #         record.years_of_experience = max(experience_from_certs,experience_from_skills)

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for employee in self:
            years_of_experience = 0

            # Cộng số năm kinh nghiệm dựa trên chứng chỉ
            if employee.certification_ids:
                for cert in employee.certification_ids:
                    if cert.acquired_date:
                        years_of_experience += (fields.Date.today().year - cert.acquired_date.year)

            # Cộng thêm năm kinh nghiệm dựa trên kỹ năng
            for skill in employee.skill_ids:
                if skill.proficiency_level == 'beginner':
                    years_of_experience += 1
                elif skill.proficiency_level == 'intermediate':
                    years_of_experience += 2
                elif skill.proficiency_level == 'advanced':
                    years_of_experience += 3

            employee.years_of_experience = years_of_experience