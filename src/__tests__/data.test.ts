import request from 'supertest';
import { createApp } from '../app';

const app = createApp();

describe('Data API Endpoints', () => {
  let createdRecordId: string;

  describe('POST /api/v1/data', () => {
    it('should ingest new data successfully', async () => {
      const testData = {
        data: {
          sensor: 'temperature',
          value: 25.5,
          unit: 'celsius',
        },
        metadata: {
          source: 'sensor-001',
        },
      };

      const response = await request(app).post('/api/v1/data').send(testData).expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data).toHaveProperty('timestamp');
      expect(response.body.data.processed).toBe(false);
      expect(response.body.data.data).toEqual(testData.data);
      expect(response.body.data.metadata).toEqual(testData.metadata);

      createdRecordId = response.body.data.id;
    });

    it('should reject invalid data (missing data field)', async () => {
      const response = await request(app).post('/api/v1/data').send({}).expect(400);

      expect(response.body.error).toHaveProperty('message');
      expect(response.body.error.statusCode).toBe(400);
    });

    it('should reject invalid data (data is not an object)', async () => {
      const response = await request(app)
        .post('/api/v1/data')
        .send({ data: 'not an object' })
        .expect(400);

      expect(response.body.error).toBeDefined();
    });
  });

  describe('GET /api/v1/data/:id', () => {
    it('should retrieve a specific data record', async () => {
      const response = await request(app).get(`/api/v1/data/${createdRecordId}`).expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(createdRecordId);
    });

    it('should return 404 for non-existent record', async () => {
      const fakeId = '00000000-0000-0000-0000-000000000000';
      const response = await request(app).get(`/api/v1/data/${fakeId}`).expect(404);

      expect(response.body.error).toHaveProperty('message');
      expect(response.body.error.statusCode).toBe(404);
    });
  });

  describe('GET /api/v1/data', () => {
    it('should retrieve all data records', async () => {
      const response = await request(app).get('/api/v1/data').expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body).toHaveProperty('pagination');
      expect(response.body).toHaveProperty('stats');
      expect(response.body.stats).toHaveProperty('total');
      expect(response.body.stats).toHaveProperty('processed');
      expect(response.body.stats).toHaveProperty('unprocessed');
    });

    it('should support pagination', async () => {
      const response = await request(app).get('/api/v1/data?limit=5&offset=0').expect(200);

      expect(response.body.pagination.limit).toBe(5);
      expect(response.body.pagination.offset).toBe(0);
    });
  });

  describe('POST /api/v1/data/:id/process', () => {
    it('should process a data record', async () => {
      const response = await request(app)
        .post(`/api/v1/data/${createdRecordId}/process`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.processed).toBe(true);
      expect(response.body.data).toHaveProperty('processingTimestamp');
      expect(response.body.data).toHaveProperty('processingResult');
      expect(response.body.data.processingResult.status).toBe('success');
    });

    it('should return 404 for non-existent record', async () => {
      const fakeId = '00000000-0000-0000-0000-000000000000';
      const response = await request(app).post(`/api/v1/data/${fakeId}/process`).expect(404);

      expect(response.body.error).toHaveProperty('message');
      expect(response.body.error.statusCode).toBe(404);
    });

    it('should handle already processed records', async () => {
      const response = await request(app)
        .post(`/api/v1/data/${createdRecordId}/process`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.processed).toBe(true);
    });
  });

  describe('DELETE /api/v1/data/:id', () => {
    it('should delete a data record', async () => {
      const response = await request(app).delete(`/api/v1/data/${createdRecordId}`).expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('deleted successfully');
    });

    it('should return 404 when deleting non-existent record', async () => {
      const response = await request(app).delete(`/api/v1/data/${createdRecordId}`).expect(404);

      expect(response.body.error.statusCode).toBe(404);
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for undefined routes', async () => {
      const response = await request(app).get('/api/v1/undefined-route').expect(404);

      expect(response.body.error).toHaveProperty('message');
      expect(response.body.error.statusCode).toBe(404);
    });
  });
});
