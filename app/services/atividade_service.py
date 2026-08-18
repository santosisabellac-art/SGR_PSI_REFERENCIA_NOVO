from app.repositories.atividade_repository import AtividadeRepository


class AtividadeService:

    def __init__(self):
        self.repository = AtividadeRepository()

    def listar_por_aprendiz(self, aprendiz_id):
        return self.repository.listar_por_aprendiz(aprendiz_id)

    def registrar(self, aprendiz_id, tipo, descricao):
        return self.repository.criar(
            aprendiz_id=aprendiz_id,
            tipo=tipo,
            descricao=descricao,
        )
