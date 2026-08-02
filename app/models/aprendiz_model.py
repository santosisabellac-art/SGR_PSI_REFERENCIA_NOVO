from sqlalchemy import Boolean, Column, Integer, String

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

    def __repr__(self):
        return f"<Aprendiz(nome='{self.nome}')>"