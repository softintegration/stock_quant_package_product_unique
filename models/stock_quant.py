# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class QuantPackage(models.Model):
    """ Inherit stock package to constraint one product by package """
    _inherit = "stock.quant.package"

    product_id = fields.Many2one('product.product',string='Product',compute='_compute_product',store=True,readonly=True)


    @api.depends('quant_ids')
    def _compute_product(self):
        for each in self:
            # FIXME : can we do better than this (check the unicity out of the compute field)
            each._check_product_unicity()
            each.product_id = each.quant_ids and each.quant_ids.mapped("product_id")[0] or False


    def _check_product_unicity(self):
        for each in self:
            if each.quant_ids and len(each.quant_ids.mapped('product_id')) > 1:
                raise ValidationError(_("Package with different products is not allowed,please check the package %s!")%each.name)

