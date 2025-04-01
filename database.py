from sqlalchemy import create_engine, String, Integer, DateTime
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class REPORTS(Base):
    __tablename__ = "reports"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    complaint: Mapped[str] = mapped_column(String(1000), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

def insert_report(user_id: int, complaint: str, engine):
    try:
        with Session(engine) as session:
            report = REPORTS(
                user_id=user_id,
                complaint=complaint
            )
            session.add(report)
            session.commit()
            return True
    except Exception as e:
        print(f"Error inserting report: {e}")
        session.rollback()
        return False

def create_db(engine) -> None:
    try:
        Base.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database: {e}")

DATABASE_URL = "sqlite:///bot_database.sqlite"
engine = create_engine(DATABASE_URL, echo=True)
create_db(engine)