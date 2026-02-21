// Mock uuid module
let mockIdCounter = 0;
jest.mock('uuid', () => ({
  v4: jest.fn(() => `test-uuid-${++mockIdCounter}`),
}));

