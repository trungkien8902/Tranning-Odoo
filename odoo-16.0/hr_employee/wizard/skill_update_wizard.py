from odoo import models, fields, api
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SkillUpdateWizard(models.TransientModel):
    _name = 'skill.update.wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    certification_ids = fields.Many2many('employee.certification', string='Certifications')
    skill_ids = fields.Many2many('employee.skill', string='Skills')

    @api.model
    def default_get(self, fields):
        res = super(SkillUpdateWizard, self).default_get(fields)

        certification_ids = self.env.context.get('default_certification_ids', [])
        skill_ids = self.env.context.get('default_skill_ids', [])

        _logger.info('Default certifications: %s', certification_ids)
        _logger.info('Default skills: %s', skill_ids)

        if isinstance(certification_ids, list):
            res['certification_ids'] = [(6, 0, certification_ids)]
        else:
            _logger.warning('certification_ids is not a valid list: %s', certification_ids)

        if isinstance(skill_ids, list):
            res['skill_ids'] = [(6, 0, skill_ids)]
        else:
            _logger.warning('skill_ids is not a valid list: %s', skill_ids)

        return res

    def action_update_skills(self):
        for record in self:
            new_skills = record.certification_ids.mapped('related_skill_ids')

            if new_skills:
                _logger.info('Updating skills for employee %s with new skills: %s', record.employee_id.name, new_skills.ids)
                record.employee_id.skill_ids = [(6, 0, new_skills.ids)]
            else:
                raise UserError('No skills found for the selected certifications.')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Skills Wizard',
            'res_model': 'skill.update.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_id': self.employee_id.id
            }
        }
