from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Atividade(Base):
    __tablename__ = "atividades"

    id = Column(Integer, primary_key=True, index=True)
    aprendiz_id = Column(Integer, ForeignKey("aprendizes.id"), nullable=False, index=True)
    tipo = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.now, nullable=False)

    aprendiz = relationship("Aprendiz", back_populates="atividades")
