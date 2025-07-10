from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SubscriptionType(Base):
    __tablename__ = "subscription_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_type = Column(String, nullable=False)
    subscription_period = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentType(Base):
    __tablename__ = "payment_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_type = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserDetail(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chats = relationship("UserChat", back_populates="user")

class UserChat(Base):
    __tablename__ = "users_chat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_details.id"), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("UserDetail", back_populates="chats")
    chat_details = relationship("UserChatDetail", back_populates="chat")

class UserChatDetail(Base):
    __tablename__ = "chat_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("users_chat.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    file_upload_url = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chat = relationship("UserChat", back_populates="chat_details")

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_details.id"), nullable=False)
    subscription_type_id = Column(Integer, ForeignKey("subscription_types.id"), nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    subscribed_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserPaymentInfo(Base):
    __tablename__ = "users_payment_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_details.id"), nullable=False)
    payment_type_id = Column(Integer, ForeignKey("payment_types.id"), nullable=False)
    transaction_no = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)