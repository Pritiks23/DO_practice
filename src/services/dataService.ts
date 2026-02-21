import { v4 as uuidv4 } from 'uuid';
import { DataRecord, ProcessedData } from '../types';
import { logger } from '../utils/logger';

class DataService {
  private dataStore: Map<string, DataRecord | ProcessedData> = new Map();

  async ingestData(data: Record<string, unknown>, metadata?: Record<string, unknown>): Promise<DataRecord> {
    const record: DataRecord = {
      id: uuidv4(),
      timestamp: new Date(),
      data,
      processed: false,
      metadata,
    };

    this.dataStore.set(record.id, record);
    logger.info('Data ingested', { id: record.id });

    return record;
  }

  async processData(id: string): Promise<ProcessedData> {
    const record = this.dataStore.get(id);

    if (!record) {
      throw new Error(`Record with id ${id} not found`);
    }

    if (record.processed) {
      return record as ProcessedData;
    }

    const processedRecord: ProcessedData = {
      ...record,
      processed: true,
      processingTimestamp: new Date(),
      processingResult: {
        status: 'success',
        message: 'Data processed successfully',
      },
    };

    this.dataStore.set(id, processedRecord);
    logger.info('Data processed', { id });

    return processedRecord;
  }

  async getData(id: string): Promise<DataRecord | ProcessedData | null> {
    return this.dataStore.get(id) || null;
  }

  async getAllData(limit = 100, offset = 0): Promise<(DataRecord | ProcessedData)[]> {
    const allData = Array.from(this.dataStore.values());
    return allData.slice(offset, offset + limit);
  }

  async deleteData(id: string): Promise<boolean> {
    const result = this.dataStore.delete(id);
    if (result) {
      logger.info('Data deleted', { id });
    }
    return result;
  }

  getStats() {
    const allData = Array.from(this.dataStore.values());
    const processed = allData.filter((record) => record.processed).length;
    const unprocessed = allData.length - processed;

    return {
      total: allData.length,
      processed,
      unprocessed,
    };
  }
}

export const dataService = new DataService();
