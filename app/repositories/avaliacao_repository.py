from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.avaliacao_model import Avaliacao


class AvaliacaoRepository:

    def listar_por_aprendiz(self, aprendiz_id):
        consulta = (
            select(Avaliacao)
            .where(Avaliacao.aprendiz_id == aprendiz_id)
            .order_by(Avaliacao.data.desc(), Avaliacao.id.desc())
        )

        with SessionLocal() as session:
            return session.scalars(consulta).all()

    def criar(
        self,
        aprendiz_id,
        data,
        instrumento,
        responsavel,
        sintese,
        proximos_passos="",
    ):
        with SessionLocal() as session:
            avaliacao = Avaliacao(
                aprendiz_id=aprendiz_id,
                data=data,
                instrumento=instrumento,
                responsavel=responsavel,
                sintese=sintese,
                proximos_passos=proximos_passos,
            )

            session.add(avaliacao)
            session.commit()
            session.refresh(avaliacao)

            return avaliacao

    def excluir(self, avaliacao_id):
        with SessionLocal() as session:
            avaliacao = session.get(Avaliacao, avaliacao_id)

            if avaliacao is None:
                return False

            session.delete(avaliacao)
            session.commit()

            return True
