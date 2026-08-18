from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.atividade_model import Atividade


class AtividadeRepository:

    def listar_por_aprendiz(self, aprendiz_id):
        with SessionLocal() as session:
            return session.scalars(
                select(Atividade)
                .where(Atividade.aprendiz_id == aprendiz_id)
                .order_by(Atividade.criado_em.desc(), Atividade.id.desc())
            ).all()

    def criar(self, aprendiz_id, tipo, descricao):
        with SessionLocal() as session:
            atividade = Atividade(
                aprendiz_id=aprendiz_id,
                tipo=tipo,
                descricao=descricao,
            )
            session.add(atividade)
            session.commit()
            session.refresh(atividade)
            return atividade
