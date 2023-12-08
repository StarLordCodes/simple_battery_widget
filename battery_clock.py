import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint
import psutil  # For battery information
from datetime import datetime


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.dragPosition = QPoint()

    def initUI(self):
        # Set window flags to remove title bar and buttons
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create labels for battery and clock
        self.battery_label = QLabel("Battery Percentage: -")
        self.clock_label = QLabel("Current Time: -")

        # Create a layout to organize the labels
        layout = QVBoxLayout()
        layout.addWidget(self.battery_label)
        layout.addWidget(self.clock_label)

        # Set the layout for the window
        self.setLayout(layout)

        # Update battery percentage and clock every second
        self.update_display()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_display(self):
        # Update battery percentage
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Plugged in" if battery.power_plugged else "Not plugged in"
            percent = f"Battery Percentage: {battery.percent}% ({plugged})"
            self.battery_label.setText(percent)

        # Update current time
        now = datetime.now()
        current_time = now.strftime("Current Time: %H:%M:%S")
        self.clock_label.setText(current_time)

    # Implement mouse events for window dragging
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
