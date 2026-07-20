from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from database import Base


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True, server_default="true")

    operacoes_como_separador = relationship(
        "Operacao",
        foreign_keys="Operacao.separador_id",
        back_populates="separador",
    )
    operacoes_como_conferente = relationship(
        "Operacao",
        foreign_keys="Operacao.conferente_id",
        back_populates="conferente",
    )

    def __repr__(self):
        return f"<Colaborador(id={self.id}, nome='{self.nome}', ativo={self.ativo})>"


class Operacao(Base):
    __tablename__ = "operacoes"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False, index=True)
    pedido = Column(String(50), nullable=False)
    separador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    qtd_itens_separados = Column(Integer, nullable=False)
    conferente_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    qtd_itens_conferidos = Column(Integer, nullable=False)

    separador = relationship(
        "Colaborador",
        foreign_keys=[separador_id],
        back_populates="operacoes_como_separador",
    )
    conferente = relationship(
        "Colaborador",
        foreign_keys=[conferente_id],
        back_populates="operacoes_como_conferente",
    )

    __table_args__ = (
        CheckConstraint("qtd_itens_separados >= 0"),
        CheckConstraint("qtd_itens_conferidos >= 0"),
        Index("ix_operacoes_separador_data", separador_id, data),
        Index("ix_operacoes_conferente_data", conferente_id, data),
    )

    def __repr__(self):
        return f"<Operacao(id={self.id}, data={self.data}, pedido='{self.pedido}')>"
