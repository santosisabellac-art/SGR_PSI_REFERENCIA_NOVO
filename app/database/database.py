from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///database/sgr_psicologa.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def criar_banco():
    from app.models.aprendiz_model import Aprendiz
    from app.models.atividade_model import Atividade
    from app.models.avaliacao_model import Avaliacao
    from app.models.documento_model import Documento
    from app.models.pendencia_model import Pendencia
    from app.models.supervisao_model import Supervisao

    Base.metadata.create_all(bind=engine)
