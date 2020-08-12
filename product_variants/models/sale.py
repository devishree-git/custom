# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleSubPart(models.Model):
    _name="sale.line.product.confg"
	
    sale_line_id = fields.Many2one('sale.order.line', string = 'SaleLine ID')
    pdt_attribute = fields.Many2one('product.attribute', string = 'Attribute', required=True)
    pdt_attribute_value = fields.Many2one('product.attribute.value', string='Attribute Values', required=True)   	
    
    @api.onchange('pdt_attribute')
    def attribute_list_generator(self):
        product_tmpl_id = self._context.get('product_tmpl_id')
        if product_tmpl_id:
            pdt_atrlist=self.env['product.template'].browse(product_tmpl_id).attribute_line_ids.mapped(lambda rec:rec.attribute_id).ids
            return {'domain':{'pdt_attribute':[('id','in',pdt_atrlist)]}}

class SaleOrderLineExtension(models.Model):
    _inherit = 'sale.order.line'
    pdt_id = fields.Many2one('product.template', string='Product')
    product_conf = fields.One2many('sale.line.product.confg','sale_line_id', string = 'Configure')
	
    @api.multi
    def update_product_attribute_line(self,line,cval_id):      
        writer = {'attribute_line_ids': [[1, line.id, {'value_ids': [(4,cval_id)]}]]}
        return self.pdt_id.write(writer)
		   
    @api.multi
    def product_search_variant(self,product_tmp,pvl):
        self.ensure_one()
        for prd_vrnt in product_tmp.product_variant_ids:
            if set(pvl) == set(prd_vrnt.attribute_value_ids.ids):
                return prd_vrnt.id    
        else:
            return
	
    @api.onchange('product_conf')
    def product_confgr(self): 
        if  len(self.product_conf) >= len(self.pdt_id.attribute_line_ids):
            conf_vals = self.product_conf.mapped(lambda x:x.pdt_attribute_value).ids   
            product_product_id = self.product_search_variant(self.pdt_id, conf_vals)
            if product_product_id:
                self.product_id = product_product_id
            else:
                for cnf_line in self.product_conf:
                    for attr_line in self.pdt_id.attribute_line_ids:
                        if cnf_line.pdt_attribute.id in attr_line.mapped('attribute_id').ids:
                            self.update_product_attribute_line(attr_line,cnf_line.pdt_attribute_value.id)
                            
                self.product_id = self.product_search_variant(self.pdt_id, conf_vals)






