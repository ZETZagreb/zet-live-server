const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serviraj statičke fileove
app.use(express.static(__dirname));

// Početna stranica
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', time: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`🚋 ZETko server radi na portu ${PORT}`);
});
