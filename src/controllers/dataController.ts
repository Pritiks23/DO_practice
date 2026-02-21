import { Request, Response, NextFunction } from 'express';
import { dataService } from '../services/dataService';
import { AppError } from '../middleware/errorHandler';

export const ingestData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { data, metadata } = req.body;

    if (!data || typeof data !== 'object') {
      throw new AppError(400, 'Invalid data: data must be an object');
    }

    const record = await dataService.ingestData(data, metadata);

    res.status(201).json({
      success: true,
      data: record,
    });
  } catch (error) {
    next(error);
  }
};

export const processData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;

    const processedRecord = await dataService.processData(id);

    res.status(200).json({
      success: true,
      data: processedRecord,
    });
  } catch (error) {
    if (error instanceof Error && error.message.includes('not found')) {
      next(new AppError(404, error.message));
    } else {
      next(error);
    }
  }
};

export const getData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;

    const record = await dataService.getData(id);

    if (!record) {
      throw new AppError(404, `Record with id ${id} not found`);
    }

    res.status(200).json({
      success: true,
      data: record,
    });
  } catch (error) {
    next(error);
  }
};

export const getAllData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = parseInt(req.query.limit as string) || 100;
    const offset = parseInt(req.query.offset as string) || 0;

    const records = await dataService.getAllData(limit, offset);
    const stats = dataService.getStats();

    res.status(200).json({
      success: true,
      data: records,
      pagination: {
        limit,
        offset,
        total: stats.total,
      },
      stats,
    });
  } catch (error) {
    next(error);
  }
};

export const deleteData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;

    const deleted = await dataService.deleteData(id);

    if (!deleted) {
      throw new AppError(404, `Record with id ${id} not found`);
    }

    res.status(200).json({
      success: true,
      message: `Record with id ${id} deleted successfully`,
    });
  } catch (error) {
    next(error);
  }
};
