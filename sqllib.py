# -*- coding: utf8 -*-

import pymysql

class ErpySQL:

   conn = None
   curs = None

   def __init__(self, tuser='erpy', tpassword='kiwitomato.com'):
      self.conn = pymysql.connect(host='localhost', user=tuser, password=tpassword, db='day_data', charset='utf8')
      self.curs = self.conn.cursor()
      print 'init ErpySQL'

   def __del__(self):
      self.curs.close()
      self.conn.close()
      print 'destroy ErpySQL'

   def getRowCount(self, strSql):
      print 'SQL : %s' % strSql
      self.curs.execute(strSql)
      return self.curs.rowcount

   def existId(self, strSql):
      print 'SQL : %s' % strSql
      self.curs.execute(strSql)
      if self.curs.rowcount == 0:
         return False
      else:
         return True

   def select(self, strSql):
      self.curs.execute(strSql)
      return self.curs.fetchall()

   def insertId(self, strSql):
      print 'SQL : %s' % strSql
      self.curs.execute(strSql)
      self.conn.commit()

   def updateId(self, strSql):
      print 'SQL : %s' % strSql
      self.curs.execute(strSql)
      self.conn.commit()

   def deleteId(self, strSql):
      print 'SQL : %s' % strSql
      self.curs.execute(strSql)
      self.conn.commit()

   def close(self):
      self.curs.close()
      self.conn.close()
      print 'destroy ErpySQL'

