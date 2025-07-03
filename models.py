# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
SHAKHA_NAMES = [
    "Nagagiri", "Maheshwara", "Chiranjeevi", "Vasudeva",
    "Keshava", "Brindavana", "Arehalli", "Ramanjaneya", "Kanaka"
]

class Swayamsevak(Base):
    __tablename__ = 'swayamsevaks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    pincode = Column(String)
    dob = Column(String)
    bloodgroup = Column(String)
    education = Column(String)
    profession = Column(String)
    work = Column(String)
    sanghShikshan = Column(String)
    sanghaResponsibility = Column(String)
    sanghOrganizationName = Column(String)
    otherResponsibility = Column(String)
    shakhe = Column(String)
    vasati = Column(String)
    upavasati = Column(String)
