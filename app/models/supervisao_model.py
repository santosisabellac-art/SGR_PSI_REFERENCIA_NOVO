from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Supervisao(Base):

    __tablename__ = "supervisoes"

    id = Column(Integer, primary_key=True)

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendizes.id"),
        nullable=False,
    )

    data = Column(Date, nullable=False)

    responsavel = Column(String(150), nullable=False)

    resumo = Column(Text, default="")

    orientacoes = Column(Text, default="")

    proximos_passos = Column(Text, default="")

    aprendiz = relationship(
        "Aprendiz",
        back_populates="supervisoes",
    )
