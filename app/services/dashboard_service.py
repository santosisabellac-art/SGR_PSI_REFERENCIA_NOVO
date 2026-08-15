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

    def total_aprendizes(self):

        return len(
            [
                a
                for a in self.listar_aprendizes()
                if getattr(a, "ativo", True)
            ]
        )

    def pendencias_abertas(self):
        return [
            pendencia
            for pendencia in self.pendencia_service.listar()
            if not pendencia.concluida
        ]

    def resumo_pendencias_abertas(self, pendencias=None, limite=5):
        if pendencias is None:
            pendencias = self.pendencias_abertas()

        return [
            {
                "aprendiz": (
                    pendencia.aprendiz.nome
                    if pendencia.aprendiz
                    else "Aprendiz não encontrado"
                ),
                "titulo": pendencia.titulo,
            }
            for pendencia in pendencias[:limite]
        ]

    def documentos_pendentes(self):
        return [
            documento
            for documento in self.documento_service.listar()
            if self.documento_service.situacao(documento) != "Entregue"
        ]

    def documentos_vencidos(self):
        return [
            documento
            for documento in self.documentos_pendentes()
            if self.documento_service.situacao(documento) == "Vencido"
        ]

    def prioridades(self, limite=10):
        nomes = {
            aprendiz.id: aprendiz.nome
            for aprendiz in self.listar_aprendizes()
        }

        prioridades = []

        for documento in self.documentos_vencidos():
            prioridades.append(
                {
                    "prioridade": "Documento vencido",
                    "aprendiz": nomes.get(
                        documento.aprendiz_id,
                        "Aprendiz não encontrado",
                    ),
                    "detalhe": documento.tipo,
                }
            )

        for pendencia in self.pendencias_abertas():
            prioridades.append(
                {
                    "prioridade": "Pendência aberta",
                    "aprendiz": nomes.get(
                        pendencia.aprendiz_id,
                        "Aprendiz não encontrado",
                    ),
                    "detalhe": pendencia.titulo,
                }
            )

        return prioridades[:limite]

    def agenda_hoje(self):

        aprendizes = []

        for aprendiz in self.listar_aprendizes():

            if not aprendiz.horario:
                continue

            aprendizes.append(
                {
                    "nome": aprendiz.nome,
                    "horario": aprendiz.horario,
                    "sala": aprendiz.sala or "-",
                }
            )

        aprendizes.sort(
            key=lambda x: x["horario"]
        )

        return aprendizes

    def alertas(self):

        alertas = []

        for aprendiz in self.listar_aprendizes():

            if not aprendiz.sala:

                alertas.append(
                    f"{aprendiz.nome} está sem sala."
                )

            if not aprendiz.horario:

                alertas.append(
                    f"{aprendiz.nome} está sem horário."
                )

            if not aprendiz.carga_horaria_aba:

                alertas.append(
                    f"{aprendiz.nome} está sem carga ABA."
                )

        return alertas

    def resumo(self):
        pendencias_abertas = self.pendencias_abertas()
        documentos_pendentes = self.documentos_pendentes()
        documentos_vencidos = [
            documento
            for documento in documentos_pendentes
            if self.documento_service.situacao(documento) == "Vencido"
        ]

        return {
            "data": datetime.now(),
            "total_aprendizes": self.total_aprendizes(),
            "total_pendencias_abertas": len(pendencias_abertas),
            "total_documentos_pendentes": len(documentos_pendentes),
            "total_documentos_vencidos": len(documentos_vencidos),
            "pendencias_abertas": self.resumo_pendencias_abertas(
                pendencias_abertas
            ),
            "prioridades": self.prioridades(),
            "agenda": self.agenda_hoje(),
            "alertas": self.alertas(),
        }
