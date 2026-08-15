from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.aprendiz_model import Aprendiz


class AprendizRepository:

    def listar(self):
        with SessionLocal() as session:
            return session.scalars(select(Aprendiz).order_by(Aprendiz.nome)).all()

    def buscar_por_id(self, aprendiz_id):
        with SessionLocal() as session:
            return session.get(Aprendiz, aprendiz_id)

    def criar(self, nome, codigo, nivel_suporte, dias_atendimento="", horario="", sala="", carga_horaria_aba="", observacoes=""):
        with SessionLocal() as session:
            aprendiz = Aprendiz(
                nome=nome, codigo=codigo, nivel_suporte=nivel_suporte,
                dias_atendimento=dias_atendimento, horario=horario, sala=sala,
                carga_horaria_aba=carga_horaria_aba, observacoes=observacoes,
                status="Ativo", ativo=True,
            )
            session.add(aprendiz)
            session.commit()
            session.refresh(aprendiz)
            return aprendiz

    def atualizar(self, aprendiz_id, nome, codigo, nivel_suporte, dias_atendimento="", horario="", sala="", carga_horaria_aba="", observacoes=""):
        with SessionLocal() as session:
            aprendiz = session.get(Aprendiz, aprendiz_id)
            if aprendiz is None:
                return None
            aprendiz.nome = nome
            aprendiz.codigo = codigo
            aprendiz.nivel_suporte = nivel_suporte
            aprendiz.dias_atendimento = dias_atendimento
            aprendiz.horario = horario
            aprendiz.sala = sala
            aprendiz.carga_horaria_aba = carga_horaria_aba
            aprendiz.observacoes = observacoes
            session.commit()
            session.refresh(aprendiz)
            return aprendiz

    def alterar_status(self, aprendiz_id, ativo):
        with SessionLocal() as session:
            aprendiz = session.get(Aprendiz, aprendiz_id)
            if aprendiz is None:
                return None
            aprendiz.ativo = bool(ativo)
            aprendiz.status = "Ativo" if aprendiz.ativo else "Inativo"
            session.commit()
            session.refresh(aprendiz)
            return aprendiz

    def excluir(self, aprendiz_id):
        with SessionLocal() as session:
            aprendiz = session.get(Aprendiz, aprendiz_id)
            if aprendiz is None:
                return {"sucesso": False, "motivo": "Aprendiz não encontrado."}

            possui_historico = any([
                bool(aprendiz.pendencias),
                bool(aprendiz.documentos),
                bool(aprendiz.supervisoes),
                bool(aprendiz.avaliacoes),
            ])

            if possui_historico:
                return {
                    "sucesso": False,
                    "motivo": "Não é possível excluir um aprendiz que possui histórico clínico. Inative o cadastro para preservá-lo.",
                }

            session.delete(aprendiz)
            session.commit()
            return {"sucesso": True, "motivo": ""}
