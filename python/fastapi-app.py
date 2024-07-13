from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
import asyncio

app = FastAPI()

# Asynchronous queue to handle messages
messages = asyncio.Queue()

async def message_provider():
    try:
        while True:
            # Wait until a message is available
            message = await messages.get()
            # Properly format the message for SSE
            yield f"data: {message}\n\n"
            # Needed to ensure the message is sent immediately
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        # Handle the case where the client disconnects
        print("Stream was cancelled")
        raise

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/events-page", response_class=HTMLResponse)
async def event_page():
    with open('templates/events.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/send")
async def send(request: Request):
    data = await request.json()
    # Place the received message into the queue
    await messages.put(data['message'])
    return JSONResponse({"status": "Message received"})

@app.get("/events", response_class=StreamingResponse)
async def events():
    # Use async generator and set media type for SSE
    return StreamingResponse(message_provider(), media_type='text/event-stream')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
