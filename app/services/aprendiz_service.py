from app.repositories.aprendiz_repository import AprendizRepository


class AprendizService:

    def __init__(self):
        self.repository = AprendizRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, aprendiz_id):
        return self.repository.buscar_por_id(aprendiz_id)

    def criar(
        self,
        nome,
        codigo=None,
        psicologa_referencia=None,
        nivel_suporte=None,
    ):
        return self.repository.criar(
            nome=nome,
            codigo=codigo,
            psicologa_referencia=psicologa_referencia,
            nivel_suporte=nivel_suporte,
        )