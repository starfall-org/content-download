from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    create_engine,
    Column,
    BigInteger,
    Boolean,
)

Base = declarative_base()


class Group(Base):
    __tablename__ = "allowed_group"
    id = Column(BigInteger, primary_key=True)
    allowed = Column(Boolean, default=False)


class Database:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///ai.db")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update(self, group_id: int, allowed: bool) -> None:
        group = Group(id=group_id, allowed=allowed)
        self.session.merge(group)
        self.session.commit()

    def get(self, group_id: int) -> bool:
        group = self.session.query(Group).filter_by(id=group_id).first()
        if group:
            return group.allowed
        return False
