# Gunicorn config file
worker_class = 'uvicorn.workers.UvicornWorker'

# daemon mode
daemon = True

# Server Socket
bind = '0.0.0.0:8000'

# Worker Processes
workers = 4
