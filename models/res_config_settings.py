# -*- coding: utf-8 -*-

from datetime import date, datetime
from odoo import fields, models, api, _
import requests
import json
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    psa_url = fields.Char(
        string="Url",
        config_parameter='invoice_config.url_body',
        default='http://186.1.162.202:8081/api/pte_oodo',
    )
    psa_username = fields.Char(
        string="username",
        config_parameter='invoice_config.username',
        default='1045693633',
    )
    psa_password = fields.Char(
        string="password",
        config_parameter='invoice_config.password',
        default='12345',
    )
    psa_hash_key = fields.Char(
        string="hash_key",
        config_parameter='invoice_config.hash_key',
        default='8606da74dd0724699bc874bc9348c678',
    )
    psa_date_ini = fields.Char(
        string="Fecha Inicial",
        config_parameter='invoice_config.date_ini',
        default='2021-08-01',
    )
    psa_date_end = fields.Char(
        string="Fecha Final",
        config_parameter='invoice_config.date_end',
        default='2021-08-01',
    )

    def get_invoice(self):
        _logger.info('get_invoice')

        response = requests.post(self.psa_url,
                                auth=(self.psa_username, self.psa_password),
                                headers={'Content-Type': 'application/json'},
                                json={
                                    "hash_key": self.psa_hash_key,
                                    "json": {
                                        "fecha_ini": self.psa_date_ini,
                                        "fecha_fin": self.psa_date_end
                                    }
                                })
                                
        return json.loads(response.text)

    @api.multi
    def create_invoice(self):
        lab_req_objs = self.get_invoice()

        account_invoice_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line']

        for lab_req_obj in lab_req_objs['data']:
            domain = [
                ('unique_code', '=', lab_req_obj['unique_code'])
            ]

            invoice = account_invoice_obj.search(domain, limit=1)
            if not invoice:
                new_invoice = account_invoice_obj.create({
                    'partner_id': '1',
                    'date': datetime.now(),
                    'date_invoice': datetime.now(),
                    'reference': 'Test Module',
                    'unique_code': lab_req_obj['numero_ingreso'],
                    'regime_type': lab_req_obj['tipo_regimen'],
                    'document_type': lab_req_obj['tipo_documento'],
                    'document_number': lab_req_obj['cedula'],
                    'last_name': lab_req_obj['apellido'],
                    'first_name': lab_req_obj['nombre'],
                    'entry_number': lab_req_obj['numero_ingreso'],
                    'mpre_patient': lab_req_obj['mpre_paciente'],
                })
                _logger.debug('Factura creada')
            else:
                _logger.debug('Factura ya existe')
                raise UserError(_('La factura ya existe'))
