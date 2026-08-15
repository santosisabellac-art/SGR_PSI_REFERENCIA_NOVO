from app.repositories.avaliacao_repository import AvaliacaoRepository


class AvaliacaoService:

    def __init__(self):
        self.repository = AvaliacaoRepository()

    def listar_por_aprendiz(self, aprendiz_id):
        return self.repository.listar_por_aprendiz(aprendiz_id)

    def criar(self, aprendiz_id, data, instrumento, responsavel, sintese, proximos_passos=""):
        return self.repository.criar(
            aprendiz_id=aprendiz_id,
            data=data,
            instrumento=instrumento,
            responsavel=responsavel,
            sintese=sintese,
            proximos_passos=proximos_passos,
        )

    def atualizar(self, avaliacao_id, data, instrumento, responsavel, sintese, proximos_passos=""):
        return self.repository.atualizar(
            avaliacao_id=avaliacao_id,
            data=data,
            instrumento=instrumento,
            responsavel=responsavel,
            sintese=sintese,
            proximos_passos=proximos_passos,
        )

    def excluir(self, avaliacao_id):
        return self.repository.excluir(avaliacao_id)
