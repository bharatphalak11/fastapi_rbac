from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # Import models so metadata is registered
    from app.models import user, project

    # Create all tables in the DB
    SQLModel.metadata.create_all(engine)


# If we want to track the model changes then we can use Alembic,
# It is a lightweight database migration tool for SQLAlchemy and SQLModel