
from app import session, Base

class BaseModel(Base):
    model = None
    conn = None

    def __init__(self, model):
        self.model = model

    
