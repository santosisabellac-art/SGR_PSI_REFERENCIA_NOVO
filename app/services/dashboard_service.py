from datetime import datetime

from app.services.aprendiz_service import AprendizService
from app.services.documento_service import DocumentoService
from app.services.pendencia_service import PendenciaService


class DashboardService:

    def __init__(self):
        self.aprendiz_service = AprendizService()
        self.documento_service = DocumentoService()
        self.pendencia_service = PendenciaService()

    def listar_aprendizes(self):
        return self.aprendiz_service.listar()

    def aprendizes_ativos(self):
        return [a for a in self.listar_aprendizes() if getattr(a, "ativo", True)]

    def total_aprendizes(self):
        return len(self.aprendizes_ativos())

    def pendencias_abertas(self):
        ativos = {a.id for a in self.aprendizes_ativos()}
        return [
            p for p in self.pendencia_service.listar()
            if not p.concluida and p.aprendiz_id in ativos
        ]

    def resumo_pendencias_abertas(self, pendencias=None, limite=5):
        if pendencias is None:
            pendencias = self.pendencias_abertas()
        return [
            {
                "aprendiz_id": p.aprendiz_id,
                "aprendiz": p.aprendiz.nome if p.aprendiz else "Aprendiz não encontrado",
                "titulo": p.titulo,
            }
            for p in pendencias[:limite]
        ]

    def documentos_pendentes(self):
        ativos = {a.id for a in self.aprendizes_ativos()}
        return [
            d for d in self.documento_service.listar()
            if d.aprendiz_id in ativos
            and self.documento_service.situacao(d) != "Entregue"
        ]

    def documentos_vencidos(self):
        return [
            d for d in self.documentos_pendentes()
            if self.documento_service.situacao(d) == "Vencido"
        ]

    def prioridades(self, limite=10):
        nomes = {a.id: a.nome for a in self.aprendizes_ativos()}
        prioridades = []
        for documento in self.documentos_vencidos():
            prioridades.append({
                "aprendiz_id": documento.aprendiz_id,
                "prioridade": "Documento vencido",
                "aprendiz": nomes.get(documento.aprendiz_id, "Aprendiz não encontrado"),
                "detalhe": documento.tipo,
            })
        for pendencia in self.pendencias_abertas():
            prioridades.append({
                "aprendiz_id": pendencia.aprendiz_id,
                "prioridade": "Pendência aberta",
                "aprendiz": nomes.get(pendencia.aprendiz_id, "Aprendiz não encontrado"),
                "detalhe": pendencia.titulo,
            })
        return prioridades[:limite]

    def agenda_hoje(self):
        nomes_dias = {
            0: ("segunda", "seg"),
            1: ("terça", "terca", "ter"),
            2: ("quarta", "qua"),
            3: ("quinta", "qui"),
            4: ("sexta", "sex"),
            5: ("sábado", "sabado", "sáb", "sab"),
            6: ("domingo", "dom"),
        }
        dias_hoje = nomes_dias[datetime.now().weekday()]
        aprendizes = []

        for aprendiz in self.aprendizes_ativos():
            dias = (aprendiz.dias_atendimento or "").lower()
            if not dias:
                continue
            if any(dia in dias for dia in dias_hoje):
                aprendizes.append({
                    "aprendiz_id": aprendiz.id,
                    "nome": aprendiz.nome,
                    "horario": aprendiz.horario or "Não informado",
                    "sala": aprendiz.sala or "-",
                })

        aprendizes.sort(
            key=lambda x: (
                x["horario"] == "Não informado",
                x["horario"],
                x["nome"].lower(),
            )
        )
        return aprendizes

    def alertas(self):
        alertas = []
        for aprendiz in self.aprendizes_ativos():
            if not aprendiz.sala:
                alertas.append(f"{aprendiz.nome} está sem sala.")
            if not aprendiz.horario:
                alertas.append(f"{aprendiz.nome} está sem horário.")
            if not aprendiz.carga_horaria_aba:
                alertas.append(f"{aprendiz.nome} está sem carga ABA.")
        return alertas

    def resumo(self):
        pendencias_abertas = self.pendencias_abertas()
        documentos_pendentes = self.documentos_pendentes()
        documentos_vencidos = self.documentos_vencidos()
        return {
            "data": datetime.now(),
            "total_aprendizes": self.total_aprendizes(),
            "total_pendencias_abertas": len(pendencias_abertas),
            "total_documentos_pendentes": len(documentos_pendentes),
            "total_documentos_vencidos": len(documentos_vencidos),
            "pendencias_abertas": self.resumo_pendencias_abertas(pendencias_abertas),
            "prioridades": self.prioridades(),
            "agenda": self.agenda_hoje(),
            "alertas": self.alertas(),
        }
