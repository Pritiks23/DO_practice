import { dataService } from '../services/dataService';

describe('DataService', () => {
  beforeEach(() => {
    // Clear data between tests
    dataService['dataStore'].clear();
  });

  describe('ingestData', () => {
    it('should ingest data and return a record', async () => {
      const data = { test: 'value' };
      const metadata = { source: 'test' };

      const record = await dataService.ingestData(data, metadata);

      expect(record).toHaveProperty('id');
      expect(record).toHaveProperty('timestamp');
      expect(record.data).toEqual(data);
      expect(record.metadata).toEqual(metadata);
      expect(record.processed).toBe(false);
    });
  });

  describe('processData', () => {
    it('should process unprocessed data', async () => {
      const record = await dataService.ingestData({ test: 'value' });
      const processed = await dataService.processData(record.id);

      expect(processed.processed).toBe(true);
      expect(processed).toHaveProperty('processingTimestamp');
      expect(processed).toHaveProperty('processingResult');
    });

    it('should throw error for non-existent record', async () => {
      await expect(dataService.processData('fake-id')).rejects.toThrow('not found');
    });

    it('should return already processed data', async () => {
      const record = await dataService.ingestData({ test: 'value' });
      await dataService.processData(record.id);
      const processed = await dataService.processData(record.id);

      expect(processed.processed).toBe(true);
    });
  });

  describe('getData', () => {
    it('should retrieve data by id', async () => {
      const record = await dataService.ingestData({ test: 'value' });
      const retrieved = await dataService.getData(record.id);

      expect(retrieved).toEqual(record);
    });

    it('should return null for non-existent id', async () => {
      const result = await dataService.getData('fake-id');
      expect(result).toBeNull();
    });
  });

  describe('getAllData', () => {
    it('should retrieve all data', async () => {
      await dataService.ingestData({ test: '1' });
      await dataService.ingestData({ test: '2' });

      const all = await dataService.getAllData();
      expect(all.length).toBe(2);
    });

    it('should support pagination', async () => {
      for (let i = 0; i < 5; i++) {
        await dataService.ingestData({ test: i });
      }

      const paginated = await dataService.getAllData(2, 1);
      expect(paginated.length).toBe(2);
    });
  });

  describe('deleteData', () => {
    it('should delete existing data', async () => {
      const record = await dataService.ingestData({ test: 'value' });
      const result = await dataService.deleteData(record.id);

      expect(result).toBe(true);
      const retrieved = await dataService.getData(record.id);
      expect(retrieved).toBeNull();
    });

    it('should return false for non-existent data', async () => {
      const result = await dataService.deleteData('fake-id');
      expect(result).toBe(false);
    });
  });

  describe('getStats', () => {
    it('should return correct statistics', async () => {
      const record1 = await dataService.ingestData({ test: '1' });
      await dataService.ingestData({ test: '2' });
      await dataService.processData(record1.id);

      const stats = dataService.getStats();
      expect(stats.total).toBe(2);
      expect(stats.processed).toBe(1);
      expect(stats.unprocessed).toBe(1);
    });
  });
});
