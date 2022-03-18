import pika


class Publisher:

    channel = None
    queue = None
    connection = None

    def __init__(self, config):
        try:
            self.config = config
            credentials = pika.PlainCredentials(config["USER"], config["PASSWORD"])
            Publisher.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['AMQP_IP'],
                                                                                     port=config['PORT'],
                                                                                     credentials=credentials,
                                                                                     heartbeat=600))
            Publisher.queue = config['QUEUE']
            # self.channel = self.connection.channel()
            # self.channel.queue_declare(queue=self.queue)
            Publisher.channel = Publisher.connection.channel()
            Publisher.channel.queue_declare(queue=Publisher.queue)
        except Exception as e:
            raise e

    @staticmethod
    def publish(message):
        try:
            Publisher.channel.basic_publish(exchange='', routing_key=Publisher.queue, body=message)
            print("published")
        except Exception as e:
            print(e)

    @staticmethod
    def get_channel():
        if Publisher.channel:
            return Publisher.channel
        raise SystemExit("Publisher is not set")

    @staticmethod
    def stop():
        Publisher.channel.close()
        Publisher.connection.close()
