#! /usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import sys
import cgi
import os
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

reload(sys)
sys.setdefaultencoding('utf-8')

class SinhoPresent:
   
   def render_template(self, template_filename, context):
      return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

   def presentation(self, data, who):
      total_list = 0
      list_code = []
      dict_code = {}
      dict_name = {}
      dict_pricePer = {}
      dict_startPricePer = {}
      dict_curPrice = {}
      dict_accSign = {}
      dict_tradeAmount = {}
      dict_accSignPer = {}
      dict_weekBong = {}
      dict_priceMeans = {}
      dict_topVSper = {}
      dict_accVSmax = {}

      #s_curTime = data[0:6]
      t_data = data
      YY = t_data[0:4]
      MM = t_data[4:6]
      DD = t_data[6:8]
      s_curDate = '%s-%s-%s' % (YY, MM, DD)

      hh = t_data[8:10]
      mm = t_data[10:12]
      ss = t_data[12:14]
      s_curTime = '%s:%s:%s' % (hh, mm, ss)

      r = data[15:]
      r_list = r.split("|")
      for items in r_list:
         fields = items.split("^")
         if len(fields) != 13:
            continue

         total_list += 1

         #print '[%d] ###%s' % (total_list, str(fields))

         s_code = str(fields[1])
         list_code.append(s_code)
         dict_code[s_code] = s_code
         dict_name[s_code] = str(unicode(fields[0])).strip()
         #print '%s' %  dict_name[s_code]
         dict_pricePer[s_code] = str(fields[2]).strip()
         dict_startPricePer[s_code] = str(fields[3]).strip()
         dict_curPrice[s_code] = str(fields[4]).strip()
         dict_accSign[s_code] = str(fields[5]).strip()
         dict_tradeAmount[s_code] = str(fields[6]).strip()
         dict_accSignPer[s_code] = str(fields[7]).strip()
         dict_weekBong[s_code] = str(fields[8]).strip()
         dict_priceMeans[s_code] = str(fields[9]).strip()
         dict_accVSmax[s_code] = str(fields[10]).strip()
         dict_topVSper[s_code] = str(fields[11]).strip()


      context = {
         'who': who,
         'curTime': s_curTime,
         'curDate': s_curDate,
         'list_code': list_code,
         'dict_code': dict_code,
         'dict_name': dict_name,
         'dict_pricePer': dict_pricePer,
         'dict_startPricePer': dict_startPricePer,
         'dict_curPrice': dict_curPrice,
         'dict_accSign': dict_accSign,
         'dict_tradeAmount': dict_tradeAmount,
         'dict_accSignPer': dict_accSignPer,
         'dict_weekBong': dict_weekBong,
         'dict_priceMeans': dict_priceMeans,
         'dict_accVSmax': dict_accVSmax,
         'dict_topVSper': dict_topVSper
      }

      html = self.render_template('presentation_v1.html', context)


   def presentation_acc(self, data, who):
      total_list = 0
      list_code = []
      dict_code = {}
      dict_name = {}
      dict_pricePer = {}
      dict_startPricePer = {}
      dict_curPrice = {}
      dict_accSign = {}
      dict_tradeAmount = {}
      dict_accSignPer = {}
      dict_weekBong = {}
      dict_priceMeans = {}
      dict_topVSper = {}
      dict_accVSmax = {}

      #s_curTime = data[0:6]
      t_data = data
      YY = t_data[0:4]
      MM = t_data[4:6]
      DD = t_data[6:8]
      s_curDate = '%s-%s-%s' % (YY, MM, DD)

      hh = t_data[8:10]
      mm = t_data[10:12]
      ss = t_data[12:14]
      s_curTime = '%s:%s:%s' % (hh, mm, ss)

      r = data[15:]
      r_list = r.split("|")
      for items in r_list:
         fields = items.split("^")
         if len(fields) != 13:
            continue

         total_list += 1

         #print '[%d] ###%s' % (total_list, str(fields))

         s_code = str(fields[1])
         list_code.append(s_code)
         dict_code[s_code] = s_code
         dict_name[s_code] = str(unicode(fields[0])).strip()
         #print '%s' %  dict_name[s_code]
         dict_pricePer[s_code] = str(fields[2]).strip()
         dict_startPricePer[s_code] = str(fields[3]).strip()
         dict_curPrice[s_code] = str(fields[4]).strip()
         dict_accSign[s_code] = str(fields[5]).strip()
         dict_tradeAmount[s_code] = str(fields[6]).strip()
         dict_accSignPer[s_code] = str(fields[7]).strip()
         dict_weekBong[s_code] = str(fields[8]).strip()
         dict_priceMeans[s_code] = str(fields[9]).strip()
         dict_accVSmax[s_code] = str(fields[10]).strip()
         dict_topVSper[s_code] = str(fields[11]).strip()


      context = {
         'who': who,
         'curTime': s_curTime,
         'curDate': s_curDate,
         'list_code': list_code,
         'dict_code': dict_code,
         'dict_name': dict_name,
         'dict_pricePer': dict_pricePer,
         'dict_startPricePer': dict_startPricePer,
         'dict_curPrice': dict_curPrice,
         'dict_accSign': dict_accSign,
         'dict_tradeAmount': dict_tradeAmount,
         'dict_accSignPer': dict_accSignPer,
         'dict_weekBong': dict_weekBong,
         'dict_priceMeans': dict_priceMeans,
         'dict_accVSmax': dict_accVSmax,
         'dict_topVSper': dict_topVSper
      }

      html = self.render_template('presentation_v1.html', context)

      return html

