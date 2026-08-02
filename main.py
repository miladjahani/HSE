import sys
import threading
import uvicorn
import webview
import time
import os

def start_api():
    from api.server import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def main():
    # Start FastAPI in a background thread
    t = threading.Thread(target=start_api, daemon=True)
    t.start()

    # Give the server a moment to start
    time.sleep(1)

    # Start PyWebView pointing to the local server
    # Note: In production (EXE), FastAPI will serve the built React static files on /
    webview.create_window(
        'سامانه یکپارچه مدیریت HSE معدن',
        'http://127.0.0.1:8000',
        width=1280,
        height=800,
        min_size=(1024, 768),
        background_color='#F5F7FA'
    )
    webview.start()

if __name__ == "__main__":
    main()
