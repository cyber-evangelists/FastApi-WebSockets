

# FastApi-WebSockets

## Introduction
This project is a full-stack application that consists of a React frontend and a Python backend. The frontend is responsible for rendering the user interface and handling user input, which includes validation and sanitization through the `useFormik` hook. It communicates with the backend via websockets, ensuring a seamless data exchange in JSON format, although it can handle non-JSON data types for specific messages.

The backend, developed in Python, leverages websockets to create an interactive communication channel with the frontend. It integrates MongoDB for data persistence, allowing for operations such as adding, retrieving, and searching posts. The system uses a `ConnectionManager` class to manage websocket connections securely and employs MongoDB's `ObjectID` for database entry identification.

## Features
- Real-time communication between frontend and backend using websockets.
- Input validation and sanitization in the frontend using useFormik.
- Data persistence with MongoDB, supporting CRUD operations on posts.
- Secure websocket connection management.

## Prerequisites
Before you start, ensure you have the following installed:
- Node.js and npm (for the frontend)
- Python 3.x (for the backend)
- MongoDB (for database operations)

## Setup and Installation

### Frontend
1. Clone the repository and navigate to the frontend directory:
   ```bash
   cd path/to/repository/frontend
   ```
2. Install the required npm packages:
   ```bash
   npm install
   ```

### Backend
1. Navigate to the backend directory from the root of the repository:
   ```bash
   cd path/to/repository/backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Frontend
1. Start the frontend application with npm:
   ```bash
   npm start
   ```
   This will launch the React application, typically available at `http://localhost:3000`.

### Backend
1. Start the backend server using uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   This command will start the backend server, making it listen for incoming websocket connections and HTTP requests.

## Usage

Once both the frontend and backend are running, the application will facilitate real-time communication between the client and server. The React frontend allows users to perform actions such as viewing posts in a table, adding new posts, and searching for specific posts. These actions are communicated to the Python backend via websockets, which interacts with MongoDB to perform the requested operations.

- **Adding a Post**: The user can add a new post through the frontend interface. This post is then sent to the backend, which inserts the post into the MongoDB database.
- **Viewing Posts**: The frontend retrieves and displays posts from the backend in a table format.
- **Searching for a Post**: Users can search for posts by ID through the frontend. The search query is handled by the backend, which performs the lookup in MongoDB.

## Troubleshooting

- **WebSocket Connection Issues**: Ensure both the frontend and backend servers are running and that there are no network issues preventing communication.
- **Database Operations**: Verify that MongoDB is running and accessible by the backend server for operations to succeed.

## Contributing

Contributions to the project are welcome. Please follow the standard fork and pull request workflow if you wish to contribute.
