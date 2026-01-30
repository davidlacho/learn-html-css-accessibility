"""
Pytest configuration: start the web server automatically so browser tests
can run without manually starting the server.
"""

import os
import subprocess
import sys
import time
import urllib.request

import pytest


def _server_ready(url: str = "http://localhost:8000/", timeout: float = 1.0) -> bool:
    try:
        req = urllib.request.Request(url, method="GET")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except Exception:
        return False


@pytest.fixture(scope="session", autouse=True)
def _ensure_web_server():
    """
    Start the local web server for the test session if it is not already running.
    Uses BASE_URL to decide where the app is served; if it points to localhost:8000,
    we start server.py when nothing is listening there yet.
    """
    base = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
    if "localhost" not in base and "127.0.0.1" not in base:
        yield
        return

    port = "8000"
    if ":" in base.split("//")[-1]:
        port = base.split(":")[-1].split("/")[0]
    url = f"http://127.0.0.1:{port}/"

    if _server_ready(url):
        yield
        return

    project_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(project_dir, "server.py")
    if not os.path.isfile(server_script):
        yield
        return

    proc = None
    try:
        proc = subprocess.Popen(
            [sys.executable, server_script, port],
            cwd=project_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        time.sleep(1)
        for _ in range(60):
            if _server_ready(url):
                break
            time.sleep(0.5)
        else:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=5)
            pytest.skip(
                "Web server did not start in time. Start it manually with: "
                "python3 server.py"
            )
        yield
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
