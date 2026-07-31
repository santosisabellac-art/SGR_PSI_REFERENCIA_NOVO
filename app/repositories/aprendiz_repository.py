from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.aprendiz_model import Aprendiz


class AprendizRepository:

    def listar(self):
        with SessionLocal() as session:
            return session.scalars(
                select(Aprendiz)
                .order_by(Aprendiz.nome)
            ).all()

    def buscar_por_id(self, aprendiz_id: int):
        with SessionLocal() as session:
            return session.get(Aprendiz, aprendiz_id)

    def criar(
        self,
        nome,
        codigo=None,
        psicologa_referencia=None,
        nivel_suporte=None,
    ):
        with SessionLocal() as session:

            aprendiz = Aprendiz(
                nome=nome,
                codigo=codigo,
                psicologa_referencia=psicologa_referencia,
                nivel_suporte=nivel_suporte,
                ativo=True,
            )

            session.add(aprendiz)
            session.commit()
            session.refresh(aprendiz)

            return aprendiz