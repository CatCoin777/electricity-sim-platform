#!/bin/bash
echo "Starting Electricity Market Simulation Platform..."
echo

echo "Starting Backend Server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting Frontend Server..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo
echo "Platform is starting up..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop all services..."

# Wait for user to stop
wait 