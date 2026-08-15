from app.repositories.pendencia_repository import PendenciaRepository


class PendenciaService:

    def __init__(self):
        self.repository = PendenciaRepository()

    # --------------------------

    def listar(self):
        return self.repository.listar()

    # --------------------------

    def listar_por_aprendiz(
        self,
        aprendiz_id,
    ):
        return self.repository.listar_por_aprendiz(
            aprendiz_id
        )

    # --------------------------

    def criar(
        self,
        aprendiz_id,
        titulo,
        descricao="",
    ):

        return self.repository.criar(
            aprendiz_id=aprendiz_id,
            titulo=titulo,
            descricao=descricao,
        )

    # --------------------------

    def concluir(
        self,
        pendencia_id,
    ):

        return self.repository.concluir(
            pendencia_id
        )

    # --------------------------

    def excluir(
        self,
        pendencia_id,
    ):

        return self.repository.excluir(
            pendencia_id
        )