
import os
import pytesseract
import pyscreenshot
from PySide6.QtGui import (
    QImage,
    QMouseEvent, 
    QPixmap, 
    Qt, 
    QPainter, 
    QColor, 
    QPen) 

from PySide6.QtCore import Qt, QRect, QPoint, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTextEdit,
)

path = os.path.join(os.path.dirname(__file__), "image.png")


class SnipeTool(QWidget):

    region = Signal(QRect)

    def __init__(self):
        super().__init__()

        self.start = QPoint()
        self.end = QPoint()
        self.snipping = None
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.showFullScreen()
    
    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.LeftButton):
            self.start = event.position().toPoint()
            self.end = self.start
            self.snipping = True    
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.snipping:
            self.end = event.position().toPoint()
            self.update()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.snipping = False

            rect = QRect(self.start, self.end).normalized()
            self.region.emit(rect)
            self.close()
            
    
    def paintEvent(self, event):
        painter = QPainter(self)

        # Oscurecer pantalla
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        if self.snipping:
            rect = QRect(self.start, self.end)
            # Borde
            painter.setPen(QPen(QColor(0, 255, 0), 2))

            # Relleno semitransparente
            painter.setBrush(QColor(0, 255, 0, 50))

            painter.drawRect(rect)



class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR App")

        self.imageLabel = QLabel("This label will show the screenshot when you click the button.")
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.coords = None

        regionButon = QPushButton("Draw Region")
        screenshootButton = QPushButton("Screenshoot")
        ocrButton = QPushButton("Perform OCR")

        self.textBox = QTextEdit()
        
        screenshootButton.clicked.connect(self.screenshoot)
        ocrButton.clicked.connect(self.perform_ocr)
        regionButon.clicked.connect(self.draw_region)
        mainLayout = QVBoxLayout()
        buttons = QHBoxLayout()
        mainLayout.addWidget(self.imageLabel)
        mainLayout.addWidget(self.textBox)
        buttons.addWidget(regionButon)
        buttons.addWidget(screenshootButton)
        buttons.addWidget(ocrButton)
        mainLayout.addLayout(buttons)
        
        container = QWidget()
        container.setLayout(mainLayout)

        self.setCentralWidget(container)
    
    def screenshoot(self):
        if self.area == None:
            print("Please define a region first.")
            return
        image = pyscreenshot.grab(bbox = self.coords)
        image.save(path)   # type: ignore

        pixmap = QPixmap(path)
        self.imageLabel.setPixmap(pixmap)
        print("Screenshoot saved to {}".format(path))
        
        test = self.snipeTool.snipping
        print(test)

    def perform_ocr(self):
        result = pytesseract.image_to_string(path, lang='jpn')
        print("OCR Result:")
        print(result)
        self.textBox.setPlainText(result)

    def draw_region(self):
        self.snipeTool = SnipeTool()
        self.snipeTool.region.connect(self.set_region)
        print(self.snipeTool.region)
        self.area = self.snipeTool.region
        print("Region defined: {}".format(self.area))

    def set_region(self, rect):
        self.area = rect
        self.coords = (rect.left(), rect.top(), rect.right(), rect.bottom())
        print("Region set to: {}".format(self.area))


app = QApplication([])
window = MainWindow()   
window.show()
app.exec()