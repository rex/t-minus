#!/usr/bin/env python3
"""T-MINUS server: serves the app + /say endpoint -> native macOS `say` (system default voice).

While this server is up, the com.pierce.time-announcer LaunchAgent is disabled so the two
clocks never talk over each other; it is re-enabled when the server exits. If it was already
disabled before launch, it is left exactly as found.
"""
import atexit, os, queue, signal, subprocess, sys, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 4173
q = queue.Queue()

def worker():
    while True:
        text, rate = q.get()
        try:
            cmd = ['say']
            if rate:
                cmd += ['-r', str(int(rate))]
            cmd.append(text)
            subprocess.run(cmd, timeout=120)
        except Exception:
            pass

threading.Thread(target=worker, daemon=True).start()

ANNOUNCER = 'com.pierce.time-announcer'
GUI = f'gui/{os.getuid()}'
_restore_announcer = False

def _announcer_disabled():
    """True / False, or None when launchctl can't tell us."""
    try:
        r = subprocess.run(['launchctl', 'print-disabled', GUI],
                           capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        if ANNOUNCER in line:
            v = line.split('=>')[-1].strip().lower()
            return v.startswith('true') or v.startswith('disabled')
    return False

def pause_announcer():
    global _restore_announcer
    was = _announcer_disabled()
    if was is None:
        print('· time-announcer: state unknown — left alone')
        return
    if was:
        print('· time-announcer: already disabled — left alone')
        return
    try:
        ok = subprocess.run(['launchctl', 'disable', f'{GUI}/{ANNOUNCER}'],
                            capture_output=True, timeout=10).returncode == 0
    except Exception:
        ok = False
    _restore_announcer = ok
    print('· time-announcer: PAUSED for this session' if ok
          else '· time-announcer: COULD NOT PAUSE — expect double clocks')

def resume_announcer():
    global _restore_announcer
    if not _restore_announcer:
        return
    _restore_announcer = False
    try:
        ok = subprocess.run(['launchctl', 'enable', f'{GUI}/{ANNOUNCER}'],
                            capture_output=True, timeout=10).returncode == 0
    except Exception:
        ok = False
    print('\n· time-announcer: RESUMED' if ok else
          f'\n· time-announcer: FAILED to resume — run: launchctl enable {GUI}/{ANNOUNCER}')

atexit.register(resume_announcer)
for _sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
    signal.signal(_sig, lambda *_: sys.exit(0))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == '/say':
            qs = parse_qs(u.query)
            text = (qs.get('text') or [''])[0][:500]
            rate = (qs.get('rate') or [None])[0]
            if text.strip():
                q.put((text, rate))
            self.send_response(204)
            self.end_headers()
            return
        if u.path == '/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"say":true}')
            return
        return super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *args):
        pass

pause_announcer()
print(f'T-MINUS · http://localhost:{PORT} · native say voice ONLINE')
try:
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
except KeyboardInterrupt:
    pass
