const express = require('express');
const path = require('path');
const https = require('https');

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

// ============================================================
// PROXY za zet.ficko.dev (rješava CORS problem)
// ============================================================
app.get('/proxy/vr/:vr', (req, res) => {
    const vr = req.params.vr;
    const date = req.query.date || getTodayString();
    
    const url = `https://zet.ficko.dev/${vr}?date=${date}`;
    
    console.log(`📡 Proxy: ${url}`);
    
    https.get(url, (apiRes) => {
        let data = '';
        
        apiRes.on('data', (chunk) => {
            data += chunk;
        });
        
        apiRes.on('end', () => {
            // Postavi CORS headere
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Content-Type', 'application/json');
            
            if (apiRes.statusCode === 200) {
                try {
                    const json = JSON.parse(data);
                    res.json(json);
                } catch (e) {
                    res.status(500).json({ error: 'Invalid JSON', raw: data.substring(0, 200) });
                }
            } else {
                res.status(apiRes.statusCode).json({ 
                    error: `API returned ${apiRes.statusCode}`,
                    url: url
                });
            }
        });
    }).on('error', (err) => {
        console.error('❌ Proxy greška:', err.message);
        res.status(500).json({ error: err.message });
    });
});

// Pomoćna funkcija za današnji datum
function getTodayString() {
    const d = new Date();
    return `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`;
}

app.listen(PORT, () => {
    console.log(`🚋 ZETko server radi na portu ${PORT}`);
    console.log(`🌐 Otvori: http://localhost:${PORT}`);
    console.log(`📡 Proxy: /proxy/vr/{VR}?date={YYYYMMDD}`);
});
