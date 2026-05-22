#!/bin/bash
echo ""
echo "========================================================"
echo "  Proactive LLM Defence Demo"
echo "  Universita degli Studi di Napoli Federico II"
echo "========================================================"
echo ""

# Check Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  Starting Ollama..."
    ollama serve &
    sleep 3
else
    echo "  Ollama already running"
fi

# Install Flask if needed
python3 -c "import flask" 2>/dev/null || pip3 install flask flask-cors --break-system-packages -q

echo ""
echo "  Opening demo at: http://localhost:5050"
echo "  Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 app.py
