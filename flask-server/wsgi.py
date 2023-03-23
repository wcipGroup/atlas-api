from myapp import application
from config.configuration import Configuration
from persistence.mongoClient import Mongo
from amqp.publisher import Publisher
import os
import time
import threading
from threading import Lock

# application._before_request_lock = Lock
# application._got_first_request = False
#
# @application.before_request
# def setting_communications():
#   if application._got_first_request:
#     return
#   with application._before_request_lock:
#     if application._got_first_request:
#       return
#     print("BEFORE REQUEST")
def mqttc_keep_alive(mqttc):
  while 1:
    mqttc.publish('atlas/keep_alive', "heartbeat [atlas api]")
    time.sleep(30)

@application.before_first_request
def setting_communications():
  try:
    print("before first request")
    cwd = os.path.dirname(os.path.abspath(__file__))
    Configuration(os.path.join(cwd, 'config/config.json'))
    config = Configuration.get()
    db = Mongo()
    pub = Publisher(config["AMQP"])
    mqttc = Mongo.get_mqttc()
    threading.Thread(target=mqttc_keep_alive, args=(mqttc,)).start()
    mqttc.publish('atlas/system', "starting [atlas api]")
  except Exception as e:
    print("log", str(e))


if __name__ == "__main__":
  application.run()
