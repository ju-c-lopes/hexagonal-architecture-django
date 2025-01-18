from pymongo import MongoClient

from lanchonete.settings import MONGO_URI


def get_mongo_client():
    """Capturará a string de conexão com o MongoDB e retornará um cliente para conexão com o banco de dados.

    Returns:
        MongoClient: connection string for MongoDB
    """
    return MongoClient(MONGO_URI)
