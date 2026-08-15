from app.repositories.supervisao_repository import SupervisaoRepository


class SupervisaoService:

    def __init__(self):
        self.repository = SupervisaoRepository()

    def listar_por_aprendiz(self, aprendiz_id):
        return self.repository.listar_por_aprendiz(aprendiz_id)

    def criar(
        self,
        aprendiz_id,
        data,
        responsavel,
        resumo,
        orientacoes="",
        proximos_passos="",
    ):
        return self.repository.criar(
            aprendiz_id=aprendiz_id,
            data=data,
            responsavel=responsavel,
            resumo=resumo,
            orientacoes=orientacoes,
            proximos_passos=proximos_passos,
        )

    def atualizar(
        self,
        supervisao_id,
        data,
        responsavel,
        resumo,
        orientacoes="",
        proximos_passos="",
    ):
        return self.repository.atualizar(
            supervisao_id=supervisao_id,
            data=data,
            responsavel=responsavel,
            resumo=resumo,
            orientacoes=orientacoes,
            proximos_passos=proximos_passos,
        )

    def excluir(self, supervisao_id):
        return self.repository.excluir(supervisao_id)
