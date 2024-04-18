#!/bin/bash

OSTYPE=$(uname)
existing_uvicorn_pid=$(ps aux | grep 'uvicorn' | grep 'separate-python' | grep -v grep | awk '{print $2}')
existing_rq_worker_pid=$(ps aux | grep 'rq worker' | grep 'separate-python' | grep -v grep | awk '{print $2}')

killport() {
    lsof -i :$1 | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox} LISTEN | awk '{print $2}' | xargs kill -9
}

# Check if uvicorn server is running
if [ "$existing_uvicorn_pid" ]; then
    echo "Uvicorn server is already running with PID: $existing_uvicorn_pid. Killing it..."
    kill -9 $existing_uvicorn_pid
fi

# Check if rq worker is running
if [ "$existing_rq_worker_pid" ]; then
    echo "RQ worker is already running with PID: $existing_rq_worker_pid. Killing it..."
    kill -9 $existing_rq_worker_pid
fi

# Run uvicorn server in the background and redirect its output to a log file
if [[ "$OSTYPE" == "Darwin"* ]]; then
    killport 6000
    pipenv run uvicorn src.main:app --reload --port 6000 > uvicorn.log 2>&1 & uvicorn_pid=$!
else
    killport 8000
    pipenv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 & uvicorn_pid=$!
fi

# Run rq worker in the background and redirect its output to a separate log file
pipenv run rq worker > rq_worker.log 2>&1 & rq_worker_pid=$!

echo "Uvicorn server started with PID: $uvicorn_pid"
echo "RQ worker started with PID: $rq_worker_pid"
