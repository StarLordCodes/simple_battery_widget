import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
import psutil  # For battery information
from datetime import datetime
from PyQt5.QtGui import QFont


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.dragPosition = QPoint()
        self.edit_mode = False  # Flag to track edit mode

        # this showed wrong window size because initialisation size is not the size we see
        # self.original_size = self.size()
        # print(self.original_size)

    def initUI(self):
        # Set window flags to remove title bar and buttons
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create labels for battery and clock
        self.battery_label = QLabel("Battery: -")
        self.clock_label = QLabel(" Time: -")
        self.text_field = QLineEdit()  # New text field
        self.text_field.setHidden(True)  # Initially hide the text field
        self.display_field = QLabel("Note: -")

        # Set font properties for labels
        # font = QFont("Fira Code", 14, QFont.Bold)
        font = QFont()
        font.setPointSize(10)
        self.battery_label.setFont(font)
        self.clock_label.setFont(font)
        self.display_field.setFont(font)

        # Create a layout to organize the labels
        layout = QVBoxLayout()
        layout.addWidget(self.battery_label)
        layout.addWidget(self.clock_label)
        layout.addWidget(self.text_field)
        layout.addWidget(self.display_field)

        # Set the layout for the window
        self.setLayout(layout)

        # Update battery percentage and clock every minute
        self.update_display()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 second)

        self.show()  # this will trigger showEvent() which will show actual window size

    def update_display(self):
        # Update battery percentage
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Plugged" if battery.power_plugged else "Unplugged"
            percent = f" {battery.percent}% ({plugged}) "
            self.battery_label.setText(percent)

        # Update current time
        now = datetime.now()
        current_time = now.strftime("Time: %H:%M")
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

    # Handle key press events
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.toggle_text_field()
        if event.key() == Qt.Key_Escape:
            self.close()

    # switch between edit and display modes
    def toggle_text_field(self):
        if self.edit_mode:
            self.edit_mode = False
            text = self.text_field.text()
            self.text_field.setHidden(True)
            self.display_field.setText(text)
            self.display_field.setHidden(False)
            self.resize(
                max(self.original_size.width(), len(text) + 10),
                self.original_size.height(),
            )
        else:
            self.edit_mode = True
            self.text_field.setText(self.display_field.text())
            self.display_field.setHidden(True)
            self.text_field.setHidden(False)
            self.text_field.setFocus()

    def showEvent(self, event):
        # shows real size of window after it appears on screen
        self.original_size = self.size()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
