from app.repositories.aprendiz_repository import AprendizRepository


class AprendizService:
    def __init__(self):
        self.repository = AprendizRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, aprendiz_id):
        return self.repository.buscar_por_id(aprendiz_id)

    def criar(self, nome, codigo, nivel_suporte, dias_atendimento="", horario="", sala="", carga_horaria_aba="", observacoes=""):
        return self.repository.criar(nome, codigo, nivel_suporte, dias_atendimento, horario, sala, carga_horaria_aba, observacoes)

    def atualizar(self, aprendiz_id, nome, codigo, nivel_suporte, dias_atendimento="", horario="", sala="", carga_horaria_aba="", observacoes=""):
        return self.repository.atualizar(aprendiz_id, nome, codigo, nivel_suporte, dias_atendimento, horario, sala, carga_horaria_aba, observacoes)

    def alterar_status(self, aprendiz_id, ativo):
        return self.repository.alterar_status(aprendiz_id, ativo)

    def excluir(self, aprendiz_id):
        return self.repository.excluir(aprendiz_id)
