from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.supervisao_model import Supervisao


class SupervisaoRepository:

    def listar_por_aprendiz(self, aprendiz_id):
        consulta = (
            select(Supervisao)
            .where(Supervisao.aprendiz_id == aprendiz_id)
            .order_by(Supervisao.data.desc(), Supervisao.id.desc())
        )

        with SessionLocal() as session:
            return session.scalars(consulta).all()

    def criar(
        self,
        aprendiz_id,
        data,
        responsavel,
        resumo,
        orientacoes="",
        proximos_passos="",
    ):
        with SessionLocal() as session:
            supervisao = Supervisao(
                aprendiz_id=aprendiz_id,
                data=data,
                responsavel=responsavel,
                resumo=resumo,
                orientacoes=orientacoes,
                proximos_passos=proximos_passos,
            )

            session.add(supervisao)
            session.commit()
            session.refresh(supervisao)

            return supervisao

    def excluir(self, supervisao_id):
        with SessionLocal() as session:
            supervisao = session.get(Supervisao, supervisao_id)

            if supervisao is None:
                return False

            session.delete(supervisao)
            session.commit()

            return True
