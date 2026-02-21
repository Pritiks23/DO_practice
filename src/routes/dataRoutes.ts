import { Router } from 'express';
import {
  ingestData,
  processData,
  getData,
  getAllData,
  deleteData,
} from '../controllers/dataController';
import { validateRequest } from '../middleware/validator';

const router = Router();

router.post(
  '/',
  validateRequest([
    { field: 'data', required: true, type: 'object' },
  ]),
  ingestData
);

router.get('/', getAllData);

router.get('/:id', getData);

router.post('/:id/process', processData);

router.delete('/:id', deleteData);

export default router;
