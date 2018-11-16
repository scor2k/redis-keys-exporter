#!/usr/bin/env python3

import os
import falcon
import json
import logging
import sys
import threading

from datetime   import datetime

from inc.audit  import RedisAudit
from __init__   import __version__


############################### INIT LOGGIG ##################################

log = logging.getLogger()
log.setLevel(logging.DEBUG)

stdout = logging.StreamHandler(sys.stdout)
stdout.setLevel(logging.DEBUG)
log.addHandler(stdout)


############################### FALCON CLASSES ##################################

class CORS:
  def process_request(self, req, resp):
      resp.set_header( 'Access-Control-Allow-Origin', '*' )

class RedisExporterPing:
  def on_get(self, req, resp):
    resp.status = falcon.HTTP_200

class RedisExporterMetrics:
  def on_get(self, req, resp):
    try :
      with open('redis_keys_metrics.prom', 'r') as f:
        resp.body = f.read()
        resp.status = falcon.HTTP_200
        f.close()
    except IOError:
      resp.status = falcon.HTTP_204



############################### FALCON ROUTING ##################################
api = falcon.API(  middleware=[ CORS(), ] )

api.add_route('/_ping',     RedisExporterPing())
api.add_route('/metrics',   RedisExporterMetrics())

############################### EXECUTE PERIODICALLY ##################################

def get_metrics() :
  log.debug("""[%s] Start scraping Redis.""" % ( datetime.now() ) )

  REDIS_DB_LIST           = os.environ.get('REDIS_DB_LIST', '0')
  REDIS_SCRAPE_INTERVAL   = os.environ.get('REDIS_SCRAPE_INTERVAL', 900)

  # try to convert string into list
  try :
    redis_dbs = REDIS_DB_LIST.split(",")
  except :
    redis_dbs = [0, ]

  red = RedisAudit()
  red.get_metrics(redis_dbs)

  log.debug("""[%s] End scraping Redis.""" % ( datetime.now() ) )

  threading.Timer(REDIS_SCRAPE_INTERVAL, get_metrics).start() 



############################### INIT APP ##################################

log.info("""[%s] ian Redis Exporter started. Version: %s """ % ( datetime.now(),  __version__ ) )




threading.Timer( 5, get_metrics).start()


