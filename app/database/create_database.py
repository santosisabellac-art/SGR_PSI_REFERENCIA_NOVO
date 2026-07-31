from app.database.database import Base, engine

# Importar todos os models aqui
from app.models.aprendiz_model import Aprendiz


def create_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()
    print("Banco de dados criado com sucesso!")