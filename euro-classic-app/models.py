# from . import db


# class Car(BaseModel):
#     id: Optional[PydantiObjectId] = Field(None, alies='_id')
#     slug: str
#     name: str
#     year = db.Column(db.Integer(6), index=True)
#     make = db.Column(db.String(64), index=True)
#     model = db.Column(db.String(64), index=True)
#     chasis =db.Column(db.String(64), index=True)
#     price = db.Column(db.Float(12),index=True)
    
#     def __repr__(self):
#         return '<User {}>'.format(self.Car)