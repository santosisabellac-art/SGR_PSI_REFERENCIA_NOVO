from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Pendencia(Base):

    __tablename__ = "pendencias"

    id = Column(Integer, primary_key=True)

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendizes.id"),
        nullable=False,
    )

    titulo = Column(
        String(200),
        nullable=False,
    )

    descricao = Column(
        Text,
        default="",
    )

    concluida = Column(
        Boolean,
        default=False,
    )

    aprendiz = relationship(
        "Aprendiz",
        back_populates="pendencias",
    )