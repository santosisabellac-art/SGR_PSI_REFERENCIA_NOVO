from datetime import date

from app.repositories.documento_repository import DocumentoRepository


class DocumentoService:

    def __init__(self):
        self.repository = DocumentoRepository()

    def listar(self):
        return self.repository.listar()

    def criar(
        self,
        aprendiz_id,
        tipo,
        prazo=None,
        observacoes="",
    ):
        return self.repository.criar(
            aprendiz_id=aprendiz_id,
            tipo=tipo,
            prazo=prazo,
            observacoes=observacoes,
        )

    def atualizar(
        self,
        documento_id,
        aprendiz_id,
        tipo,
        prazo=None,
        observacoes="",
    ):
        return self.repository.atualizar(
            documento_id=documento_id,
            aprendiz_id=aprendiz_id,
            tipo=tipo,
            prazo=prazo,
            observacoes=observacoes,
        )

    def marcar_como_entregue(self, documento_id):
        return self.repository.atualizar_status(
            documento_id,
            "Entregue",
        )

    def excluir(self, documento_id):
        return self.repository.excluir(documento_id)

    def situacao(self, documento):
        if documento.status == "Entregue":
            return "Entregue"

        if documento.prazo and documento.prazo < date.today():
            return "Vencido"

        return "Pendente"
