import redis
import re
import datetime
import os

class RedisAudit() :
  def __init__(self):
    self.REDIS_HOST   = os.environ.get('REDIS_HOST', '192.168.16.26')
    self.REDIS_PORT   = os.environ.get('REDIS_PORT', 6379)
    self.REDIS_POOL   = None
    self.REDIS        = None

    #self.PATTERN      = re.compile(r'^cache\.[a-z-]+')
    self.PATTERN      = re.compile(r'^[a-z]+[.:]+[a-z_-]+')

  def connect_redis(self, database=0):
    try :
      self.REDIS_POOL   = redis.ConnectionPool( host = self.REDIS_HOST, port = self.REDIS_PORT, db=database )
      self.REDIS        = redis.Redis(connection_pool = self.REDIS_POOL)
    except Exception as e:
      print (e)
      return False


  def scan_db(self, database=0) :
    self.connect_redis(database)

    data = {'other':0}

    for key in self.REDIS.scan_iter(match='*', count='200') :
      tmp = re.search( self.PATTERN, key.decode("utf-8") )

      try :
        # remove trailing sign (.) and digits
        ##kk = tmp.group(0)[:-1].replace('.','_')
        kk = re.sub( r'\d', '', tmp.group(0), flags=re.IGNORECASE )
        try :
          cur_val = data[kk]
        except :
          cur_val = 0

        #print ("key : %s, value: %s" % ( kk, cur_val ) )
        data[kk] = cur_val + 1
      except Exception as e :
        #print( "other: %s" % key )
        cur_val = int(data['other'])
        data['other'] = cur_val + 1

    return  data

  def generate_metrics(self, database, data):
    ''' get dictionary and create data for prometheus '''
    template = """redis_keys{db="%s", key="%s"} %s\n"""
    result = ""

    for key in data:
      result = result + template % ( database, key, data[key] )
      
    
    return result



  def get_metrics(self, databases) :
    ''' get metrics from all databases '''


    full_metrics = ""

    for idx, val in enumerate(databases) :
      start_time = datetime.datetime.now()
      data = self.scan_db(val)
      metrics = self.generate_metrics(val, data)
      end_time = datetime.datetime.now()
      metrics = metrics + """redis_keys_scrape_msec{db="%s"} %s\n""" % (val, (end_time - start_time).microseconds ) 

      full_metrics = full_metrics + metrics


    # writing into file
    with open('redis_keys_metrics.prom', 'w') as f:
      f.write(full_metrics)
      f.close()

    return full_metrics


    


    
