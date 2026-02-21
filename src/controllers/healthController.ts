import { Request, Response } from 'express';
import { HealthCheckResponse } from '../types';

const startTime = Date.now();

export const healthCheck = (_req: Request, res: Response) => {
  const uptime = (Date.now() - startTime) / 1000;

  const healthResponse: HealthCheckResponse = {
    status: 'healthy',
    timestamp: new Date(),
    uptime,
    version: process.env.npm_package_version || '1.0.0',
  };

  res.status(200).json(healthResponse);
};

export const readiness = (_req: Request, res: Response) => {
  res.status(200).json({
    status: 'ready',
    timestamp: new Date(),
  });
};
