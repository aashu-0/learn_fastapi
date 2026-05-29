# code to define sqlalchemy orm models
# here we are creating two database tables (users and posts)


from __future__ import annotations      # enables forward references like in list[Post]
from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
# relationship: using this we can access related objects directly, without using joins
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    
    # defines one to many relationship
    # back_populates: two way sync
    # allows user.posts
    posts: Mapped[list[Post]] = relationship(back_populates="author", cascade="all, delete-orphan")

    # for computed attribute
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return f"/static/profile_pics/default.jpeg"
    

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] =mapped_column(Text, nullable=False)

    #foreign key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(UTC))

    # defines many to one relationship
    # allows post.author to access User objects like post.author.username
    author: Mapped[User] = relationship(back_populates="posts")