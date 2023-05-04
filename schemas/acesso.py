from pydantic import BaseModel
from typing import Optional, List
from model.acesso import Acesso


class AcessoSchema(BaseModel):
    """ Define como um novo acesso liberado deve ser representado
    """
    cracha: str = "1272"
    nome: str = "Jonathas Assumpção"
    area: str = "TI"
    funcao: str = "Gerente"


class AcessoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no numero do crachá.
    """
    cracha: str = "Teste"


class ListagemAcessosSchema(BaseModel):
    """ Define como uma listagem de acessos será retornada.
    """
    acessos:List[AcessoSchema]


def apresenta_acessos(acessos: List[Acesso]):
    """ Retorna uma representação dos acessos seguindo o schema definido em
        AcessoViewSchema.
    """
    result = []
    for acesso in acessos:
        result.append({
            "cracha": acesso.cracha,
            "nome": acesso.nome,
            "area": acesso.area,
            "funcao": acesso.funcao,
        })

    return {"acessos": result}


class AcessoViewSchema(BaseModel):
    """ Define como um acesso será retornado.
    """
    cracha: str = "1272"
    nome: str = "Jonathas Assumpção"
    area: str = "TI"
    funcao: str = "Gerente"


class AcessoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_acesso(acesso: Acesso):
    """ Retorna uma representação do acesso seguindo o schema definido em
        AcessoViewSchema.
    """
    return {
        "cracha": acesso.cracha,
        "nome": acesso.nome,
        "area": acesso.area,
        "funcao": acesso.funcao,
    }
