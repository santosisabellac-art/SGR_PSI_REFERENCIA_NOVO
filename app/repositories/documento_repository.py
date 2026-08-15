from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.session import SessionLocal
from app.models.documento_model import Documento


class DocumentoRepository:

    def listar(self):
        consulta = (
            select(Documento)
            .options(joinedload(Documento.aprendiz))
            .order_by(Documento.status, Documento.prazo, Documento.tipo)
        )

        with SessionLocal() as session:
            return session.scalars(consulta).all()

    def criar(
        self,
        aprendiz_id,
        tipo,
        prazo=None,
        observacoes="",
    ):
        with SessionLocal() as session:
            documento = Documento(
                aprendiz_id=aprendiz_id,
                tipo=tipo,
                prazo=prazo,
                observacoes=observacoes,
                status="Pendente",
            )

            session.add(documento)
            session.commit()
            session.refresh(documento)

            return documento

    def atualizar(
        self,
        documento_id,
        aprendiz_id,
        tipo,
        prazo=None,
        observacoes="",
    ):
        with SessionLocal() as session:
            documento = session.get(Documento, documento_id)

            if documento is None:
                return None

            documento.aprendiz_id = aprendiz_id
            documento.tipo = tipo
            documento.prazo = prazo
            documento.observacoes = observacoes

            session.commit()
            session.refresh(documento)

            return documento

    def atualizar_status(self, documento_id, status):
        with SessionLocal() as session:
            documento = session.get(Documento, documento_id)

            if documento is None:
                return None

            documento.status = status
            session.commit()
            session.refresh(documento)

            return documento

    def excluir(self, documento_id):
        with SessionLocal() as session:
            documento = session.get(Documento, documento_id)

            if documento is None:
                return False

            session.delete(documento)
            session.commit()

            return True
