from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from yamler import app
#from flask.ext.sqlalchemy import SQLAlchemy

#class nullpool_SQLAlchemy(SQLAlchemy):
#    def apply_driver_hacks(self, app, info, options):
#        super(nullpool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
#        from sqlalchemy.pool import NullPool
#        options['poolclass'] = NullPool
        #del options['pool_size']

#db = SQLAlchemy(app)
#Model = db.Model
#db_session = db.session
#metadata = db.metadata
#conn = db.engine.connect()

engine = create_engine(app.config['DATABASE_URI'], poolclass=NullPool, convert_unicode=True, **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

#conn = engine.connect()
conn = ''

#def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    #import yamler.models
    #Model.metadata.create_all(bind=engine)
#Model = declarative_base()
Model = declarative_base(name='Model')
Model.query = db_session.query_property()
metadata = MetaData(bind=engine)
