from sqlalchemy import Column, Integer, String
from flask import request
from app import session, Base


class Employee(Base):
    __tablename__ = "employee"

    name = Column(String)
    id = Column(Integer, primary_key=True)
    address = Column(String)
    pic_id = Column(String)

    def __init__(self, name, id, address, pic_id='default'):
        super().__init__()
        self.name = name
        self.id = id
        self.address = address
        self.pic_id = 'default'

    def __str__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "address": self.address
        })

    def __cache__(self):
        return {
            'key': 'emp_{}'.format(self.id),
            'value': str(self)
        }

    def save(self):
        session.add(self)
        session.commit()

    def get_by_id(self):
        emp = session.query(Employee).filter_by(id=self.id).first()
        return emp
    
    def delete(self):
        emp = session.query(Employee).filter_by(id=self.id).first()
        session.delete(emp)
        session.commit()

    def update(self):
        emp = session.query(Employee).filter_by(id=id).first()
        emp.name = self.name or emp.name
        emp.address = self.address or emp.address
        return session.commit()
    
    def validate(self):
        val_name = len(self.name) > 0 and len(self.name) < 256
        val_addr = len(self.address) > 0 and len(self.address) < 1024
        return val_name and val_addr

