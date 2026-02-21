import request from 'supertest';
import { createApp } from '../app';

const app = createApp();

describe('Health Endpoints', () => {
  describe('GET /api/v1/health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/api/v1/health').expect(200);

      expect(response.body).toHaveProperty('status', 'healthy');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('uptime');
      expect(response.body).toHaveProperty('version');
      expect(typeof response.body.uptime).toBe('number');
    });
  });

  describe('GET /api/v1/ready', () => {
    it('should return readiness status', async () => {
      const response = await request(app).get('/api/v1/ready').expect(200);

      expect(response.body).toHaveProperty('status', 'ready');
      expect(response.body).toHaveProperty('timestamp');
    });
  });
});
