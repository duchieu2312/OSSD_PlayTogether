from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from pytube import YouTube
from ManageVideo import ManageVideoWindow

class YoutubeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.resize(800, 600)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # Tạo giao diện
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Thêm widget cho các nút và thanh URL
        toolbar_layout = QHBoxLayout()

        # Thêm nút "Previous"
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_page)
        toolbar_layout.addWidget(self.previous_button)

        # Thêm nút "Next"
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        toolbar_layout.addWidget(self.next_button)

        # Thêm thanh hiện URL
        self.url_edit = QLineEdit()
        self.url_edit.setReadOnly(True)  # Đặt chỉ đọc để ngăn người dùng chỉnh sửa URL
        toolbar_layout.addWidget(self.url_edit)

        # Thêm widget của thanh công cụ vào layout chính
        self.layout.addLayout(toolbar_layout)

        # Thêm trình duyệt web
        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        # Truy cập trực tiếp vào trang chủ YouTube
        self.webview.setUrl(QUrl("https://www.youtube.com"))
        self.webview.urlChanged.connect(self.update_url)
        
        # Thêm nút tải Video
        self.download_button = QPushButton("Download Video")
        self.download_button.clicked.connect(self.download_current_video)
        self.layout.addWidget(self.download_button)
        
        # Thêm nút quản lý Video
        self.manage_button = QPushButton("Manage Videos")
        self.manage_button.clicked.connect(self.open_manage)
        self.layout.addWidget(self.manage_button)
        
    def load_url(self, url):
        self.webview.load(QUrl(url))
    
    def previous_page(self):
        self.webview.back()

    def next_page(self):
        self.webview.forward()
    
    def update_url(self, url):
        # Cập nhật thanh URL khi URL trang web thay đổi
        self.url_edit.setText(url.toString())        

    def download_current_video(self):
        # Lấy địa chỉ website hiện tại
        current_url = self.webview.url()
        if current_url.isEmpty() or "watch?" not in current_url.toString():
            QMessageBox.warning(self, "Warning", "No video selected!")
            return
        video_url = current_url.toString()

        try:
            # Tìm các luồng tải xuống của video
            yt = YouTube(video_url)
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            
            # Trích xuất độ phân giải của từng luồng
            resolutions = [f"{stream.resolution}" for stream in streams if stream.resolution is not None]

            # Hiển thị hộp thoại lựa chọn độ phân giải
            resolution, ok = QInputDialog.getItem(self, "Select Resolution", "Choose resolution:", resolutions, 0, False)
            if not ok: return

            # Tìm luồng đã chọn
            selected_stream = next(stream for stream in streams if  f"{stream.resolution}" == resolution)
            
            # Chọn vị trí thư mục tải xuống
            download_dir = QFileDialog.getExistingDirectory(self, "Selecte directory to save file")

            # Nếu người dùng đã chọn thư mục, thư mục sẽ được sử dụng để lưu trữ file
            if download_dir:
                # Tải về luồng đã chọn
                selected_stream.download(output_path=download_dir)
                QMessageBox.information(self, "Success", "Video downloaded successfully!")
            else:
                # Người dùng không chọn thư mục, không thực hiện tải về
                QMessageBox.warning(self, "Warning", "You haven't selected a download directory!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download video: {str(e)}")

    def open_manage(self):
        self.manage_window = ManageVideoWindow()
        self.manage_window.show()

    def closeEvent(self, event):
        self.webview.load(QUrl("youtube.com"))
        self.close()