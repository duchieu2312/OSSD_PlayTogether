from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QDir, QTime
from PyQt5.QtGui import QIcon

class VideoPlayer(QWidget):
    def __init__(self, file_path=None):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.resize(800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        layout = QVBoxLayout()
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setFixedHeight(10)
        self.currentTimeLabel.setFixedWidth(100)
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setFixedHeight(10)
        self.totalTimeLabel.setFixedWidth(100)
        # Kết nối sự kiện positionChanged của mediaPlayer với một phương thức mới để cập nhật thời gian
        self.mediaPlayer.positionChanged.connect(self.update_time)

 # Tạo một QLabel mới
        self.soundLabel = QLabel("Sound")
        self.soundLabel.setFixedHeight(10)
        self.soundLabel.setFixedWidth(100)  
        # Thêm thanh trượt âm lượng vào layout
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.sliderMoved.connect(self.set_volume)
        layout.addWidget(self.volumeSlider)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        

        layout = QVBoxLayout()
        layout.addWidget(videowidget)
        layout.addWidget(openBtn)
        layout.addWidget(self.playBtn)
        layout.addWidget(self.currentTimeLabel)
        layout.addWidget(self.slider)
        layout.addWidget(self.totalTimeLabel)
        layout.addWidget(self.soundLabel)
        layout.addWidget(self.volumeSlider)  # Thêm thanh chỉnh âm lượng vào layout
        layout.addWidget(self.label)

        self.setLayout(layout)
        if file_path is not None:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()  # Thêm dòng này để tự động phát


    def open_file(self):
        current_dir = QDir.currentPath()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", current_dir, "Video Files (*.mp4 *.mp3);;All Files (*)")

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
    def closeEvent(self, event):
        self.mediaPlayer.stop()
        event.accept()     
        
    def update_time(self, position):
        # Cập nhật thời gian hiện tại
        self.currentTimeLabel.setText(QTime(0, 0).addMSecs(position).toString())

        # Cập nhật tổng thời lượng
        duration = self.mediaPlayer.duration()
        if duration >= 0:
            self.totalTimeLabel.setText(QTime(0, 0).addMSecs(duration).toString())           

if __name__ == "__main__":
    app = QApplication([])
    player = VideoPlayer()
    player.show()
    app.exec_()