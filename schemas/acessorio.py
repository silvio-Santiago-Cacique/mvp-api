from pydantic import BaseModel


class AcessorioSchema(BaseModel):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    veiculo_id: int = 1
    nome: str = "ArBags duplos"
