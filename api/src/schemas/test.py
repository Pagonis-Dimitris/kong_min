from src import ma
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field

from src.models.auth import PortalUser, PortalCompanies, Products, Ips

class CompaniesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PortalCompanies
        include_relationships = True
        load_instance = True 
        ordered = True