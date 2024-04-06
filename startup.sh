#!/bin/bash

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
}

# Function to kill a process by name
kill_process() {
    pkill -f "$1"
}

# Check if uvicorn server is running
if is_process_running "uvicorn"; then
    echo "Uvicorn server is already running. Killing the process..."
    kill_process "uvicorn"
fi

# Check if rq worker is running
if is_process_running "rq worker"; then
    echo "RQ worker is already running. Killing the process..."
    kill_process "rq worker"
fi

# Run uvicorn server in the background and redirect its output to a log file
pipenv run uvicorn src.main:app --reload --host 0.0.0.0 > uvicorn.log 2>&1 &
uvicorn_pid=$!

# Run rq worker in the background and redirect its output to a separate log file
pipenv run rq worker > rq_worker.log 2>&1 &
rq_worker_pid=$!

echo "Uvicorn server started with PID: $uvicorn_pid"
echo "RQ worker started with PID: $rq_worker_pid"
