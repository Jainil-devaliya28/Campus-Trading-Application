"""
Table abstraction for the DBMS.
Maps indexed keys to stored records/values.
"""

from typing import Any, List, Tuple, Optional, Dict
from .bplustree import BPlusTree


class Table:
    """Represents a database table with B+ Tree indexing."""
    
    def __init__(self, table_name: str, index_column: str, order: int = 3):
        """
        Initialize a table.
        
        Args:
            table_name: Name of the table
            index_column: Name of the column to index (primary key)
            order: B+ Tree order
        """
        self.table_name = table_name
        self.index_column = index_column
        self.bplustree = BPlusTree(order=order)
        self.records = {}  # Map from key to full record
        self.schema = {}  # Column definitions
    
    def define_schema(self, schema: Dict[str, str]) -> None:
        """
        Define table schema.
        
        Args:
            schema: Dictionary mapping column names to data types
        """
        self.schema = schema
    
    def insert(self, key: int, record: Dict[str, Any]) -> None:
        """
        Insert a record into the table.
        
        Args:
            key: Index key (usually primary key)
            record: Dictionary containing all column values
        """
        self.records[key] = record
        self.bplustree.insert(key, key)  # Value is the record key
    
    def search(self, key: int) -> Optional[Dict[str, Any]]:
        """
        Search for a record by key.
        
        Args:
            key: Key to search for
            
        Returns:
            Record dictionary if found, else None
        """
        result = self.bplustree.search(key)
        if result is not None:
            return self.records.get(result)
        return None
    
    def delete(self, key: int) -> bool:
        """
        Delete a record from the table.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deletion succeeded, False otherwise
        """
        if key in self.records:
            del self.records[key]
            self.bplustree.delete(key)
            return True
        return False
    
    def update(self, key: int, new_record: Dict[str, Any]) -> bool:
        """
        Update a record in the table.
        
        Args:
            key: Key of record to update
            new_record: New record data
            
        Returns:
            True if update succeeded, False if key not found
        """
        if key not in self.records:
            return False
        
        self.records[key] = new_record
        return self.bplustree.update(key, key)
    
    def range_query(self, start_key: int, end_key: int) -> List[Dict[str, Any]]:
        """
        Retrieve all records within a key range.
        
        Args:
            start_key: Start of range (inclusive)
            end_key: End of range (inclusive)
            
        Returns:
            List of records in range
        """
        results = []
        key_pairs = self.bplustree.range_query(start_key, end_key)
        
        for key, _ in key_pairs:
            if key in self.records:
                results.append(self.records[key])
        
        return results
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all records in the table.
        
        Returns:
            List of all records
        """
        results = []
        pairs = self.bplustree.get_all()
        
        for key, _ in pairs:
            if key in self.records:
                results.append(self.records[key])
        
        return results
    
    def count(self) -> int:
        """Get number of records in table."""
        return len(self.records)
    
    def __repr__(self):
        return f"Table(name={self.table_name}, records={len(self.records)})"
