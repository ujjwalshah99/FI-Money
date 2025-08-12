const Product = require('../models/Product');

exports.addProduct = async (req, res) => {
    
    const { name, type, sku, image_url, description, quantity, price } = req.body;

    try {
        let product = await Product.findOne({ sku });

        if (product) {
            return res.status(400).json({ msg: 'Product with this SKU already exists' });
        }

        product = new Product({
            name,
            type,
            sku,
            image_url,
            description,
            quantity,
            price,
        });

        await product.save();

        res.status(201).json({
            msg: 'Product added successfully',
            productId: product.id,
        });
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
};

exports.getProducts = async (req, res) => {
    const page = parseInt(req.query.page, 10) || 1;
    const limit = parseInt(req.query.limit, 10) || 10;
    const skip = (page - 1) * limit;

    try {
        const products = await Product.find().skip(skip).limit(limit);
        const totalProducts = await Product.countDocuments();

        res.json({
            products,
            currentPage: page,
            totalPages: Math.ceil(totalProducts / limit),
            totalProducts,
        });
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
};

exports.updateProductQuantity = async (req, res) => {
    const { quantity } = req.body;

    if (typeof quantity !== 'number' || !Number.isInteger(quantity)) {
        return res.status(400).json({ msg: 'Quantity must be an integer.' });
    }

    try {
        const updatedProduct = await Product.findByIdAndUpdate(
            req.params.id,
            { $set: { quantity } },
            { new: true }
        );

        if (!updatedProduct) {
            return res.status(404).json({ msg: 'Product not found' });
        }

        res.json({
            msg: 'Product quantity updated successfully',
            product: updatedProduct,
        });
    } catch (err) {
        console.error(err.message);
        if (err.kind === 'ObjectId') {
            return res.status(404).json({ msg: 'Product not found' });
        }
        res.status(500).send('Server Error');
    }
};