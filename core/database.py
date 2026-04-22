from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql://postgres:tutuca05@localhost:5432/food_store_2"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
