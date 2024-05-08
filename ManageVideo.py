from PyQt5.QtWidgets import QMainWindow, QHeaderView, QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
import subprocess

class MP4AndFoldersProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        file_name = self.sourceModel().fileName(source_index)
        if file_name.endswith(".mp4") or self.sourceModel().isDir(source_index):
            return super().filterAcceptsRow(source_row, source_parent)  # Hiển thị các tệp MP4 và thư mục
        else:
            return False


class ManageVideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Video Downloader")
        self.resize(800, 600)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # Tạo giao diện
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Lấy đường dẫn thư mục của tệp Python hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Tạo một mô hình hệ thống tệp với đường dẫn thư mục của tệp Python làm gốc
        self.model = QFileSystemModel()
        self.model.setRootPath(current_dir)

        # Tạo một mô hình proxy để lọc các loại tệp
        self.proxy_model = MP4AndFoldersProxyModel()
        self.proxy_model.setSourceModel(self.model)

        # Tạo một cây nhìn
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.setRootIndex(self.proxy_model.mapFromSource(self.model.index(current_dir)))
        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)

        layout.addWidget(self.tree_view)
        
        # Đặt chiều rộng cố định cho mỗi cột
        header = self.tree_view.header()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Cột đầu tiên

        # Đặt chiều rộng cho các cột khác ở đây nếu cần
        header.resizeSection(0, 500)  # Đặt chiều rộng cho cột đầu tiên

        # Mở rộng thư mục
        self.tree_view.expanded.connect(self.expand_folder)

        # Nút thêm thư mục mới
        self.new_folder_button = QPushButton("New Folder")
        self.new_folder_button.clicked.connect(self.create_new_folder_dialog)
        layout.addWidget(self.new_folder_button)

        # Nút di chuyển file
        self.move_file_button = QPushButton("Move File")
        self.move_file_button.clicked.connect(self.move_file_dialog)
        layout.addWidget(self.move_file_button)

        # Mở file mp4
        self.tree_view.doubleClicked.connect(self.open_file)


    def expand_folder(self, index):
        # Mở rộng tất cả các mục con của thư mục đã mở rộng
        self.tree_view.setExpanded(index, True)

    def create_new_folder_dialog(self):
        folder_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
        if ok:
            current_dir = os.getcwd()
            new_folder_path = os.path.join(current_dir, folder_name)
            try:
                os.mkdir(new_folder_path)
                self.model.setRootPath(current_dir)  # Cập nhật mô hình để làm mới cây nhìn
            except OSError as e:
                QMessageBox.warning(self, "Error", str(e))

    def move_file_dialog(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            source_index = self.proxy_model.mapToSource(index)
            file_path = self.model.filePath(source_index)
            file_name = os.path.basename(file_path)
            destination_folder, ok = QInputDialog.getText(self, 'Move File', f'Move "{file_name}" to folder:')
            if ok:
                destination_path = os.path.join(self.model.rootPath(), destination_folder)
                try:
                    os.rename(file_path, os.path.join(destination_path, file_name))
                    self.model.setRootPath(self.model.rootPath())  # Cập nhật mô hình để làm mới cây nhìn
                except OSError as e:
                    QMessageBox.warning(self, "Error", str(e))


    def open_file(self, index):
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.model.filePath(source_index)
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.mp3', '.mp4', '.avi', '.mkv', '.flv']:
            try:
                if sys.platform.startswith('win'):
                    os.startfile(file_path)
                elif sys.platform.startswith('linux'):
                    subprocess.Popen(['xdg-open', file_path])
                elif sys.platform.startswith('darwin'):
                    subprocess.Popen(['open', file_path])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Unable to open file: {str(e)}")
        else:
            QMessageBox.information(self, "Info", "File type not supported.")