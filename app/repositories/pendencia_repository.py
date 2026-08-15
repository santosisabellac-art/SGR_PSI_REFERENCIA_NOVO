from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.pendencia_model import Pendencia


class PendenciaRepository:

    def listar(self):
        with SessionLocal() as session:
            return session.scalars(
                select(Pendencia).order_by(
                    Pendencia.concluida,
                    Pendencia.id.desc(),
                )
            ).all()

    def listar_por_aprendiz(self, aprendiz_id):
        with SessionLocal() as session:
            return session.scalars(
                select(Pendencia)
                .where(Pendencia.aprendiz_id == aprendiz_id)
                .order_by(Pendencia.concluida, Pendencia.id.desc())
            ).all()

    def criar(self, aprendiz_id, titulo, descricao=""):
        with SessionLocal() as session:
            pendencia = Pendencia(
                aprendiz_id=aprendiz_id,
                titulo=titulo,
                descricao=descricao,
            )
            session.add(pendencia)
            session.commit()
            session.refresh(pendencia)
            return pendencia

    def atualizar(self, pendencia_id, titulo, descricao=""):
        with SessionLocal() as session:
            pendencia = session.get(Pendencia, pendencia_id)
            if pendencia is None:
                return None
            pendencia.titulo = titulo
            pendencia.descricao = descricao
            session.commit()
            session.refresh(pendencia)
            return pendencia

    def concluir(self, pendencia_id):
        with SessionLocal() as session:
            pendencia = session.get(Pendencia, pendencia_id)
            if pendencia is None:
                return None
            pendencia.concluida = True
            session.commit()
            session.refresh(pendencia)
            return pendencia

    def reabrir(self, pendencia_id):
        with SessionLocal() as session:
            pendencia = session.get(Pendencia, pendencia_id)
            if pendencia is None:
                return None
            pendencia.concluida = False
            session.commit()
            session.refresh(pendencia)
            return pendencia

    def excluir(self, pendencia_id):
        with SessionLocal() as session:
            pendencia = session.get(Pendencia, pendencia_id)
            if pendencia is None:
                return False
            session.delete(pendencia)
            session.commit()
            return True
