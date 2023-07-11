from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Acessorio(Base):
    __tablename__ = 'acessorio'

    id = Column(Integer, primary_key=True)
    nome = Column(String(4000))
    data_validade = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o acessório e um veiculo.
    # Aqui está sendo definido a coluna 'veiculo' que vai guardar
    # a referencia ao veiculo, a chave estrangeira que relaciona
    # um veiculo ao acessório.
    veiculo = Column(Integer, ForeignKey("veiculo.pk_veiculo"), nullable=False)

    def __init__(self, nome:str, data_validade:Union[DateTime, None] = None):
        """
        Cria um Acessório

        Arguments:
            nome: o nome de um acessório.
            data_validade: data de quando o acessório foi feito ou inserido
                           à base
        """
        self.nome = nome
        if data_validade:
            self.data_validade = data_validade
