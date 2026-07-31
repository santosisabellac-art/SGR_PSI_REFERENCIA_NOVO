from app.services.aprendiz_service import AprendizService

service = AprendizService()

aprendiz = service.criar(
    nome="Aprendiz Teste",
    codigo="TESTE001",
    psicologa_referencia="Isabella",
    nivel_suporte="Nível 2",
)

print(aprendiz.id)
print(aprendiz.nome)

print(service.listar())