from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


class DatabaseConnector:
    def __init__(self, db_type: str, db_user: str, db_password: str, db_host: str, db_port: int, db_name: str, safe_mode: bool = True):
        self.db_type = db_type
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.safe_mode = safe_mode
        
        # Build the connection URL
        self.db_url = self._build_db_url()
        self.engine: Engine = create_engine(self.db_url)
    def _build_db_url(self) -> str:
        """Constructs a DB URL based on type."""
        if self.db_type == "postgresql":
            return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        elif self.db_type == "mysql":
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        elif self.db_type == "sqlite":
            return f"sqlite:///{self.db_name}"
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")
    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.engine.connect()
            print("Connection successful!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
    def get_tables(self):
        """Returns a list of tables in the database."""
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            print(f"Error retrieving tables: {e}")
            return []
    def get_columns(self, table_name: str):
        """Returns a list of columns in the specified table."""
        try:
            inspector = inspect(self.engine)
            return inspector.get_columns(table_name)
        except Exception as e:
            print(f"Error retrieving columns for table {table_name}: {e}")
            return []
    def get_schema(self):
        """Extract schema: tables, columns, PKs, FKs."""
        inspector = inspect(self.engine)
        schema = {}

        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            pk = inspector.get_pk_constraint(table_name)
            fks = inspector.get_foreign_keys(table_name)

            schema[table_name] = {
                "columns": [{col['name']: str(col['type'])} for col in columns],
                "primary_key": pk.get("constrained_columns", []),
                "foreign_keys": [
                    {
                        "column": fk['constrained_columns'],
                        "references_table": fk['referred_table'],
                        "references_columns": fk['referred_columns'],
                    }
                    for fk in fks
                ]
            }

        return schema
    def execute_query(self, query: str):
        """Executes a SQL query and returns the results.
        
        In safe mode, prevents destructive operations like DELETE, DROP, TRUNCATE,
        and UPDATE without a WHERE clause.
        """
        if self.safe_mode:
            # Convert to lowercase for case-insensitive checking
            query_lower = query.lower().strip()
            
            # Check for dangerous operations
            dangerous_ops = ['delete from', 'drop table', 'drop database', 'truncate table']
            if any(op in query_lower for op in dangerous_ops):
                raise ValueError("Destructive operations are not allowed in safe mode. "
                               "Set safe_mode=False during initialization to allow these operations.")
            
            # Check for UPDATE without WHERE clause
            if query_lower.startswith('update') and 'where' not in query_lower:
                raise ValueError("UPDATE operations without WHERE clause are not allowed in safe mode. "
                               "Set safe_mode=False during initialization to allow these operations.")
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                return result.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
    def dispose(self):
        """Disposes the engine."""
        try:
            self.engine.dispose()
            print("Engine disposed successfully.")
        except Exception as e:
            print(f"Error disposing the engine: {e}")