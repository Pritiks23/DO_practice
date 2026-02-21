import { Router } from 'express';
import { healthCheck, readiness } from '../controllers/healthController';

const router = Router();

router.get('/health', healthCheck);
router.get('/ready', readiness);

export default router;
