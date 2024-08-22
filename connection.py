import sys
import time
from pymavlink import mavutil
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QApplication

from PyQt5.QtCore import QThread, pyqtSignal

class GCSData(QMainWindow):
    def __init__(self, ip, port):
        super().__init__()
        self.connection_string = f"tcp:{ip}:{port}"  # Construct the connection string here
        self.setUI()

        # Initialize the MavData thread
        self.mav_thread = MavData(ip, port)
        self.mav_thread.data_received.connect(self.update_labels)
        self.mav_thread.start()


    def setUI(self):
        self.setWindowTitle("GCS-Data")
        self.resize(500,400)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # adding labels
        self.airLabel = QLabel(self)
        self.airLabel.setGeometry(50, 10, 200, 150)
        # self.airLabel.setText(str(self.))
        self.groundLabel = QLabel(self)
        self.groundLabel.setGeometry(50, 70, 300, 150)

        self.yawLabel = QLabel(self)
        self.yawLabel.setGeometry(50, 130, 200, 180)
        
        self.headLabel = QLabel(self)
        self.headLabel.setGeometry(50, 170, 300, 180)

    def update_labels(self, data):
        airspeed = round(data.get('airspeed', 0), 2)
        groundspeed = round(data.get('groundspeed', 0), 2)
        yaw = round(data.get('yaw', 0), 2)
        heading = round(data.get('heading', 0), 2)

        self.airLabel.setText(f"Airspeed: {airspeed * 3.6}")
        self.groundLabel.setText(f"Groundspeed: {groundspeed}")
        self.yawLabel.setText(f"Yaw: {yaw}")
        self.headLabel.setText(f"Heading: {heading}")
        print(airspeed, groundspeed, yaw, heading)

    def closeEvent(self, event):
        # Stop the thread when the window is closed
        self.mav_thread.stop()
        self.mav_thread.wait()
        event.accept()


class MavData(QThread):
    data_received = pyqtSignal(dict)

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connection_string = f"tcp:{self.ip}:{self.port}"
        self.running = True

    def run(self):
        master = mavutil.mavlink_connection(self.connection_string)
        while self.running:
            try:
                message = master.recv_match()
                if message is not None:
                    message = message.to_dict()
                    if message.get('mavpackettype') == 'VFR_HUD':
                        self.data_received.emit(message)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.1)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GCSData('127.0.0.1', '14550')
    window.show()
    sys.exit(app.exec_())
