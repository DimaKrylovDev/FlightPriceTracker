from db.database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

 
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[str]

    
    

    