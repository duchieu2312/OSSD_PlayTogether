from PyQt5.QtWidgets import QMainWindow, QStatusBar, QLineEdit, QPushButton, QWidget, QListWidget, QCheckBox, QListWidgetItem
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QIcon
import pytube
import webbrowser
import os

class YoutubeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube Downloader")
        self.resize(800, 600)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # Tạo giao diện
        self.init_ui()

    def init_ui(self):

        #
        self.centralwidget = QWidget(self)

        #
        self.Search = QLineEdit(self.centralwidget)
        self.Search.setGeometry(QRect(30, 30, 491, 20))
        self.Search.setPlaceholderText("Nhập tiêu đề video")

        #
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QRect(30, 60, 741, 481))


        self.SearchButton = QPushButton(self.centralwidget)
        self.SearchButton.setGeometry(QRect(530, 30, 91, 23))
        self.SearchButton.setText("Tìm kiếm")
        self.SearchButton.clicked.connect(self.search_videos)


        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QRect(630, 30, 120, 17))
        self.checkBox.setText("Tải về máy và xem")


        self.WatchButton = QPushButton(self.centralwidget)
        self.WatchButton.setGeometry(QRect(30, 550, 741, 23))
        self.WatchButton.setText("Xem")
        self.WatchButton.clicked.connect(self.watch_video)


        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
    def search_videos(self):
        search_term = self.Search.text()
        self.videos = []
        self.listWidget.clear()
        for video in pytube.Search(search_term).results:
            title = video.title
            views = f"{video.views:,}"
            publish_date = video.publish_date.strftime("%Y-%m-%d")
            item = QListWidgetItem(f"{title} - {views} người xem - {publish_date}")
            self.listWidget.addItem(item)
            self.videos.append(video)


    def watch_video(self):
        selected_item = self.listWidget.selectedItems()
        if not selected_item:
            self.statusbar.showMessage("Please select a video")
            return
        selected_video_index = self.listWidget.currentRow()
        video = self.videos[selected_video_index]
        if self.checkBox.isChecked():
            try:
                downloaded_file = video.streams.first().download()
                if os.name == "nt":
                    try:
                        os.startfile(downloaded_file)
                        self.statusbar.showMessage("Video downloaded and opened")
                    except Exception as e:
                        print(f"Error opening video in Windows Media Player: {e}")
                        self.statusbar.showMessage("Error opening video")
                else:
                    self.statusbar.showMessage("Windows Media Player integration not available on this system.")
            except Exception as e:
                print(f"Error downloading video: {e}")
                self.statusbar.showMessage("Error downloading video")
        else:
            webbrowser.open(video.watch_url, new=0, autoraise=True)