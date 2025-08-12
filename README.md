# Fi-Money

A financial management application built with Node.js, Express, and MongoDB.

## Features

- User authentication with JWT tokens
- Secure password hashing with bcrypt
- RESTful API design
- MongoDB database integration
- Environment variable configuration
- Docker containerization support

## Tech Stack

- **Backend**: Node.js, Express.js
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: JSON Web Tokens (JWT)
- **Security**: bcryptjs for password hashing
- **Development**: Nodemon for auto-restart
- **Containerization**: Docker & Docker Compose

## Prerequisites

Before running this application, make sure you have one of the following setups:

### Option 1: Local Development
- [Node.js](https://nodejs.org/) (v14 or higher)
- [MongoDB](https://www.mongodb.com/) (local installation or MongoDB Atlas)
- npm or yarn package manager

### Option 2: Docker Development (Recommended)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation & Setup

### Option 1: Traditional Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fimoney
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory and add your environment variables:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/fimoney
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=7d
```

### Option 2: Docker Setup (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd fimoney
```

2. Create a `.env` file in the root directory (optional - Docker Compose has built-in environment variables):
```env
PORT=5000
MONGO_URI=mongodb://admin:password123@mongodb:27017/fimoney?authSource=admin
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d
```

3. Create an `init-mongo.js` file in the root directory to initialize the database:
```javascript
// init-mongo.js
db = db.getSiblingDB('fimoney');
db.createUser({
  user: 'admin',
  pwd: 'password123',
  roles: [
    {
      role: 'readWrite',
      db: 'fimoney'
    }
  ]
});
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

This will start both the application (on port 5000) and MongoDB database (with authentication) in containers.

## Usage

### Development Mode

#### Traditional Development
To run the application in development mode with auto-restart:

```bash
npm run dev
```

#### Docker Development
To run with Docker Compose in development mode:

```bash
docker-compose up
```

For development with live reload:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Production Mode

#### Traditional Production
To run the application in production:

```bash
node server.js
```

#### Docker Production
To run with Docker Compose in production:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

The server will start on port 5000 (Docker) or the port specified in your `.env` file (local development).

### Docker Commands

#### Useful Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f mongodb

# Rebuild containers
docker-compose up --build

# Access application container
docker-compose exec app bash

# Access MongoDB container
docker-compose exec mongodb mongosh -u admin -p password123 --authenticationDatabase admin

# Remove volumes (reset database)
docker-compose down -v
```

## Project Structure

```
fimoney/
├── server.js             # Main server file
├── routes/               # API route handlers
├── middleware/           # Custom middleware (authMiddleware)
├── models/               # MongoDB models
├── controllers/          # Route controllers
├── Screenshot/           # API endpoint screenshots
│   ├── register.jpg
│   ├── login.jpg
│   ├── postProduct.jpg
│   ├── getProduct.jpg
│   └── updateProductById.jpg
├── docker-compose.yml    # Docker Compose configuration
├── init-mongo.js        # MongoDB initialization script
├── Dockerfile           # Docker image configuration
├── package.json         # Project dependencies and scripts
├── .env                 # Environment variables (not in repo)
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```

## API Endpoints

### Authentication

#### POST /register - Register a new user
Register a new user account with email and password.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword",
}
```

![Register Endpoint Screenshot](Screenshot/register.jpg)
*Screenshot showing the register endpoint in action*

---

#### POST /login - User login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

![Login Endpoint Screenshot](Screenshot/login.jpg)
*Screenshot showing the login endpoint in action*

---

### Products Management

#### POST / - Add new product (Protected)
Add a new product to the inventory. Requires authentication.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "name": "Product Name",
  "type": "Category Type",
  "sku": "UNIQUE-SKU-123",
  "image_url": "http://yourdomain.com/image.jpg",
  "description": "Detailed product description goes here.",
  "quantity": 0,
  "price": 0.00
}

```

![Add Product Endpoint Screenshot](Screenshot/postProduct.jpg)
*Screenshot showing the add product endpoint in action*

---

#### GET / - Get all products (Protected)
Retrieve all products from inventory. Requires authentication.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

![Get Products Endpoint Screenshot](Screenshot/getProduct.jpg)
*Screenshot showing the get products endpoint in action*

---

#### PUT /:id/quantity - Update product quantity (Protected)
Update the quantity of a specific product. Requires authentication.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "quantity": 150
}
```

![Update Product Quantity Screenshot](Screenshot/updateProductById.jpg)
*Screenshot showing the update product quantity endpoint in action*

## Environment Variables

| Variable | Description | Required | Docker Notes |
|----------|-------------|----------|--------------|
| `PORT` | Server port number | No (default: 5000) | Exposed through Docker on port 5000 |
| `MONGO_URI` | MongoDB connection string | Yes | Use `mongodb://admin:password123@mongodb:27017/fimoney?authSource=admin` for Docker |
| `JWT_SECRET` | Secret key for JWT tokens | Yes | |
| `JWT_EXPIRES_IN` | Token expiration time | No (default: 7d) | |

### Environment Configuration Notes

- **Local Development**: Use `mongodb://localhost:27017/fimoney`
- **Docker Development**: Use `mongodb://admin:password123@mongodb:27017/fimoney?authSource=admin`
- **Production**: Use your production MongoDB URI (Atlas, etc.)

### MongoDB Authentication (Docker)

The Docker setup includes MongoDB with authentication enabled:
- **Username**: `admin`
- **Password**: `password123`
- **Database**: `fimoney`
- **Auth Database**: `admin`

## Screenshots

To help with API testing and documentation, this project includes screenshots of each endpoint in action. Screenshots are stored in the `Screenshot/` directory and show:

- Request/response examples using tools like Postman or Insomnia
- Proper header configuration for protected routes
- Sample request bodies and expected responses
- Authentication flow demonstration

### Adding Screenshots

1. Create a `Screenshot/` directory in your project root
2. Test each endpoint using an API client (Postman, Insomnia, etc.)
3. Take screenshots showing:
   - The endpoint URL and method
   - Request headers (especially Authorization for protected routes)
   - Request body (for POST/PUT requests)
   - Response data
4. Save screenshots with descriptive names as shown in the project structure

## Development

### Prerequisites for Development

- Install nodemon globally (optional): `npm install -g nodemon`

### Running Tests

```bash
# Traditional setup
npm test

# Docker setup
docker-compose exec app npm test
```

### Code Style

This project follows standard JavaScript conventions. Consider using ESLint and Prettier for consistent code formatting.

## Docker Development Workflow

1. **Initial Setup**: `docker-compose up --build`
2. **Daily Development**: `docker-compose up`
3. **View Logs**: `docker-compose logs -f app`
4. **Database Access**: `docker-compose exec mongodb mongosh -u admin -p password123 --authenticationDatabase admin`
5. **Stop Services**: `docker-compose down`

## Troubleshooting

### Docker Issues

- **Port conflicts**: Ensure ports 5000 and 27017 are not in use
- **Database connection**: Verify MongoDB container is running with `docker-compose ps`
- **Authentication errors**: Check MongoDB credentials (admin/password123)
- **Volume issues**: Try `docker-compose down -v` to remove volumes and restart
- **Network issues**: Ensure containers can communicate via `fimoney-network`

### Common Development Issues

- **Module not found**: Run `npm install` or `docker-compose up --build`
- **Database connection**: Check your MongoDB URI in `.env`
- **Authentication errors**: Verify JWT_SECRET is set

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security Considerations

- Passwords are hashed using bcryptjs
- JWT tokens are used for authentication
- Environment variables store sensitive data
- Input validation should be implemented
- Rate limiting should be considered for production
- Docker containers run with appropriate security settings

---

**Note**: Remember to add your `.env` file to `.gitignore` to avoid committing sensitive information to version control.
