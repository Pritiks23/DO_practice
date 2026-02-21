export interface DataRecord {
  id: string;
  timestamp: Date;
  data: Record<string, unknown>;
  processed: boolean;
  metadata?: {
    source?: string;
    version?: string;
    [key: string]: unknown;
  };
}

export interface ProcessedData extends DataRecord {
  processed: true;
  processingTimestamp: Date;
  processingResult?: {
    status: 'success' | 'error';
    message?: string;
    [key: string]: unknown;
  };
}

export interface ApiError {
  message: string;
  statusCode: number;
  details?: unknown;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: Date;
  uptime: number;
  version: string;
  dependencies?: {
    database?: 'connected' | 'disconnected';
    [key: string]: string | undefined;
  };
}
