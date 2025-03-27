from flask import Flask, request
from flask_socketio import SocketIO
import SupervisorAgent as SAgent
import threading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app,
                  cors_allowed_origins="*",
                  ping_timeout=300,  # 5 minutes
                  ping_interval=15,  # 15 seconds
                  max_http_buffer_size=100 * 1024 * 1024,  # 100MB
                  engineio_logger=True,
                  async_mode='threading')


active_connections = {}

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    active_connections[sid] = time.time()
    logger.info(f"Client connected: {sid}")
    

    def keepalive_task():
        while sid in active_connections:
            try:
                socketio.emit('heartbeat', {'ts': time.time()}, room=sid)
                time.sleep(20)
            except:
                break
    
    threading.Thread(target=keepalive_task, daemon=True).start()

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in active_connections:
        del active_connections[sid]
    logger.info(f"Client disconnected: {sid}")

@socketio.on('client_keepalive')
def handle_client_keepalive(data):
    sid = request.sid
    if sid in active_connections:
        active_connections[sid] = time.time()  # Update last active time
        socketio.emit('keepalive_ack', {'server_time': time.time()}, room=sid)

# Your existing prompt handler
@socketio.on('prompt')
def handle_message(data):
    thread = threading.Thread(target=SAgent.execute, args=(data['prompt'], socketio))
    thread.daemon = True
    thread.start()
    return '', 202

if __name__ == '__main__':
    host = '10.56.18.60'
    port = 5000
    logger.info(f"Starting server with ping_timeout=300, ping_interval=15")
    socketio.run(app,
                host=host,
                port=port,
                debug=True,
                use_reloader=False)