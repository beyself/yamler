from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from yamler import app

#engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True,**app.config['DATABASE_CONNECT_OPTIONS'])
engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True, pool_recycle=3600)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine)) 

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    import yamler.models
    Model.metadata.create_all(bind=engine)

#Model = declarative_base()
Model = declarative_base(name='Model')
Model.query = db_session.query_property()
