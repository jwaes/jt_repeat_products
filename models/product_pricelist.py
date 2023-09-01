import json
import logging
import time
from datetime import date, datetime
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools import date_utils, xlsxwriter, io

_logger = logging.getLogger(__name__)

class Pricelist(models.Model):
    _inherit = "product.pricelist"

    product_tag_id = fields.Many2one('product.tag', string='Related Product Tag')

    def repeat_pricelist_report(self):
        now = datetime.now()
        data = {
            'model_id': self.id,
            'name': self.name,
            'generated' : now,
            'byuser': self.env.user.display_name,
        }



        # templates = self.env['product.template'].search([('all_product_tag_ids', 'in', self.product_tag_id.id, )])
        # _logger.info("Number of found templates :: %s", len(templates))   

        return {
            'type' : 'ir.actions.report',
            'data': {
                'model' : 'product.pricelist',
                'options' : json.dumps(data, default=date_utils.json_default),
                'output_format' : 'xlsx',
                'report_name' : 'Pricelist_' + self.env.company.name.strip().replace(" ", "")  + '_' + self.name.strip().replace(" ", "") + '_' + now.strftime('%Y%m%d') , },
            'report_type' : 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        # self.ensure_one()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        color_green = '#5f7568'
        color_salmon = '#fdf0e7'

        format_title = workbook.add_format({'font_size': 20, 'bold': True, 'align': 'center',})
        format_title.set_font_color(color_green)
        format_title.set_bg_color(color_salmon)
        format_product_template = workbook.add_format({'font_size': 12, 'bold': True, 'bg_color' : '#f1f1f1'})
        format_product = workbook.add_format({'font_size': 12, 'bold': False})
        format_table_header = workbook.add_format({'font_size': 13, 'bold': True, 'font_color' : color_green})
        format_currency = workbook.add_format({ 'font_size': 12, 'bold': False})
        format_currency.set_num_format('#,##0.00')
        format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

        sheet = workbook.add_worksheet('Repeat Materials')
        # sheet.set_landscape()
        # sheet.set_header('&LEauzon BV&CPage &P of &N&RGenerated on &D')

        columns = {
            "code" : {
                "idx" : 1,
                "name" : "SKU",
            },
            "product_name" : {
                "idx" : 2,
                "name" : "Product name",
            },
            "barcode" : {
                "idx" : 3,
                "name" : "GTIN-13",
            },
            "unit" : {
                "idx" : 4,
                "name" : "Unit",
            },              
            "price" : {
                "idx" : 5,
                "name" : "Unit Price",
            },  
            "currency" : {
                "idx" : 6,
                "name" : "Currency",
            },
            "pack_name" : {
                "idx" : 7,
                "name" : "Packaging",
            },              
            "pack_qty" : {
                "idx" : 8,
                "name" : "Packaging Qty",
            }, 
            "pack_barcode" : {
                "idx" : 9,
                "name" : "GTIN-14",
            },                                                              
        }


        pricelist = self.env['product.pricelist'].browse(data['model_id'])
        title = "Eauzon - Repeat Materials pricelist : " + pricelist.name

        row = 0
        # sheet.set_row(row, 40, format_title)
        sheet.merge_range(row, 0, row, len(columns) + 1, title, format_title)
        # sheet.write(row, 0, title)
        row += 2
        sheet.write(row, 0, "Generated on " +  data['generated'] + " by " + data['byuser'])
        row += 2

        for key, value in columns.items():
            sheet.write(row, value['idx'], value['name'], format_table_header)
        row += 1

        templates = self.env['product.template'].search([('all_product_tag_ids', 'in', pricelist.product_tag_id.id)])

        if pricelist.product_tag_id:
            for template in templates:
                _logger.info('TMPL: %s', template.name)
                if template.is_public_visible:
                    sheet.merge_range(row, 0, row, len(columns) + 1, template.name, format_product_template)
                    row +=1
                    for product in template.product_variant_ids:
                        product_name = product.with_context(display_default_code=False).display_name
                        if product.public_visible:
                            if len(product.packaging_ids) == 0:
                                sheet.write(row, columns['code']['idx'], product.default_code, format_product)                        
                                sheet.write(row, columns['product_name']['idx'], product_name, format_product)
                                sheet.write(row, columns['barcode']['idx'], product.barcode, format_product)
                                sheet.write(row, columns['unit']['idx'], product.uom_id.name, format_product)                                
                                sheet.write(row, columns['pack_name']['idx'], 'No packaging found')
                                row +=1
                            for packaging in product.packaging_ids:                                    
                                sheet.write(row, columns['code']['idx'], product.default_code, format_product)                        
                                sheet.write(row, columns['product_name']['idx'], product_name, format_product)
                                sheet.write(row, columns['barcode']['idx'], product.barcode, format_product)
                                sheet.write(row, columns['unit']['idx'], product.uom_id.name, format_product)
                                _logger.info('moq is %s', packaging.qty)
                                price = pricelist.get_product_price(product, packaging.qty, False)
                                _logger.info('price is %s', price)
                                sheet.write(row, columns['price']['idx'], price, format_currency)
                                sheet.write(row, columns['currency']['idx'], pricelist.currency_id.name, format_product)
                                sheet.write_number(row, columns['pack_qty']['idx'], packaging.qty, format_product)
                                sheet.write(row, columns['pack_name']['idx'], packaging.name, format_product)
                                sheet.write(row, columns['pack_barcode']['idx'], packaging.barcode, format_product)
                                row +=1
                        else:
                            _logger.info("%s is not publicly visible, not adding to pricelist", product_name)
                else:
                    _logger.info("%s is not publicly visible, not adding to pricelist",  template.name)                  


        sheet2 = workbook.add_worksheet('Price validity')
        row = 0

        cols2 = {
            "product" : {
                "idx" : 1,
                "name" : "Product",
            },
            "product_variant" : {
                "idx" : 2,
                "name" : "Product Variant",
            },
            "type" : {
                "idx" : 3,
                "name" : "Price type",
            }, 
            "fixed_price" : {
                "idx" : 4,
                "name" : "Price",
            },
            "currency" : {
                "idx" : 5,
                "name" : "Currency",
            }, 
            "min_qty" : {
                "idx" : 6,
                "name" : "Min qty",
            },                         
            "start_date" : {
                "idx" : 7,
                "name" : "Valid from date",
            },
            "end_date" : {
                "idx" : 8,
                "name" : "Valid to date",
            },                                             
        }        

        _logger.info("pricelist (%s) is %s", len(pricelist.item_ids), pricelist)

        for key, value in cols2.items():
            sheet2.write(row, value['idx'], value['name'], format_table_header)
        row += 1


        for item in pricelist.item_ids:
            _logger.info("line is %s %s", item, item.compute_price )
            if item.product_tmpl_id:
                sheet2.write(row, cols2['product']['idx'], item.product_tmpl_id.name, format_product)
            if item.product_id:
                sheet2.write(row, cols2['product_variant']['idx'], item.product_id.name, format_product)
            price_type = item.compute_price
            sheet2.write(row, cols2['type']['idx'], price_type, format_product)
            if price_type == "fixed" :
                sheet2.write(row, cols2['fixed_price']['idx'], item.fixed_price, format_currency)
            sheet2.write(row, cols2['currency']['idx'], pricelist.currency_id.name, format_product)                            
            sheet2.write_number(row, cols2['min_qty']['idx'], item.min_quantity, format_product)  
            if item.date_start:
                sheet2.write(row, cols2['start_date']['idx'], item.date_start, format_date)
            if item.date_end:
                sheet2.write(row, cols2['end_date']['idx'],  item.date_end, format_date)
            row +=1


        # sheet.autofit()
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()        