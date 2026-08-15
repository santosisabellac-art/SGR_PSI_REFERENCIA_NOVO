from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True)

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendizes.id"),
        nullable=False,
    )

    data = Column(Date, nullable=False)

    instrumento = Column(String(150), nullable=False)

    responsavel = Column(String(150), nullable=False)

    sintese = Column(Text, default="")

    proximos_passos = Column(Text, default="")

    aprendiz = relationship(
        "Aprendiz",
        back_populates="avaliacoes",
    )
