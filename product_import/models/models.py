# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_RMS_Supplier_ID = fields.Char('RMS_Supplier_ID')
    x_rms_sup_code = fields.Char('rms_sup_code')
    x_FaxNumber = fields.Char('xFaxNumber')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    ItemID = fields.Char('ItemID')

class ProductProduct(models.Model):
    _inherit = "product.product"

    x_SubDescription1 = fields.Char('SubDescription1')
    x_SubDescription2 = fields.Char('SubDescription2')
    x_SubDescription3 = fields.Char('SubDescription3')
    x_DateCreated = fields.Char('x_DateCreated')
    x_FoodStampable = fields.Char(' x_FoodStampable')
    x_RMS_HQ_ID = fields.Char('x_RMS_HQ_ID')
    x_RMS_M1_ID = fields.Char('x_RMS_M1_ID')
    x_Department = fields.Char('X_Department')
    x_Category = fields.Char('Category')
    x_BarcodeFormat = fields.Char('BarcodeFormat')
    x_ItemType = fields.Char('ItemType')
    x_ParentItem = fields.Char('ParentItem')
    x_PictureName = fields.Char('PictureName')
    x_LastSold = fields.Char('LastSold')
    x_SaleType = fields.Char('SaleType')
