from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Acessorio


class Veiculo(Base):
    __tablename__ = 'veiculo'

    id = Column("pk_veiculo", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    ano_fabricacao = Column(Integer)
    ano_modelo_fabricacao = Column(Integer)
    placa = Column(String(50), unique=True)
    status = Column(String(50))
    valor_diaria = Column(Float)
    data_aquisicao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o veiculo e o acessório.
    # Essa relação é implicita, não está salva na tabela 'veiculo',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    acessorios = relationship("Acessorio")

    def __init__(self, nome:str, ano_fabricacao:int, ano_modelo_fabricacao:int, valor_diaria:float, placa:str,status:str,
                 data_aquisicao:Union[DateTime, None] = None):
        """
        Cria um Veiculo

        Arguments:
            nome: nome do veiculo.
            ano_fabricacao: ano_fabricacao que se fabricou o  veiculo
            ano_modelo_fabricacao: ano_modelo_fabricacao que se fabricou o veiculo
            placa: placa do veículo
            valor_diaria: valor_diaria esperada para locar o veiculo
            data_aquisicao: data de quando o veiculo foi adquirido
        """
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao
        self.ano_modelo_fabricacao = ano_modelo_fabricacao
        self.placa = placa
        self.status
        self.valor_diaria = valor_diaria

        # se não for informada, será o data exata da inserção no banco
        if data_aquisicao:
            self.data_aquisicao = data_aquisicao

    def adiciona_acessorio(self, acessorio:Acessorio):
        """ Adiciona um novo acessório ao Veiculo
        """
        self.acessorios.append(acessorio)

