import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import os

# custom module
from cosmos.utils.singleton import Singleton
from cosmos.utils.logging import Logger
from cosmos.utils.constants import (
    DB_ISOLATION_LEVELS,
    FILE_DB_DSN_CONSTANT,
)


# init logger
logger = Logger().get_logger()


class Database(metaclass=Singleton):
    '''
    Create a singleton connection pool with the database.
    '''
    def __init__(
        self,
        use_file_db:bool=False,
        db_type:str="postgresql",
    ) -> None:
        self.engine = None

        if use_file_db:
            self.dsn = FILE_DB_DSN_CONSTANT
        else:
            user_name = os.getenv("DB_USER", 'postgres')
            password = os.getenv("DB_PASSWORD", 'postgres')
            host = os.getenv("DB_HOST", 'localhost')
            self.dsn = "{}://{}:{}@{}".format(db_type, user_name, password, host)

        self.BASE = declarative_base()

    def create_engine(
        self,
        pool_size:int=10,
        max_overflow:int=0,
        pool_recycle:int=3600,
        isolation_level:str="REPEATABLE READ"
    ) -> None:
        """
        Create a connection pool with the database.

        Reference: <https://docs.sqlalchemy.org/en/20/core/connections.html#setting-transaction-isolation-levels-including-dbapi-autocommit>

        Args:
            pool_size (int, optional): The size of the SQL connection pool. Defaults to 10.
            max_overflow (int, optional): The max overflow value. Defaults to 0.
            isolation_level (str, optional): The isolation level. Defaults to "REPEATABLE READ".

        Raises:
            ValueError: If the isolation level is not supported.
            Exception: If the engine creation fails.
        """
        try:
            if isolation_level not in DB_ISOLATION_LEVELS:
                raise ValueError(f"Isolation level {isolation_level} is not supported. Supported levels are {DB_ISOLATION_LEVELS}")

            logger.debug(f"Creating a DB engine ({self.dsn}) with pool_size={pool_size}, pool_recycle={pool_recycle} and max_overflow={max_overflow} :: isolation_level={isolation_level}")
            if self.engine is None:
                self.engine = create_engine(
                    self.dsn,
                    pool_size=pool_size,
                    max_overflow=max_overflow,
                    isolation_level=isolation_level,
                    pool_recycle=pool_recycle,
                )
        except Exception as ex:
            logger.error(f"Failed to create a DB engine, {str(ex)}")
            raise ex

    def get_engine(self):
        """Get the database engine.

        Returns:
            Engine: Database engine.
        """
        if self.engine is None:
            self.create_engine()
        return self.engine


    def dispose_connection(self):
        """Close the Database connection pool."""
        self.engine.dispose(True)

    @contextlib.contextmanager
    def get_session(self, cleanup=False):
        engine = self.get_engine()
        session = Session(bind=engine)
        self.Base.metadata.create_all(engine)

        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()

        if cleanup:
            self.Base.metadata.drop_all(engine)

    @contextlib.contextmanager
    def get_conn(self, cleanup=False):
        engine = self.get_engine()
        conn = engine.connect()
        self.Base.metadata.create_all(engine)

        yield conn
        conn.close()

        if cleanup:
            self.Base.metadata.drop_all(engine)
