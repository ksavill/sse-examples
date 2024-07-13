from flask import Flask, request, jsonify, render_template, Response
import queue
import threading

app = Flask(__name__)

# Thread-safe queue to hold messages
messages = queue.Queue()

def message_provider():
    while True:
        # Block until a message is available and then yield it
        message = messages.get()
        yield f"data: {message}\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events-page')
def event_page():
    return render_template('events.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    # Put the message into the queue
    messages.put(data['message'])  # Assuming JSON contains 'message' key
    return jsonify(status='Message received'), 200

@app.route('/events')
def events():
    # Set up the response as an event stream
    return Response(message_provider(), mimetype='text/event-stream')

if __name__ == "__main__":
    # Start the Flask application in a separate thread
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=5000)).start()