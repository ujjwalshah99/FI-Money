
const express = require('express');
const router = express.Router();
const {
    addProduct,
    getProducts,
    updateProductQuantity,
} = require('../controllers/productController');
const authMiddleware = require('../middleware/authMiddleware');

router.post('/', authMiddleware, addProduct);
router.get('/', authMiddleware, getProducts);
router.put('/:id/quantity', authMiddleware, updateProductQuantity);

module.exports = router;