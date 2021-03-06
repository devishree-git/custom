import os
import pandas as  pd    
import re
from odoo import api, fields, models
from flask import Flask, make_response, request, send_file
import csv
from odoo.exceptions import UserError, ValidationError

"""main_product
bom_type
product_qty
product_uom_id
code
line_product_id
line_qty
line_uom
is_line"""

class ImportSol(models.TransientModel):
    _name = "import.sol"
    _description = "Import Data"

    datas = fields.Binary('Database Data')
    datas_fname = fields.Char('File Name')
    file_path = fields.Char('Import file path')

    @api.multi
    def import_partner(self):
        pt = self.file_path
        with open(pt, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                state_id = self.env['res.country.state'].search([('name', '=', row['State'])])
                country_id = self.env['res.country'].search([('name', '=', row['Country'])])
                self.env['res.partner'].create({
                                    'x_RMS_Supplier_ID':row['x_RMS_Supplier_ID'],
                                    'company_type':True,
                                    'name':row['Company Name'],
                                    'street_name':row['Street'],
                                    'street2':row['Street2'],
                                    'city':row['city'],
                                    'state_id':state_id.id,
                                    'zip':row['zip'],
                                    'country_id':country_id.id,
                                    'email':row['Email'],
                                    'website':row['Website'],
                                    'x_AccountNumber':row['x_AccountNumber'],
                                    'phone':row['Phone'],
                                    'x_FaxNumber':row['x_FaxNumber'],
                                })

    @api.multi
    def import_template(self):
        pt = self.file_path
        with open(pt, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.env['product.template'].create({
                                    'default_code':row['ItemLookupCode'],
                                    'name':row['Description'],
                                    'description':row['Description'],
                                    'standard_price':row['Cost'],
                                    'ItemID':row['ItemID'],
                                })    


    @api.multi
    def import_product(self):
        pt = self.file_path
        with open(pt, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                External_data = row['External ID'].split('_')
                External_id = External_data[-1]
                tmpl_id = self.env['product.template'].search([('ItemID', '=', str(External_id))])
                if row['Product Type'] == 'Storable Product':
                    Product_type = 'product'
                elif row['Product Type'] == 'Consumable':
                    Product_type = 'consu'
                elif row['Product Type'] == 'Service':
                    Product_type = 'service'
                categories = row['Product Category'].split('/')
                category = self.env['product.category'].search([('name', '=', categories[-1])])
                partner = self.env['res.partner'].search([('name', '=', row['Supplier'])])
                self.env['product.product'].create({
                                    'default_code':row['Internal Reference'],
                                    'barcode':row['Barcode'],
                                    'name':row['Description'],
                                    'description':row['Description'],
                                    'standard_price':row['Cost'],
                                    'ItemID':row['ItemID'],
                                    'product_tmpl_id':tmpl_id.id,
                                    'type': Product_type,
                                    'categ_id':category.id,
                                    'purchase_ok':row['Can be Purchased'],
                                    'available_in_pos': row['Available in POS'],
                                    'x_SubDescription1':row['x_SubDescription1'],
                                    'x_SubDescription2':row['x_SubDescription2'],
                                    'x_SubDescription3':row['x_SubDescription3'],

                                })
                prd = self.env['product.product'].search([('default_code','=',row['Internal Reference'])])
                self.env['product.supplier.info'].create({
                    'name':partner.id,
                    'min_qty':row['Barcode'],
                    'price':row['Sale Price'],
                    'product_id':prd.id
                })

