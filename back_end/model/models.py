from sqlalchemy import Column, Integer, String,ForeignKey,Table
from sqlalchemy.orm import  Mapped, MappedAsDataclass, declared_attr, mapped_column,declarative_base
from sqlalchemy.orm import relationship
from typing import List
# from back_end.database import Base
# 多対多の関係
Base = declarative_base()
issue_action_association = Table(
   'issue_action', Base.metadata,
    Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=True),
    Column('action_id', Integer, ForeignKey('actions.id'), primary_key=True)
)

class IssueModel(Base):
  __tablename__ = 'issues'
  id:Mapped[int] = mapped_column(primary_key=True, index=True,autoincrement=True)
  title:Mapped[str] = mapped_column()
  description:Mapped[str] = mapped_column()
  
  plan:Mapped["PlanModel"] = relationship("PlanModel", back_populates="issue", uselist=False)
  evaluation:Mapped["EvaluationModel"] = relationship("EvaluationModel", back_populates="issue", uselist=False)
  advice:Mapped["AdviceModel"] = relationship("AdviceModel", back_populates="issue", uselist=False)
  
  actions:Mapped[List["ActionModel"]] = relationship(
    "ActionModel",
    secondary=issue_action_association,
    back_populates="issues"
  )
  
class PlanModel(Base):
  __tablename__ = 'plans'
  
  id = Column(Integer, primary_key=True, index=True,autoincrement=True)
  title = Column(String)
  content = Column(String)
  issue_id = Column(Integer, ForeignKey('issues.id',ondelete='CASCADE'),unique=True)
  
  issue = relationship("IssueModel", back_populates="plan")

class ActionModel(Base):
  __tablename__ = 'actions'
  id:Mapped[int] = mapped_column( primary_key=True, index=True, autoincrement=True)
  title:Mapped[str] = mapped_column()
  content:Mapped[str] = mapped_column()
  
  issues:Mapped[List["IssueModel"]] = relationship(
        "IssueModel",
        secondary=issue_action_association,
        back_populates="actions"
    )
  
  
class EvaluationModel(Base):
    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    issue_id = Column(Integer, ForeignKey('issues.id', ondelete="CASCADE"), unique=True)
    
    issue = relationship("IssueModel", back_populates="evaluation")

class AdviceModel(Base):
    __tablename__ = 'advice'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    issue_id = Column(Integer, ForeignKey('issues.id', ondelete="CASCADE"), unique=True)
    
    issue = relationship("IssueModel", back_populates="advice")