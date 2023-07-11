from pydantic import BaseModel
from typing import Optional, List
from model.veiculo import Veiculo

from schemas import AcessorioSchema


class VeiculoSchema(BaseModel):
    """ Define como um novo veiculo a ser inserido deve ser representado
    """
    nome: str = "Honda New Civic"
    ano_fabricacao: Optional[int] = 2020
    ano_modelo_fabricacao: Optional[int] = 2020
    valor_diaria: float = 150.00


class ListagemVeiculosSchema(BaseModel):
    """ Define como uma listagem de veiculos que será retornada.
    """
    veiculos:List[VeiculoSchema]


def apresenta_veiculos(veiculos: List[Veiculo]):
    """ Retorna uma representação do veiculo seguindo o schema definido em
        VeiculoViewSchema.
    """
    
    result = []
    for veiculo in veiculos:
        result.append({
            "id": veiculo.id,
            "nome": veiculo.nome,
            "ano_fabricacao": veiculo.ano_fabricacao,
            "ano_modelo_fabricacao": veiculo.ano_modelo_fabricacao,
            "valor_diaria": veiculo.valor_diaria,
            "total_acessorios": len(veiculo.acessorios),
            "acessorios": [{"nome": c.nome} for c in veiculo.acessorios]            
        })

    return {"veiculos": result}

class VeiculoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do veiculo.
    """
    nome: str = "Honda New Civic"


class VeiculoViewSchema(BaseModel):
    """ Define como um veiculo será retornado: veiculo + acessórios.
    """
    id: int = 1
    nome: str = "Honda New Civic"
    ano_fabricacao: Optional[int] = 2020
    ano_modelo_fabricacao: Optional[int] = 2020
    valor_diaria: float = 150.00
    total_acessorios: int = 1
    acessorios:List[AcessorioSchema]


class UpdateVeiculoSchema(BaseModel):
    """ Define como um novo veiculo pode ser atualizado.
    """
    #inserido o id para facilitar a busca na base para alteração
    id:int = 1
    nome: str = "Honda New Civic"
    ano_fabricacao: Optional[int] = 2020
    ano_modelo_fabricacao: Optional[int] = 2020
    valor_diaria: Optional[float] = 150.00

    
class VeiculoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_veiculo(veiculo: Veiculo):
    """ Retorna uma representação do veiculo seguindo o schema definido em
        VeiculoViewSchema.
    """
    return {
        "id": veiculo.id,
        "nome": veiculo.nome,
        "ano_fabricacao": veiculo.ano_fabricacao,
        "ano_modelo_fabricacao": veiculo.ano_modelo_fabricacao,
        "valor_diaria": veiculo.valor_diaria,
        "total_acessorios": len(veiculo.acessorios),
        "acessorios": [{"nome": c.nome} for c in veiculo.acessorios]
    }


