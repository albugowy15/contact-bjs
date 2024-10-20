# Skill Test

## Overview

This project is a full-stack web application designed to demonstrate various skills in web development. It consists of a React.js frontend with Tailwind CSS for styling, and a Flask backend with PostgreSQL as the database.

## Project Structure

The project is organized into two main directories:

- `frontend/`: Contains the React.js and Tailwind CSS frontend application
- `backend/`: Houses the Flask and PostgreSQL backend application

## Technologies Used

### Frontend

- React.js
- Tailwind CSS

## Backend

- Flask (Python)
- PostgreSQL

## DevOps

- Docker
- Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose
- Postman (for API testing and documentation)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/albugowy15/contact-bjs.git
   cd contact-bjs`
   ```
2. No additional installation steps are required as the project uses Docker.

## Running the Project

To run the entire project using Docker Compose, execute the following command in the root directory of the project:

```sh
cp ./frontend/.env.example ./frontend/.env
docker-compose up
```

This command will build and start both the frontend and backend services.

- The frontend will be available at: `http://localhost:3000`
- The backend API will be accessible at: `http://localhost:5000`

To stop the application, use:

```sh
docker-compose down
```

## API Documentation

The API documentation for this project is available as a Postman collection. To access and use the API documentation:

1. Download the Postman collection JSON file from the project repository (`contact-app.postman.collection.json`).
2. Open Postman on your local machine.
3. Click on "Import" in Postman.
4. Choose the downloaded JSON file to import the collection.
5. Once imported, you'll have access to all documented API endpoints, including request methods, URL, headers, and body examples.

This Postman collection provides a comprehensive and interactive way to explore and test the API endpoints.
