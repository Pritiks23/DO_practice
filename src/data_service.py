"""
Data service for managing data records.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from src.types import DataRecord, ProcessedData, ProcessingResult
from src.logger import logger


class DataService:
    """Service for managing data records."""
    
    def __init__(self):
        """Initialize the data service."""
        self.data_store: Dict[str, Union[DataRecord, ProcessedData]] = {}
    
    async def ingest_data(
        self, 
        data: Dict[str, Any], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> DataRecord:
        """
        Ingest new data.
        
        Args:
            data: Data to ingest
            metadata: Optional metadata
            
        Returns:
            Created data record
        """
        record = DataRecord(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            data=data,
            processed=False,
            metadata=metadata
        )
        
        self.data_store[record.id] = record
        logger.info(f"Data ingested with id: {record.id}")
        
        return record
    
    async def process_data(self, record_id: str) -> ProcessedData:
        """
        Process a data record.
        
        Args:
            record_id: ID of the record to process
            
        Returns:
            Processed data record
            
        Raises:
            ValueError: If record not found
        """
        record = self.data_store.get(record_id)
        
        if not record:
            raise ValueError(f"Record with id {record_id} not found")
        
        if record.processed:
            return record  # type: ignore
        
        processed_record = ProcessedData(
            id=record.id,
            timestamp=record.timestamp,
            data=record.data,
            processed=True,
            metadata=record.metadata,
            processingTimestamp=datetime.utcnow(),
            processingResult=ProcessingResult(
                status="success",
                message="Data processed successfully"
            )
        )
        
        self.data_store[record_id] = processed_record
        logger.info(f"Data processed with id: {record_id}")
        
        return processed_record
    
    async def get_data(self, record_id: str) -> Optional[Union[DataRecord, ProcessedData]]:
        """
        Get a data record by ID.
        
        Args:
            record_id: ID of the record to retrieve
            
        Returns:
            Data record or None if not found
        """
        return self.data_store.get(record_id)
    
    async def get_all_data(
        self, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[Union[DataRecord, ProcessedData]]:
        """
        Get all data records with pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of data records
        """
        all_data = list(self.data_store.values())
        return all_data[offset:offset + limit]
    
    async def delete_data(self, record_id: str) -> bool:
        """
        Delete a data record.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            True if deleted, False if not found
        """
        if record_id in self.data_store:
            del self.data_store[record_id]
            logger.info(f"Data deleted with id: {record_id}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about stored data.
        
        Returns:
            Dictionary with total, processed, and unprocessed counts
        """
        all_data = list(self.data_store.values())
        processed = sum(1 for record in all_data if record.processed)
        unprocessed = len(all_data) - processed
        
        return {
            "total": len(all_data),
            "processed": processed,
            "unprocessed": unprocessed
        }


# Global instance
data_service = DataService()
