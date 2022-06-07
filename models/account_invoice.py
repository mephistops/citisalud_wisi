from odoo import fields, models

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    unique_code = fields.Char(string="Token Único", copy=False)
    regime_type = fields.Char(string="Tipo de Régimen")
    document_type = fields.Char(string="Tipo de Documento")
    document_number = fields.Char(string="Número de Documento")
    last_name = fields.Char(string="Apellidos")
    first_name = fields.Char(string="Nombres")
    entry_number = fields.Char(string="Número de Ingreso")
    mpre_patient = fields.Char(string="mpre Paciente")
    