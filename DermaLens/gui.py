import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton,
    QMainWindow, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar,
    QFileDialog
)
from PyQt5 import QtWidgets, QtGui

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from results import Get_Result


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dermalens - Ana Sayfa')
        self.setGeometry(200, 200, 440, 500)
        
        self.widget = QWidget()
        layout = QVBoxLayout()
        
        self.model_handler = Get_Result()
        self.model_handler.model_load()
        
        palette = self.widget.palette()
        palette.setColor(self.widget.backgroundRole(), QtGui.QColor("#1e1e2f"))  # koyu arka plan
        palette.setColor(self.widget.foregroundRole(), QtGui.QColor("#ffffff"))  # yazılar beyaz
        self.widget.setPalette(palette)
        
        self.file_path = '...'
        self.stat = '...'
        self.stat_loading = 'in progress'
        self.result_dermalens = 'scanning'
        self.range_of_row = -1


        bar = QMenuBar(self.widget)
        file_menu = bar.addMenu('File')
        file_menu.addAction(QAction('File', self))
        file_menu.addAction(QAction('Result', self))
        file_menu.addAction(QAction('Info', self))

        layout.addWidget(bar)


        self.model = QStandardItemModel()
        self.model.setRowCount(9)
        self.model.setColumnCount(3)
        

        table_view = QTableView()
        table_view.setModel(self.model)
        layout.addWidget(table_view)


        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)
        
        self.stop_button = QPushButton("Stop", self)
        
        layout.addWidget(self.stop_button)


        self.file_label = QLabel(f"Seçilen Dosya: {self.file_path}", self)
        layout.addWidget(self.file_label)

        self.reload_table("...")

        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        
        if hasattr(self, 'data_loader') and self.data_loader.isRunning():
            self.data_loader.stop() 
        event.accept()
        
    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        
        if self.file_path:
            self.range_of_row += 1
            self.file_label.setText(f"Seçilen Dosya: {self.file_path}")
            self.reload_table(self.result_dermalens)
            
            self.start_data_loader()

    def start_data_loader(self):
        self.file_path = self.file_path.replace("/", "//")
        self.data_loader = GetResultDeepface(self.file_path,self.model_handler)
        self.data_loader.signal.connect(self.reload_table)
        self.data_loader.start()
        self.stop_button.clicked.connect(self.stop_button_using)
    
    def stop_button_using(self):
        self.data_loader.stop()
        self.reload_table('stopped')
    
    def reload_table(self, result_dermalens):
        if self.range_of_row == 9:
            for row in range(9):
                for column in range(3):
                    item = QStandardItem("")
                    self.model.setItem(row, column, item)
            self.range_of_row = 0
        

        item = QStandardItem(f'{os.path.basename(self.file_path)}')
        status_item = QStandardItem(self.stat)
        status_loading = QStandardItem(self.stat_loading)

        if "akiec" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "bcc" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "bkl" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "df" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "mel" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "nv" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "vasc" in result_dermalens.lower():
            self.stat = result_dermalens
        elif "stopped" in result_dermalens.lower():
            self.stat = 'Stopped'
            
        status_item = QStandardItem(self.stat)
        status_loading = QStandardItem(self.stat_loading)
        self.model.setItem(self.range_of_row, 0, item)
        self.model.setItem(self.range_of_row, 1, status_loading)
        self.model.setItem(self.range_of_row, 2, status_item)
        self.stat = 'scanning...'
        self.stat_loading = 'in progress'


class GetResultDeepface(QThread):
    signal = pyqtSignal(str)

    def __init__(self, path, model_handler):
        super().__init__()
        self.path = path
        self.model_handler = model_handler
        self.running = True

    def run(self):
        try:
            if self.running:
                result = self.model_handler.get_image_pre(self.path)
                #result = Get_Result().get_image_pre(self.path)
                self.signal.emit(str(result))
        except Exception as e:
            self.signal.emit(f"Hata: {str(e)}")

    def stop(self):
        self.running = False
        self.terminate()
        self.wait()
def paint(app):
    app.setStyleSheet("""
    /* --- Butonlar --- */
    QPushButton {
        background-color: #2a2c40;
        color: #ffffff;
        border: 1px solid #444444;
        padding: 5px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #3d3f5c;
    }
    QPushButton:pressed {
        background-color: #1e1e2f;
    }

    /* --- Tablo --- */
    QTableView {
        background-color: #1e1e2f;
        color: #ffffff;
        gridline-color: #444444;
        selection-background-color: #2a2a40;
        selection-color: #ffffff;
    }
    QHeaderView::section {
        background-color: #2a2c40;
        color: #ffffff;
        border: 1px solid #444444;
        padding: 4px;
    }

    /* --- ScrollBar --- */
    QScrollBar:vertical {
        background: #1e1e2f;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #444444;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #5a5a5a;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }

    QScrollBar:horizontal {
        background: #1e1e2f;
        height: 12px;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background: #444444;
        min-width: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #5a5a5a;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;
        width: 0px;
    }

    /* --- QFileDialog ve Input Alanları --- */
    QFileDialog, QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #1e1e2f;
        color: #ffffff;
        border: 1px solid #444444;
    }

    QLabel {
        color: #ffffff;
    }

    QMenuBar {
        background-color: #2a2c40;
        color: #ffffff;
    }
    QMenuBar::item:selected {
        background: #444444;
    }

    QMenu {
        background-color: #2a2c40;
        color: #ffffff;
    }
    QMenu::item:selected {
        background-color: #444444;
    }
    /* --- Tablo Köşe Hücresi (sol üstteki minik kutucuk) --- */
    QTableCornerButton::section {
        background-color: #2a2c40;
        border: 1px solid #444444;
    }
    """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    paint(app)
    login_window = HomePage()
    login_window.show()
    sys.exit(app.exec_())