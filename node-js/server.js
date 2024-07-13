const express = require('express');
const app = express();
const PORT = 5000;

// In-memory message queue
const messages = [];

app.use(express.json());

// Endpoint to serve the main page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html');
});

app.get('/events-page', (req,res) => {
    res.sendFile(__dirname + '/templates/events.html');
});

// Endpoint for clients to send messages
app.post('/send', (req, res) => {
    const data = req.body;
    const message = data.message;
    messages.push(message);  // Add message to the queue
    res.status(200).json({ status: 'Message received' });
});

// Endpoint for SSE
app.get('/events', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const sendEvent = () => {
        if (messages.length > 0) {
            const message = messages.shift();  // Get the first message and remove it from the array
            res.write(`data: ${message}\n\n`); // Send the message directly as a string
        }
    };

    // Send an event every second if there are messages
    const intervalId = setInterval(sendEvent, 1000);

    req.on('close', () => {
        clearInterval(intervalId);
        res.end();
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
