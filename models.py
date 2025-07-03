# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
SHAKHA_NAMES = [
    "Nagagiri", "Maheshwara", "Chiranjeevi", "Vasudeva",
    "Keshava", "Brindavana", "Arehalli", "Ramanjaneya", "Kanaka"
]

Base = declarative_base()

class Swayamsevak(Base):
    __tablename__ = 'swayamsevaks'

    id = Column(Integer, primary_key=True)
    
    # API-required fields
    prant = Column(String)
    vibhag = Column(String)
    bhag = Column(String)
    nagar = Column(String)

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
