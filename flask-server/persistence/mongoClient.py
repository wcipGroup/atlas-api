from config.configuration import Configuration
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import socket


class Mongo():
    __config = None
    __mongo_config = None
    __host = None
    __user = None
    __password = None
    __port = None
    __auth_db = None
    __timeout = None
    __mqttc = None
    __mbus_server_ip = None
    connection = None
    db = None

    def __init__(self):
        print("Mongo object init...")
        self.__config = Configuration.get()
        self.__mongo_config = self.__config["MONGO"]

        self.__host = self.__mongo_config["HOST"]
        self.__user = self.__mongo_config["USER"]
        self.__password = self.__mongo_config["PASSWORD"]
        self.__port = self.__mongo_config["PORT"]
        # self.__auth_db = self.__mongo_config["AUTH_DB"]
        # self.__timeout = self.__mongo_config["TIMEOUT"]
        Mongo.connection = MongoClient(self.__host, self.__port, username=self.__user, password=self.__password,
         authMechanism='SCRAM-SHA-256')
        # Mongo.connection = MongoClient(f"mongodb+srv://{self.__user}:{self.__password}@{self.__host}/test?retryWrites=true&w=majority")
        if self.__config["DEBUG"]:
            self.__set_database(self.__mongo_config["DEBUG_DATABASE"])
        else:
            self.__set_database(self.__mongo_config["DATABASE"])

        try:
            self.__check_connection()
            Mongo.__mqttc = mqtt.Client()
            Mongo.__mqttc.connect(self.__mongo_config["MQTT_SERVER"], 1883, 60)

            Mongo.__mbus_server_ip = self.__mongo_config["MBUS_SERVER"]
        except Exception as e:
            raise e

    @staticmethod
    def __set_database(database):
        Mongo.db = Mongo.connection[database]

    @staticmethod
    def __check_connection():
        try:
            Mongo.connection.server_info()
            print("Mongo client initialized")
        except Exception as e:
            Mongo.connection.close()
            raise e

    @staticmethod
    def get_connection():
        if Mongo.connection:
            return Mongo.connection
        raise SystemExit("MongoDB is not set")

    @staticmethod
    def get_db():
        if Mongo.db:
            return Mongo.db
        raise SystemExit("MongoDB is not set")

    @staticmethod
    def get_mqttc():
        if Mongo.__mqttc:
            return Mongo.__mqttc
        raise SystemExit("MQTT is not set")

    @staticmethod
    def get_mbus_server_ip():
        return Mongo.__mbus_server_ip