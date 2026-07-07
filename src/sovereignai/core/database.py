"""Database engine, session, repository, and unit-of-work abstractions."""
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sovereignai.config.settings import get_settings

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_session() -> Generator[Session, None, None]:
    """Yield a database session for request-scoped dependency injection."""
    session = SessionLocal()
    try: yield session
    finally: session.close()

class UnitOfWork:
    """Transaction boundary implementing commit and rollback semantics."""
    def __init__(self, session: Session) -> None: self.session = session
    def __enter__(self) -> 'UnitOfWork': return self
    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.session.rollback() if exc else self.session.commit()
