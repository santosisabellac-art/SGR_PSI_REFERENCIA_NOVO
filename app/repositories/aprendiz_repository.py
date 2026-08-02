from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.aprendiz_model import Aprendiz


class AprendizRepository:

    def listar(self):
        with SessionLocal() as session:
            return session.scalars(
                select(Aprendiz).order_by(Aprendiz.nome)
            ).all()

    def buscar_por_id(self, aprendiz_id):
        with SessionLocal() as session:
            return session.get(Aprendiz, aprendiz_id)

    def criar(
        self,
        nome,
        codigo,
        nivel_suporte,
        dias_atendimento="",
        horario="",
        sala="",
        carga_horaria_aba="",
        observacoes="",
    ):

        with SessionLocal() as session:

            aprendiz = Aprendiz(
                nome=nome,
                codigo=codigo,
                nivel_suporte=nivel_suporte,
                dias_atendimento=dias_atendimento,
                horario=horario,
                sala=sala,
                carga_horaria_aba=carga_horaria_aba,
                observacoes=observacoes,
                status="Ativo",
                ativo=True,
            )

            session.add(aprendiz)

            session.commit()

            session.refresh(aprendiz)

            return aprendiz