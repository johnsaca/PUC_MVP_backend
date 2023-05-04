from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Acesso(Base):
    __tablename__ = 'acesso'

    cracha = Column("pk_acesso", String(140),primary_key=True)
    nome = Column(String(140))
    area = Column(String(140))
    funcao = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, cracha:str, nome:str, area:str, funcao:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Libera um Acesso

        Arguments:
            cracha: número do crachá.
            nome: nome do funcionário
            area: area na qual o funcionario trabalha
            funcao: funcao do funcionario
            data_insercao: data de quando o acesso foi liberado
        """
        self.cracha = cracha
        self.nome = nome
        self.area = area
        self.funcao = funcao
        self.data_insercao = data_insercao