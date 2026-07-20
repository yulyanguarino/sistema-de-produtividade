from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional


# ---- Colaborador ----
class ColaboradorBase(BaseModel):
    nome: str
    ativo: bool = True


class ColaboradorCreate(ColaboradorBase):
    pass


class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = None
    ativo: Optional[bool] = None


class ColaboradorRead(ColaboradorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---- Operacao ----
class OperacaoBase(BaseModel):
    data: date
    pedido: str
    separador_id: int
    qtd_itens_separados: int = Field(ge=0)
    conferente_id: int
    qtd_itens_conferidos: int = Field(ge=0)


class OperacaoCreate(OperacaoBase):
    pass


class OperacaoRead(OperacaoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OperacaoReadDetalhado(OperacaoRead):
    separador_nome: str
    conferente_nome: str


# ---- Dashboard ----
class IndicadoresRead(BaseModel):
    total_pedidos: int
    total_itens_separados: int
    total_itens_conferidos: int
    colaboradores_ativos: int


class RankingItem(BaseModel):
    colaborador_id: int
    colaborador_nome: str
    qtd_pedidos: int
    qtd_itens: int


class RankingResponse(BaseModel):
    separadores: list[RankingItem]
    conferentes: list[RankingItem]


class DashboardResponse(BaseModel):
    indicadores: IndicadoresRead
    ranking: RankingResponse
    filtros_aplicados: dict
