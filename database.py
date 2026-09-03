from sqlalchemy import create_engine #import create_engine to manage database connections and execute SQL statements
from sqlalchemy.orm import sessionmaker #import sessionmaker to generate new Session objects for interacting with the database
from sqlalchemy.ext.declarative import declarative_base #import declarative_base to create a base class for defining database models (SQL tables)

#1. Neon.tech Cloud PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_un1lLHtR5FxY@ep-holy-thunder-b3cu8d7z-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

#2. Create the SQLAlchemy engine that connects Python to Neon Cloud
#engine holds the connections to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#3. Create a SessionLocal factory class for database transactions 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

#4. Create a Base class for ORM models to inherit from on Day 8!!
Base = declarative_base()