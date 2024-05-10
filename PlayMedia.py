from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QStyle, QSizePolicy, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QDir, QTime
from PyQt5.QtGui import QIcon, QPixmap
import os

class VideoPlayer(QWidget):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.resize(800, 600)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.showMaximized()
        
        

        # Tạo giao diện
        self.init_ui(file_path)

    def init_ui(self,file_path):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.setFixedWidth(50)
        self.playBtn.clicked.connect(self.play_video)
        
        
        self.volumeLabel = QLabel("Volume:")
        self.volumeLabel.setFixedWidth(55)


        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setFixedWidth(150)

        self.volumeSlider.sliderMoved.connect(self.set_volume)

        ButtonsLayout = QHBoxLayout()
        ButtonsLayout.addWidget(self.playBtn)
        ButtonsLayout.addWidget(self.volumeLabel)
        ButtonsLayout.addWidget(self.volumeSlider)
        ButtonsLayout.setAlignment(Qt.AlignCenter)

        self.currentTimeLabel = QLabel()
        self.spaceLabel = QLabel("/")
        self.totalTimeLabel = QLabel()


        TimeLayout = QHBoxLayout()
        TimeLayout.addWidget(self.currentTimeLabel)
        TimeLayout.addWidget(self.spaceLabel)
        TimeLayout.addWidget(self.totalTimeLabel)
        TimeLayout.setAlignment(Qt.AlignLeft)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)


        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        # Kết nối sự kiện positionChanged của mediaPlayer với một phương thức mới để cập nhật thời gian
        self.mediaPlayer.positionChanged.connect(self.update_time)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(videowidget)
        MainLayout.addLayout(TimeLayout)
        MainLayout.addWidget(self.slider)
        MainLayout.addLayout(ButtonsLayout)
        MainLayout.addWidget(self.openBtn)
        MainLayout.addWidget(self.label)

        self.setLayout(MainLayout)
        if file_path is not None:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()  # Thêm dòng này để tự động phát


    def open_file(self):
        current_dir = QDir.currentPath()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", current_dir, "Video Files (*.mp4);;All Files (*)")

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()  # Thêm dòng này để tự động phát


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
        
    def update_time(self, position):
        # Cập nhật thời gian hiện tại
        self.currentTimeLabel.setText(QTime(0, 0).addMSecs(position).toString())

        # Cập nhật tổng thời lượng
        duration = self.mediaPlayer.duration()
        if duration >= 0:
            self.totalTimeLabel.setText(QTime(0, 0).addMSecs(duration).toString())   

    def closeEvent(self, event):
        self.mediaPlayer.stop()
        event.accept()     

class MusicPlayer(QWidget):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.resize(300, 200)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        

        # Tạo giao diện
        self.init_ui(file_path)

    def init_ui(self,file_path):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)

        filename = os.path.basename(file_path)
        self.nameLabel = QLabel()
        self.nameLabel.setText(filename)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playBtn.setFixedWidth(50)
        self.playBtn.clicked.connect(self.play_music)
        
        self.volumeLabel = QLabel("Volume:")
        self.volumeLabel.setFixedWidth(55)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setFixedWidth(150)
        self.volumeSlider.sliderMoved.connect(self.set_volume)

        ButtonsLayout = QHBoxLayout()
        ButtonsLayout.addWidget(self.playBtn)
        ButtonsLayout.addWidget(self.volumeLabel)
        ButtonsLayout.addWidget(self.volumeSlider)
        ButtonsLayout.setAlignment(Qt.AlignCenter)

        self.currentTimeLabel = QLabel()
        self.spaceLabel = QLabel("/")
        self.totalTimeLabel = QLabel()

        TimeLayout = QHBoxLayout()
        TimeLayout.addWidget(self.currentTimeLabel)
        TimeLayout.addWidget(self.spaceLabel)
        TimeLayout.addWidget(self.totalTimeLabel)
        TimeLayout.setAlignment(Qt.AlignLeft)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        self.openBtn = QPushButton('Open Music')
        self.openBtn.clicked.connect(self.open_file)

        # Kết nối sự kiện positionChanged của mediaPlayer với một phương thức mới để cập nhật thời gian
        self.mediaPlayer.positionChanged.connect(self.update_time)

        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.nameLabel)
        MainLayout.addLayout(TimeLayout)
        MainLayout.addWidget(self.slider)
        MainLayout.addLayout(ButtonsLayout)
        MainLayout.addWidget(self.openBtn)

        self.setLayout(MainLayout)
        if file_path is not None:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()  # Thêm dòng này để tự động phát


    def open_file(self):
        current_dir = QDir.currentPath()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Music", current_dir, "Music Files (*.mp3);;All Files (*)")

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()  # Thêm dòng này để tự động phát


    def play_music(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
        
    def update_time(self, position):
        # Cập nhật thời gian hiện tại
        self.currentTimeLabel.setText(QTime(0, 0).addMSecs(position).toString())

        # Cập nhật tổng thời lượng
        duration = self.mediaPlayer.duration()
        if duration >= 0:
            self.totalTimeLabel.setText(QTime(0, 0).addMSecs(duration).toString())   

    def closeEvent(self, event):
        self.mediaPlayer.stop()
        event.accept()