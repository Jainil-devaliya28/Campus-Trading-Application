"""
Database Manager - Manages tables and database operations.
"""

from typing import Dict, Optional, List, Any
from .table import Table


class DatabaseManager:
    """Manages database tables and operations."""
    
    def __init__(self, db_name: str):
        """
        Initialize the database manager.
        
        Args:
            db_name: Name of the database
        """
        self.db_name = db_name
        self.tables: Dict[str, Table] = {}
    
    def create_table(self, table_name: str, index_column: str, order: int = 3) -> Table:
        """
        Create a new table in the database.
        
        Args:
            table_name: Name for the table
            index_column: Column to use as index (primary key)
            order: B+ Tree order
            
        Returns:
            The created Table object
        """
        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists")
        
        table = Table(table_name, index_column, order=order)
        self.tables[table_name] = table
        return table
    
    def get_table(self, table_name: str) -> Optional[Table]:
        """
        Retrieve a table by name.
        
        Args:
            table_name: Name of table to retrieve
            
        Returns:
            Table object if exists, else None
        """
        return self.tables.get(table_name)
    
    def drop_table(self, table_name: str) -> bool:
        """
        Drop (delete) a table from the database.
        
        Args:
            table_name: Name of table to drop
            
        Returns:
            True if table existed and was dropped, False otherwise
        """
        if table_name in self.tables:
            del self.tables[table_name]
            return True
        return False
    
    def list_tables(self) -> List[str]:
        """Get list of all table names."""
        return list(self.tables.keys())
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database."""
        stats = {
            'db_name': self.db_name,
            'num_tables': len(self.tables),
            'tables': {}
        }
        
        for name, table in self.tables.items():
            stats['tables'][name] = {
                'record_count': table.count(),
                'index_column': table.index_column
            }
        
        return stats
    
    def __repr__(self):
        return f"DatabaseManager(db='{self.db_name}', tables={list(self.tables.keys())})"
