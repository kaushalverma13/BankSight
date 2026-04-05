"""
Database Connection and Session Management
Enterprise-grade database connectivity for BankSight
"""

import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool, QueuePool
from config.settings import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_ECHO,
    DB_POOL_SIZE,
    DB_MAX_OVERFLOW,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Enterprise Database Connection Manager"""
    
    _engine = None
    _session_factory = None
    _scoped_session = None
    
    @classmethod
    def initialize(cls, reset=False):
        """Initialize database connection pool"""
        if reset or cls._engine is None:
            try:
                cls._engine = create_engine(
                    SQLALCHEMY_DATABASE_URI,
                    echo=SQLALCHEMY_ECHO,
                    poolclass=QueuePool,
                    pool_size=DB_POOL_SIZE,
                    max_overflow=DB_MAX_OVERFLOW,
                    pool_pre_ping=True,  # Verify connections before using
                    pool_recycle=3600,  # Recycle connections every hour
                    connect_args={
                        "connect_timeout": 10,
                        "application_name": "banksight",
                    }
                )
                
                # Setup event listeners
                cls._setup_event_listeners()
                
                # Create session factory
                cls._session_factory = sessionmaker(bind=cls._engine)
                cls._scoped_session = scoped_session(cls._session_factory)
                
                logger.info("Database connection pool initialized successfully")
                return cls._engine
                
            except Exception as e:
                logger.error(f"Failed to initialize database: {str(e)}")
                raise
    
    @classmethod
    def _setup_event_listeners(cls):
        """Setup SQLAlchemy event listeners"""
        try:
            @event.listens_for(cls._engine, "connect")
            def receive_connect(dbapi_conn, connection_record):
                """Execute on connection establish"""
                if hasattr(dbapi_conn, 'autocommit'):
                    dbapi_conn.autocommit = False
        except Exception as e:
            logger.debug(f"Could not setup connect event: {e}")
    
    @classmethod
    def get_engine(cls):
        """Get database engine"""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
    
    @classmethod
    def get_session(cls):
        """Get new database session"""
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory()
    
    @classmethod
    def get_scoped_session(cls):
        """Get thread-scoped session"""
        if cls._scoped_session is None:
            cls.initialize()
        return cls._scoped_session
    
    @classmethod
    @contextmanager
    def session_scope(cls):
        """Provide a transactional scope for database operations"""
        session = cls.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database transaction failed: {str(e)}")
            raise
        finally:
            session.close()
    
    @classmethod
    def create_all_tables(cls):
        """Create all database tables"""
        try:
            from src.database.models import Base
            engine = cls.get_engine()
            Base.metadata.create_all(engine)
            logger.info("All database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            raise
    
    @classmethod
    def drop_all_tables(cls):
        """Drop all database tables (use with caution)"""
        try:
            from src.database.models import Base
            engine = cls.get_engine()
            Base.metadata.drop_all(engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop tables: {str(e)}")
            raise
    
    @classmethod
    def dispose_engine(cls):
        """Dispose database connection pool"""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            cls._scoped_session = None
            logger.info("Database connection pool disposed")
    
    @classmethod
    def health_check(cls):
        """Check database health"""
        try:
            with cls.session_scope() as session:
                session.execute("SELECT 1")
            logger.info("Database health check passed")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False


# Repository Base Class
class BaseRepository:
    """Base repository for common database operations"""
    
    def __init__(self, model):
        self.model = model
    
    def create(self, session, **kwargs):
        """Create new record"""
        instance = self.model(**kwargs)
        session.add(instance)
        return instance
    
    def get_by_id(self, session, id):
        """Get record by ID"""
        return session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, session, skip=0, limit=100):
        """Get all records with pagination"""
        return session.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, session, id, **kwargs):
        """Update record by ID"""
        record = self.get_by_id(session, id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
        return record
    
    def delete(self, session, id):
        """Delete record by ID"""
        record = self.get_by_id(session, id)
        if record:
            session.delete(record)
        return record
    
    def filter(self, session, **kwargs):
        """Filter records by attributes"""
        query = session.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()


# Initialize on import
try:
    DatabaseManager.initialize()
except Exception as e:
    logger.warning(f"Database not available at startup: {str(e)}")
