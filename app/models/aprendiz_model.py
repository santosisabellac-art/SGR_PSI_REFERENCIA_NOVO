from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Aprendiz(Base):
    __tablename__ = "aprendizes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    codigo = Column(String(30), unique=True, nullable=False)

    nivel_suporte = Column(String(20), nullable=False)

    dias_atendimento = Column(String(100))

    horario = Column(String(100))

    sala = Column(String(30))

    carga_horaria_aba = Column(String(20))

    status = Column(String(20), default="Ativo")

    observacoes = Column(String(500))

    ativo = Column(Boolean, default=True)

    # Relacionamento com pendências
    pendencias = relationship(
        "Pendencia",
        back_populates="aprendiz",
        cascade="all, delete-orphan",
    )

    documentos = relationship(
        "Documento",
        back_populates="aprendiz",
        cascade="all, delete-orphan",
    )

    supervisoes = relationship(
        "Supervisao",
        back_populates="aprendiz",
        cascade="all, delete-orphan",
    )

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="aprendiz",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Aprendiz(nome='{self.nome}')>"
