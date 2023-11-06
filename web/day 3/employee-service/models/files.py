from sqlalchemy import Column, Integer, String
from flask import request
from app import session, Base

class Employee(Base):

    __tablename__ = "employee_files"

    name = Column(String)
    id = Column(Integer, primary_key=True)
    path = Column(String)
    

    def __init__(self, name, id, path):
        super().__init__()
        self.name = name
        self.id = id
        self.path = path

    def __str__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "address": self.address
        })

    def save(self):
        session.add(self)

    def get_by_id(self):
        emp = Employee.query.filter_by(id=self.id).first()
        return emp
    
    def delete(self):
        Employe.query.filter_by(id=self.id).delete()
        

    def update(self):
        emp = session.query(Employee).filter_by(id=id).first()
        emp.name = self.name or emp.name
        emp.address = self.address or emp.address
        return session.commit()
    
    def validate(self):
        val_name = len(self.name) > 0 and len(self.name) < 256
        val_addr = len(self.address) > 0 and len(self.address) < 1024
        return val_name and val_addr

