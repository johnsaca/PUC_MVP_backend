from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Acesso
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
acesso_tag = Tag(name="Acesso", description="Adição, visualização e remoção de acessos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/acesso', tags=[acesso_tag],
          responses={"200": AcessoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_Acesso(form: AcessoSchema):
    """Autoriza um novo Acesso à base de dados

    Retorna uma representação dos acessos.
    """
    acesso = Acesso(
        cracha=form.cracha,
        nome=form.nome,
        area=form.area,
        funcao=form.funcao)
    logger.debug(f"Adicionando acesso ao funcionário de crachá: '{acesso.cracha}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando acesso
        session.add(acesso)
        # efetivando o comando de adição de novo acesso na tabela
        session.commit()
        logger.debug(f"Adicionado ao funcionário de crachá: '{acesso.cracha}'")
        return apresenta_acessos(acesso), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O crachá fornecido ja possui acesso ao sistema."
        logger.warning(f"Erro ao liberar acesso '{acesso.cracha}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Náo foi possível liberar acesso ao crachá informado."
        logger.warning(f"Erro ao tentar adicionar o crachá '{acesso.cracha}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/acessos', tags=[acesso_tag],
         responses={"200": ListagemAcessosSchema, "404": ErrorSchema})
def get_acessos():
    """Faz a busca por todos os Acessos liberados

    Retorna uma representação da listagem dos acessos existentes.
    """
    logger.debug(f"Buscando acessos")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acessos = session.query(Acesso).all()

    if not acessos:
        # se esse crachá náo está liberado
        return {"acessos": []}, 200
    else:
        logger.debug(f"%d acesso encontrado" % len(acessos))
        # retorna a representação dos acessos
        print(acessos)
        return apresenta_acessos(acessos), 200


@app.get('/acesso', tags=[acesso_tag],
         responses={"200": AcessoViewSchema, "404": ErrorSchema})
def get_acesso(query: AcessoBuscaSchema):
    """Faz a busca pelo Acesso a partir do crachá do produto

    Retorna uma representação dos acessos associados.
    """
    acesso_id = query.id
    logger.debug(f"Coletando dados de acesso #{acesso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acesso = session.query(Acesso).filter(Acesso.id == acesso_id).first()

    if not acesso:
        # se o acesso não foi encontrado
        error_msg = "Crachá não encontrado na base de acesso"
        logger.warning(f"Erro ao buscar o crachá '{acesso_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Acesso econtrado: '{acesso.cracha}'")
        # retorna a representação do acesso
        return apresenta_acessos(acesso), 200


@app.delete('/acesso', tags=[acesso_tag],
            responses={"200": AcessoDelSchema, "404": ErrorSchema})
def del_acesso(query: AcessoBuscaSchema):
    """Retira o acesso a partir do crachá informado

    Retorna uma mensagem de confirmação da remoção.
    """
    acesso_cracha = unquote(unquote(query.cracha))
    print(acesso_cracha)
    logger.debug(f"Deletando dados de acesso #{acesso_cracha}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Acesso).filter(Acesso.cracha == acesso_cracha).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Removendo acesso #{acesso_cracha}")
        return {"mesage": "Acesso removido", "id": acesso_cracha}
    else:
        # se o crachá não foi encontrado
        error_msg = "Crachá não encontrado na base de dados"
        logger.warning(f"Erro ao remover o acesso de #'{acesso_cracha}', {error_msg}")
        return {"mesage": error_msg}, 404
