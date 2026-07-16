

import re
import time
import threading

import webview

try:
    import serial
except ImportError:
    serial = None  



SERVER_URL = "http://127.0.0.1:8000/desktop-login/"

WINDOW_TITLE = "PosPlatform — Kassir"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800


SCALE_ENABLED = True
SCALE_PORT = "COM3"     
SCALE_BAUDRATE = 9600     




class ScaleReader:
 

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.latest_weight = 0.0
        self.connected = False
        self._stop = False

    def start(self):
        if serial is None:
            print("[Tarozi] pyserial o'rnatilmagan — 'pip install pyserial' bajaring.")
            return
        thread = threading.Thread(target=self._read_loop, daemon=True)
        thread.start()

    def stop(self):
        self._stop = True

    def _read_loop(self):
        while not self._stop:
            try:
                with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                    self.connected = True
                    print(f"[Tarozi] {self.port} portiga ulandi.")
                    while not self._stop:
                        raw = ser.readline()
                        line = raw.decode(errors="ignore").strip()
                        if not line:
                            continue
                        weight = self._parse_line(line)
                        if weight is not None:
                            self.latest_weight = weight
            except Exception as e:
                if self.connected:
                    print(f"[Tarozi] Ulanish uzildi: {e}")
                self.connected = False
                time.sleep(2)

    def _parse_line(self, line):
      
        m = re.search(r'([+-]?\d+\.\d+)\s*kg', line, re.IGNORECASE)
        if m:
            return float(m.group(1))

        if re.fullmatch(r'\d+', line):
            return int(line) / 1000

        return None


scale_reader = ScaleReader(SCALE_PORT, SCALE_BAUDRATE)


class Api:
    def get_scale_weight(self):
        return {
            "weight_kg": round(scale_reader.latest_weight, 3),
            "connected": scale_reader.connected,
        }


def main():
    if SCALE_ENABLED:
        scale_reader.start()

    window = webview.create_window(
        title=WINDOW_TITLE,
        url=SERVER_URL,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(1000, 650),
        confirm_close=True,
        text_select=False,
        js_api=Api(),
    )
    webview.start()


if __name__ == "__main__":
    main()