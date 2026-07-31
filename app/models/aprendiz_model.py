from sqlalchemy import Boolean, Column, Integer, String

from app.database.database import Base


class Aprendiz(Base):
    __tablename__ = "aprendizes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    codigo = Column(String(30), unique=True)

    psicologa_referencia = Column(String(100))

    nivel_suporte = Column(String(30))

    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Aprendiz(nome='{self.nome}')>"