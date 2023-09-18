from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Veiculo, Acessorio
from logger import logger
from schemas import veiculo, VeiculoBuscaSchema, VeiculoDelSchema, VeiculoSchema, VeiculoViewSchema, ListagemVeiculosSchema, ErrorSchema, apresenta_veiculo, apresenta_veiculos #*  UpdateVeiculoSchema
from flask_cors import CORS
from schemas.veiculo import UpdateVeiculoSchema
from schemas.acessorio import AcessorioSchema


info = Info(title="Minha API - Veículos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
veiculo_tag = Tag(name="Veiculo", description="Adição, visualização, atualização e remoção de veiculos à base")
acessorio_tag = Tag(name="Acessorio", description="Adição de um acessório à um veiculos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')


@app.post('/veiculo', tags=[veiculo_tag],
          responses={"200": VeiculoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_veiculo(form: VeiculoSchema):
    """Adiciona um novo Veiculo à base de dados

    Retorna uma representação dos veiculos e acessórios associados.
    """
    veiculo = Veiculo(
        nome=form.nome,
        ano_fabricacao=form.ano_fabricacao,
        ano_modelo_fabricacao=form.ano_modelo_fabricacao,
        placa=form.placa,
        status=form.status,
        valor_diaria=form.valor_diaria)
    logger.debug(f"Adicionando veiculo de nome: '{veiculo.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando veiculo
        session.add(veiculo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado veiculo de nome: '{veiculo.nome}'")
        return apresenta_veiculo(veiculo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Veiculo de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar veiculo '{veiculo.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar veiculo '{veiculo.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.put('/update_veiculo', tags=[veiculo_tag],
          responses={"200": VeiculoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_veiculo(form: UpdateVeiculoSchema):
    """Edita um Veiculo já salvo na base de dados

    Retorna uma representação dos veiculos e acessórios associados.
    """
    ## recebe o id ao invés do nome para busca
    id_veiculo = form.id
    nome_veic = form.nome
    session = Session()

    try:
        #passa a buscar pelo id e o nome para possível troca
        #query = session.query(Veiculo).filter(Veiculo.nome == nome_veic)
        query = session.query(Veiculo).filter(Veiculo.id == id_veiculo)
        print(query)
        db_veiculo = query.first()
        if not db_veiculo:
            # se o veiculo não foi encontrado
            error_msg = "Veiculo não encontrado na base :/"
            logger.warning(f"Erro ao buscar veiculo '{nome_veic}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            if form.ano_fabricacao:
                db_veiculo.ano_fabricacao = form.ano_fabricacao
            
            if form.ano_modelo_fabricacao:
                db_veiculo.ano_modelo_fabricacao = form.ano_modelo_fabricacao
            
            if form.valor_diaria:
                db_veiculo.valor_diaria = form.valor_diaria
            
            db_veiculo.nome = form.nome # só para garantir, pois estava dando erro ao gravar o nome
            db_veiculo.placa = form.placa
            db_veiculo.status = form.status
            
            session.add(db_veiculo)
            session.commit()
            logger.debug(f"Alterado veiculo de nome: '{db_veiculo.nome}'")
            return apresenta_veiculo(db_veiculo), 200
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar veiculo, {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.get('/veiculos', tags=[veiculo_tag],
         responses={"200": ListagemVeiculosSchema, "404": ErrorSchema})
def get_veiculos():
    """Faz a busca por todos os Veiculo cadastrados

    Retorna uma representação da listagem de veiculos.
    """
    logger.debug(f"Coletando veiculos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    veiculos = session.query(Veiculo).all()

    if not veiculos:
        # se não há veiculos cadastrados
        return {"veiculos": []}, 200
    else:
        logger.debug(f"%d veiculos econtrados" % len(veiculos))
        # retorna a representação de veiculo
        print(veiculos)
        return apresenta_veiculos(veiculos), 200


@app.get('/veiculo', tags=[veiculo_tag],
         responses={"200": VeiculoViewSchema, "404": ErrorSchema})
def get_veiculo(query: VeiculoBuscaSchema):
    """Faz a busca por um Veiculo a partir do id do veiculo

    Retorna uma representação dos veiculos e acessórios associados.
    """
    veiculo_nome = query.nome
    logger.debug(f"Coletando dados sobre veiculo #{veiculo_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    veiculo = session.query(Veiculo).filter(Veiculo.nome == veiculo_nome).first()

    if not veiculo:
        # se o veiculo não foi encontrado
        error_msg = "Veiculo não encontrado na base :/"
        logger.warning(f"Erro ao buscar veiculo '{veiculo_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Veiculo econtrado: '{veiculo.nome}'")
        # retorna a representação de veiculo
        return apresenta_veiculo(veiculo), 200


@app.delete('/veiculo', tags=[veiculo_tag],
            responses={"200": VeiculoDelSchema, "404": ErrorSchema})
def del_veiculo(query: VeiculoBuscaSchema):
    """Deleta um Veiculo a partir do nome de veiculo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    veiculo_nome = unquote(unquote(query.nome))
    print(veiculo_nome)
    logger.debug(f"Deletando dados sobre veiculo #{veiculo_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Veiculo).filter(Veiculo.nome == veiculo_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado veiculo #{veiculo_nome}")
        return {"mesage": "Veiculo removido", "id": veiculo_nome}
    else:
        # se o veiculo não foi encontrado
        error_msg = "Veiculo não encontrado na base :/"
        logger.warning(f"Erro ao deletar veiculo #'{veiculo_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/acessorio', tags=[acessorio_tag],
          responses={"200": VeiculoViewSchema, "404": ErrorSchema})
def add_acessorio(form: AcessorioSchema):
    """Adiciona de um novo acessório à um veiculos cadastrado na base identificado pelo id

    Retorna uma representação dos veiculos e acessório associados.
    """
    veiculo_id  = form.veiculo_id
    logger.debug(f"Adicionando acessório ao veículo #{veiculo_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo veiculo
    veiculo = session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()

    if not veiculo:
        # se veiculo não encontrado
        error_msg = "Veiculo não encontrado na base :/"
        logger.warning(f"Erro ao adicionar acessório ao veiculo '{veiculo_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o acessório
    nome = form.nome
    acessorio = Acessorio(nome)

    # adicionando o acessório ao veiculo
    veiculo.adiciona_acessorio(acessorio)
    session.commit()

    logger.debug(f"Adicionado acessório ao veiculo #{veiculo_id}")

    # retorna a representação de veiculo
    return apresenta_veiculo(veiculo), 200