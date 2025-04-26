from .config import engine, Base
from .models import Evaluacion

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db() 