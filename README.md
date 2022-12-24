# Py Random Chat
A random chat web application built with React & Django.

# Installing development dependencies
Install backend dependencies with `cd backend && pip -r requirements.txt`. Install frontend dependencies with `cd frontend && yarn install`.

# Running
The backend and frontend servers run at `8000` and `3000` ports respectively. After running both servers by the instructions listed
bellow you should be able to acces the app at http://localhost:3000.

## Development
After installing the dependencies run `cd backend && ./run-dev.sh` for the backend server, and ` cd frontend && yarn start ` for the frontend server.

## Production
Run `docker-compose up` from the root directory.
