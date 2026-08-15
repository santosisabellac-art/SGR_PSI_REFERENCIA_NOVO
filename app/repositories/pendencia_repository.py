from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.pendencia_model import Pendencia


class PendenciaRepository:

    def __init__(self):

        self.db: Session = SessionLocal()

    # -------------------------

    def listar(self):

        return (
            self.db.query(Pendencia)
            .order_by(Pendencia.concluida)
            .all()
        )

    # -------------------------

    def listar_por_aprendiz(
        self,
        aprendiz_id,
    ):

        return (
            self.db.query(Pendencia)
            .filter(
                Pendencia.aprendiz_id == aprendiz_id
            )
            .order_by(Pendencia.concluida)
            .all()
        )

    # -------------------------

    def criar(
        self,
        aprendiz_id,
        titulo,
        descricao="",
    ):

        pendencia = Pendencia(

            aprendiz_id=aprendiz_id,

            titulo=titulo,

            descricao=descricao,

        )

        self.db.add(pendencia)

        self.db.commit()

        self.db.refresh(pendencia)

        return pendencia

    # -------------------------

    def concluir(
        self,
        pendencia_id,
    ):

        pendencia = self.db.get(
            Pendencia,
            pendencia_id,
        )

        if pendencia:

            pendencia.concluida = True

            self.db.commit()

        return pendencia

    # -------------------------

    def excluir(
        self,
        pendencia_id,
    ):

        pendencia = self.db.get(
            Pendencia,
            pendencia_id,
        )

        if pendencia:

            self.db.delete(pendencia)

            self.db.commit()