from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Documento(Base):

    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendizes.id"),
        nullable=False,
    )

    tipo = Column(
        String(100),
        nullable=False,
    )

    prazo = Column(Date, nullable=True)

    status = Column(
        String(20),
        nullable=False,
        default="Pendente",
    )

    observacoes = Column(Text, default="")

    aprendiz = relationship(
        "Aprendiz",
        back_populates="documentos",
    )
