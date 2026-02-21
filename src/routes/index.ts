import { Router } from 'express';
import dataRoutes from './dataRoutes';
import healthRoutes from './healthRoutes';

const router = Router();

router.use('/data', dataRoutes);
router.use('/', healthRoutes);

export default router;
