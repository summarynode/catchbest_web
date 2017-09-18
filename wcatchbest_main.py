#! /usr/bin/env python
# -*- coding: utf8 -*-
 
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from sqllib import ErpySQL

import datetime
import sys
import cgi
import threading
from urlparse import urlparse
import urlparse as urlpar
reload(sys)
sys.setdefaultencoding('utf-8')

import redis

import wcatchbest_present

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        msg = ""
        cmd = ""
        parsed_path = urlparse(self.path)
        print 'parsed_path : %s' % str(parsed_path)

        if parsed_path.path == "/login":

           api = ErpySQL()

           """
           print 'path : %s' % self.path
           print 'parsed path : %s' % parsed_path.path
           print 'parsed query : %s' % parsed_path.query
           print 'client ip : %s' % self.client_address[0]
           """

           result = urlpar.parse_qs(parsed_path.query)
           #print 'result : %s' % result

           t_id = result.get('id', None)
           if t_id is None:
              msg = "None id"
           else:
              t_id = ''.join(result['id'])
              print '(in) t_id : %s' % t_id

           t_password = result.get('password', None)
           if t_password is None:
              msg = "None password"
           else:
              t_password = ''.join(result['password'])
              print '(in) t_password : %s' % t_password

           t_ip = self.client_address[0]
           print '(in) t_ip : %s' % t_ip

           if len(msg) == 0:
              cmd = "select id from user_info where id='%s' and password='%s'" % (t_id.strip(), t_password.strip())
              rowCount = api.getRowCount(cmd)
              if rowCount == 1:
                 cur_datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                 cmd = "update user_info set ip='%s', login_time='%s' where id='%s'" % (t_ip, cur_datetime, t_id)
                 api.updateId(cmd)
                 msg = "login success | %s | 0.1" % t_ip
              else:
                 msg = "login fail"

           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(len(msg)))
           self.end_headers()

           self.wfile.write(msg)

        elif parsed_path.path == "/set":

           result = urlpar.parse_qs(parsed_path.query)

           t_key = result.get('key', None)
           if t_key is None:
              msg = "None key"
           else:
              t_key = ''.join(result['key'])
              print 't_key : %s' % t_key

           t_value = result.get('value', None)
           if t_value is None:
              msg = "None value"
           else:
              t_value = ''.join(result['value'])
              print 't_value : %s' % t_value

           if len(msg) == 0:
              result = urlpar.parse_qs(parsed_path.query)
              redi = redis.StrictRedis(host='localhost', port=6379, db=0)
              redi.set(t_key, t_value)
              msg = "set success"

           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(len(msg)))
           self.end_headers()

           self.wfile.write(msg)

        elif parsed_path.path == "/get":

           result = urlpar.parse_qs(parsed_path.query)
           #print 'result : %s' % result

           t_key = result.get('key', None)
           if t_key is None:
              msg = "None key"
           else:
              t_key = ''.join(result['key'])
              print 't_key : %s' % t_key

           t_who = result.get('who', None)
           if t_who is None:
              t_who = ""
           else:
              t_who = ''.join(result['who'])
              print 't_who : %s' % t_who

           result_value = ''
           present_data = ''
           if len(msg) == 0:
              redi = redis.StrictRedis(host='localhost', port=6379, db=0)
              result_value = redi.get(t_key)
              #print 'result : %s' % result_value
              if len(str(result_value)) == 0:
                 present_data = "key is None"
              else:
                 present_data = wcatchbest_present.SinhoPresent().presentation(result_value, t_who)


           send_len = len(present_data.encode("utf-8"))
           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(send_len))
           self.end_headers()

           self.wfile.write(str(present_data))

        elif parsed_path.path == "/search":

           listAll = []
           present_data=""
           s_date = ""
           s_acc_v = ""
           s_tr_v = ""
           s_per = ""
           msg = ""
           t_who = ""
           result = urlpar.parse_qs(parsed_path.query)
           t_ip = self.client_address[0]
           t_code = result.get('code', None)
           if t_code is None:
              msg = "None code"
           else:
              t_code = ''.join(result['code'])
              print '(in) t_code : %s' % t_code
              msg = t_code

              api = ErpySQL()
              sql = "select CONVERT(s_date, CHAR(8)) as r_date, s_volume as acc_v, s_acc_volume as tr_v, s_per as per from acc_volume where s_code='" + t_code + "' order by s_date desc"
              rows = api.select(sql)
              for row in rows:
                 s_date  = str(row[0])
                 s_acc_v = str(row[1])
                 s_tr_v  = str(row[2])
                 s_per   = str(row[3])

                 rlist = "%s|%s|%s|%s|%s" % (t_code, s_date, s_acc_v, s_tr_v, s_per)
                 listAll.append(rlist)
                 msg = wcatchbest_present.SinhoPresent().presentation_acc(rlist, t_who)
                 #print rlist

              print listAll

           send_len = len(msg.encode("utf-8"))
           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(send_len))
           self.end_headers()
           self.wfile.write(msg)

        elif parsed_path.path == "/check":

           api = ErpySQL()
           result = urlpar.parse_qs(parsed_path.query)

           t_ip = self.client_address[0]

           t_id = result.get('id', None)
           if t_id is None:
              msg = "None id"
           else:
              t_id = ''.join(result['id'])
              print '(in) t_id : %s' % t_id

           if len(msg) == 0:
              cmd = "select id from user_info where id='%s' and ip='%s'" % (t_id, t_ip)
              rowCount = api.getRowCount(cmd)
              if rowCount == 0:
                 #msg = "ip address is success"
                 msg = "fail another ip address"
                 print "fail another ip address : %s, %s" % (t_id, t_ip)
              else:
                 msg = "ip address is success"

           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(len(msg)))
           self.end_headers()
           self.wfile.write(msg)

        elif parsed_path.path == "/list":

           api = ErpySQL()
           result = urlpar.parse_qs(parsed_path.query)
           t_id = result.get('id', None)
           if t_id is None:
              msg = "None id"
           else:
              t_id = ''.join(result['id'])
              print '(in) t_id : %s' % t_id

           t_password = result.get('password', None)
           if t_password is None:
              msg = "None password"
           else:
              t_password = ''.join(result['password'])
              print '(in) t_password : %s' % t_password

           if t_id == 'erpy' or t_id == 'yang3952':
              msg = ""
           else:
              msg = "fail id"

           api = ErpySQL()
           if len(msg) == 0:
              cmd = "select id from user_info where id='%s' and password='%s'" % (t_id.strip(), t_password.strip())
              rowCount = api.getRowCount(cmd)
              if rowCount == 1:
                 msg = ""
              else:
                 msg = "login fail"


           total = 0
           if len(msg) == 0:
              cmd = "select id, name, start_date, end_date, user_info, ip, login_time from user_info"
              results = api.select(cmd)
              for row in results:
                 total += 1
                 msg = msg + str(total) + " " + str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + " " + str(row[5]) + " " + str(row[6]) + "<br>"
                 msg = msg + "============================================================================================<br>"

           self.send_response(200)
           encoding = sys.getfilesystemencoding()
           self.send_header("Content-type", "text/html; charset=%s" % encoding)
           self.send_header("Content-Length", str(len(msg)))
           self.end_headers()

           self.wfile.write(msg)

        else:
           print 'else parsed path : %s' % parsed_path.path

        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    try:
       #server = ThreadedHTTPServer(('localhost', 7645), Handler)
       server = ThreadedHTTPServer(('', 6677), Handler)
       print 'Starting server, use <Ctrl-C> to stop'
       server.serve_forever()
    except KeyboardInterrupt:
       print('^C received, shutting down the web server')
       server.socket.close()
