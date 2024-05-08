from PyQt5 import QtCore, QtGui, QtWidgets
from SpotifyDownloader import SpotifyWindow
from YoutubeDownloader import YoutubeWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlayTogether")
        self.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.init_ui()

    def init_ui(self):

        # Khung
        self.centralwidget = QtWidgets.QWidget(self)

        # Nút chuyển sang giao diện Youtube Downloader
        self.YoutubeButton = QtWidgets.QPushButton(self.centralwidget)
        self.YoutubeButton.setGeometry(QtCore.QRect(30, 60, 261, 430))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.YoutubeButton.setFont(font)
        self.YoutubeButton.setStyleSheet("border-image: url(images/Youtube.png); padding-top: 250px; border-radius: 10px;")
        self.YoutubeButton.clicked.connect(self.open_youtubedownloader)

        # Nút chuyển sang giao diện Spotify Downloader
        self.SpotifyButton = QtWidgets.QPushButton(self.centralwidget)
        self.SpotifyButton.setGeometry(QtCore.QRect(510, 60, 261, 430))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.SpotifyButton.setFont(font)
        self.SpotifyButton.setStyleSheet("border-image: url(images/Spotify.png); padding-top: 250px; border-radius: 10px;")
        self.SpotifyButton.clicked.connect(self.open_spotifydownloader)

        # Tiêu đề
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(250, 0, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.Title.setFont(font)
        self.Title.setText("PlayTogether")
        self.Title.setWordWrap(False)

        # Giới thiệu
        self.MadeByLabel = QtWidgets.QLabel(self.centralwidget)
        self.MadeByLabel.setGeometry(QtCore.QRect(10, 510, 251, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MadeByLabel.setFont(font)
        self.MadeByLabel.setText("Made by:\n"
"Nguyễn Đức Hiếu - 3120560028\n"
"Lê Nguyễn Đăng Khôi - 3120410252\n"
"Đào Ngọc Linh - 3120410277\n"
"Nguyễn Trương Tấn Lộc - 3120410293")
        
        # Ảnh nền
        self.Photo = QtWidgets.QLabel(self.centralwidget)
        self.Photo.setGeometry(QtCore.QRect(-4, -8, 811, 611))
        self.Photo.setText("")
        self.Photo.setPixmap(QtGui.QPixmap("images/bg.png"))
        self.Photo.setScaledContents(True)

        # Thông tin
        self.Desc = QtWidgets.QLabel(self.centralwidget)
        self.Desc.setGeometry(QtCore.QRect(300, 110, 201, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Desc.setFont(font)
        self.Desc.setText("<html><head/><body><p>Choose your downloader</p></body></html>")
        self.Desc.setAlignment(QtCore.Qt.AlignCenter)

        self.Photo.raise_()
        self.YoutubeButton.raise_()
        self.SpotifyButton.raise_()
        self.Title.raise_()
        self.MadeByLabel.raise_()
        self.Desc.raise_()

        self.setCentralWidget(self.centralwidget)

    def open_youtubedownloader(self):
        self.hide()
        self.youtube_window = YoutubeWindow()
        self.youtube_window.show()

    def open_spotifydownloader(self):
        self.hide()
        self.spotify_window = SpotifyWindow()
        self.spotify_window.load_songs("XXXTentacion")
        self.spotify_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())