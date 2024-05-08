from PyQt5.QtWidgets import QFileDialog,QApplication,QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget,QSlider,QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QTime
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import webbrowser
import requests
from io import BytesIO
from ManageSong import ManageSongWindow

class SpotifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Song Downloader")
        self.resize(800, 600)
        icon = QIcon()
        icon.addPixmap(QPixmap("images/Logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # Khởi tạo Spotify client
        client_id = '98825532008844aaa042b6795fb1ab34'
        client_secret = '21b96ce2c8b94a60a8ccd9de42d563c7'
        self.spotify_client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify_client = spotipy.Spotify(client_credentials_manager=self.spotify_client_credentials_manager)
        self.is_repeating = False
        self.is_playing = False

        # Khởi tạo media player để phát nhạc
        self.media_player = QMediaPlayer()

        # Tạo giao diện
        self.init_ui()

    def init_ui(self):
        
        # Khung tìm kiếm
        self.search_label = QLabel("Tìm kiếm:")
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Enter song name....")
        self.search_entry.textChanged.connect(self.search_tracks)

        search_layout = QVBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_entry)

        search_widget = QWidget()
        search_widget.setLayout(search_layout)

        # Danh sách bài hát
        self.track_list_widget = QListWidget()
        self.track_list_widget.itemClicked.connect(self.play_selected_track)
        # self.track_list_widget.setStyleSheet("color: white;")

        # Thanh điều khiển nhạc và thời gian chạy nhạc
        self.horizontal_slider = QSlider(Qt.Horizontal)
        self.time_label_start = QLabel()
        self.time_label_end = QLabel()

        # Gộp Thanh điều khiển nhạc và thời gian chạy nhạc
        TimeAndHorizaltal = QHBoxLayout()
        TimeAndHorizaltal.addWidget(self.time_label_start)
        TimeAndHorizaltal.addWidget(self.horizontal_slider)
        TimeAndHorizaltal.addWidget(self.time_label_end)

        # Nút quản lý bài hát
        self.manage_button = QPushButton("Manage Songs")
        self.manage_button.clicked.connect(self.open_manage)

        # Nút chuyển bài trước
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_track)

        # Nút bấm phát và ngưng
        self.play_stop_button = QPushButton("Play")
        self.play_stop_button.clicked.connect(self.play_stop_track)

        # Nút chuyển bài sau
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_track)
        self.repeat_button = QPushButton("Repeat")

        # Tên bài hát và hình bài hát đang phát
        self.font = QFont()
        self.font.setPointSize(20)  # Đặt kích thước văn bản là 16
        self.DisplayNameMusic_Label = QLabel()
        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(200, 200)

        # Nút chuyển đến trang phát bài hát
        self.moveMusic = QPushButton("Go to music")
        self.moveMusic.hide()
        self.moveMusic.clicked.connect(self.go_to_music)

        # Nút tải bài hát về
        self.download_button = QPushButton()
        self.download_button.hide()
        self.download_button.clicked.connect(self.download_track)

        # Gộp tên bài hát, hình và nút tải về
        nameAndImage = QHBoxLayout()
        nameAndImage.addWidget(self.album_art_label)
        nameAndImage.addWidget(self.DisplayNameMusic_Label)
        nameAndImage.addWidget(self.moveMusic)
        nameAndImage.addWidget(self.download_button)

        # Gộp các button nhạc        
        buttons_music = QHBoxLayout()
        buttons_music.addWidget(self.manage_button)
        buttons_music.addWidget(self.previous_button)
        buttons_music.addWidget(self.play_stop_button)
        buttons_music.addWidget(self.next_button)
        buttons_music.addWidget(self.repeat_button)

        # Gộp khung tìm kiếm và danh sách bài hát vào cùng một layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widget)
        main_layout.addWidget(self.track_list_widget)
        main_layout.addLayout(TimeAndHorizaltal)
        main_layout.addLayout(nameAndImage)
        main_layout.addLayout(buttons_music)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        # central_widget.setStyleSheet("background-color: rgba(0,0,0, .5);")
        self.setCentralWidget(central_widget)
        self.media_player.positionChanged.connect(self.update_slider_position)
        self.horizontal_slider.sliderMoved.connect(self.set_media_player_position)
        self.horizontal_slider.sliderReleased.connect(self.check_slider_position)
        self.repeat_button.clicked.connect(self.repeat_music)


    def search_tracks(self):
        query = self.search_entry.text()
        if query:
            results = self.spotify_client.search(q=query, limit=30)
            self.track_list_widget.clear()  # Xóa danh sách bài hát cũ
            self.track_infos = [(track['name'], track['artists'][0]['name'], track['preview_url']) for track in results['tracks']['items']]
            for idx, track_info in enumerate(self.track_infos):
                track_name, artist_name, _ = track_info
                self.track_list_widget.addItem(f"{idx+1}. {track_name} - {artist_name}")
        else:                
            self.track_list_widget.clear()  # Xóa danh sách bài hát cũ
            self.load_songs("XXXTentacion")

    def play_stop_track(self):
        if self.is_playing:  # Nếu bài hát đang phát thì ngưng nó
            self.media_player.stop()
            self.set_media_player_position(self.media_player.position())  # Đặt vị trí thanh trượt về vị trí hiện tại
            self.play_stop_button.setText("Play")  # Đổi nút thành "Play"
            self.is_playing = False
        else:  # Nếu bài hát đang ngưng thì phát nó
            index = self.track_list_widget.currentRow() 
            self.is_playing = True
            track_name, artist_name, preview_url = self.track_infos[index]
            print(preview_url)
            if preview_url:
                self.play_audio_from_url(preview_url)
                self.DisplayNameMusic_Label.setText(f" {track_name} - {artist_name}")
                self.setImageMusic(track_name, artist_name)
                self.play_stop_button.setText("Stop")  # Đổi nút thành "Stop"
                self.is_playing = True
            else:
                QMessageBox.information(self, "Thông báo", "Bài hát không tồn tại.")

    def play_selected_track(self):
        index = self.track_list_widget.currentRow() 
        if index != -1:
            track_name, artist_name, preview_url = self.track_infos[index]
            # print(preview_url)
            if preview_url:
                self.play_audio_from_url(preview_url)
                self.DisplayNameMusic_Label.setText(f" {track_name} \n {artist_name}")
                self.DisplayNameMusic_Label.setFont(self.font)
                self.setImageMusic(track_name, artist_name)
                self.moveMusic.show()
                self.download_button.setText("Download")
                self.download_button.show()
                self.play_stop_button.setText("Stop")  # Đổi nút thành "Stop"
                self.is_playing = True
            else:
                QMessageBox.information(self, "Thông báo", "Bài hát không tồn tại.")

    def go_to_music(self):
        index = self.track_list_widget.currentRow()
        track_name, artist_name, _ = self.track_infos[index]
        track_url = self.get_track_url(track_name, artist_name)
        if track_url:
            webbrowser.open(track_url)
        else:
            QMessageBox.information(self, "Thông báo", "Không tìm thấy bài hát trên Spotify.")

    def play_audio_from_url(self, url):
        self.media_player.setMedia(QMediaContent(QUrl(url)))
        self.media_player.play()

    def load_songs(self, artist_name):
        results = self.spotify_client.search(q=artist_name, limit=30)
        self.track_infos = [(track['name'], track['artists'][0]['name'], track['preview_url']) for track in results['tracks']['items']]
        added_track_names = set()  # Tạo một set để lưu trữ các tên bài hát đã thêm vào danh sách
        for idx, track_info in enumerate(self.track_infos):
            track_name, artist_name, _ = track_info
            if track_name.split not in added_track_names:  # Kiểm tra xem tên bài hát đã tồn tại trong danh sách chưa
                self.track_list_widget.addItem(f"{idx+1}. {track_name} - {artist_name}")
                added_track_names.add(track_name)  # Thêm tên bài hát vào set

    def update_slider_position(self, position):
        # Cập nhật giá trị của horizontal_slider khi thời gian phát thay đổi
        current_position = self.media_player.position()

        # Lấy tổng thời lượng của bài hát
        total_duration = self.media_player.duration()

        # Chuyển đổi thời gian sang định dạng phút:giây
        current_time = QTime(0, 0, 0).addMSecs(current_position)
        total_time = QTime(0, 0, 0).addMSecs(total_duration)

        # Hiển thị thời gian trên label
        self.time_label_start.setText(current_time.toString("m:ss"))
        self.time_label_end.setText(total_time.toString("m:ss"))

        # Kiểm tra nếu tổng thời lượng khác 0 (tránh lỗi chia cho 0)
        if total_duration != 0:
            # Tính toán giá trị mới cho horizontal_slider dựa trên thời gian hiện tại và tổng thời lượng
            new_slider_value = int((current_position / total_duration) * self.horizontal_slider.maximum())
            self.horizontal_slider.setValue(new_slider_value)


    def set_media_player_position(self, position):
        # Lấy giá trị mới của horizontal_slider
        new_slider_value = self.horizontal_slider.value()

        # Lấy tổng thời lượng của bài hát
        total_duration = self.media_player.duration()

        # Tính toán thời lượng mới của bài hát dựa trên giá trị của horizontal_slider
        new_position = int((new_slider_value / self.horizontal_slider.maximum()) * total_duration)

        # Đặt thời lượng mới cho bài hát
        self.media_player.setPosition(new_position)

    # xử lý btn next music
    def next_track(self):
        current_index = self.track_list_widget.currentRow()
        if current_index < self.track_list_widget.count() - 1:
            next_index = current_index + 1
            next_track_info = self.track_infos[next_index]
            track_name, artist_name, preview_url = next_track_info
            # nếu gặp bài nhạc không có preview_url liên tiếp thì lập tức bỏ qua
            while(True):
                if preview_url:
                    self.play_audio_from_url(preview_url)
                    self.DisplayNameMusic_Label.setText(f" {track_name} - {artist_name}")
                    self.track_list_widget.setCurrentRow(next_index)
                    self.setImageMusic(track_name,artist_name)
                    # checkMessage =True
                    break
                # khi bài hát không tồn tại chuyển qua bài mới luôn
                else:
                    next_index +=1
                    next_track_info = self.track_infos[next_index]
                    track_name, artist_name, preview_url = next_track_info
            
        else:
            QMessageBox.information(self, "Thông báo", "Đã phát hết danh sách bài hát.")

    # lùi bài hát
    def previous_track(self):
        current_index = self.track_list_widget.currentRow()
        if current_index > 0:
            previous_index = current_index -1 
            previous_track_info = self.track_infos[previous_index]
            track_name, artist_name, preview_url = previous_track_info
            # nếu gặp bài nhạc không có preview_url liên tiếp thì lập tức bỏ qua
            while(True):
                if preview_url:
                    self.play_audio_from_url(preview_url)
                    self.DisplayNameMusic_Label.setText(f" {track_name} - {artist_name}")
                    self.track_list_widget.setCurrentRow(previous_index)
                    self.setImageMusic(track_name,artist_name)
                    # checkMessage =True
                    break
                # khi bài hát không tồn tại chuyển qua bài mới luôn
                else:
                    previous_index -=1
                    previous_track_info = self.track_infos[previous_index]
                    track_name, artist_name, preview_url = previous_track_info
        else:
            QMessageBox.information(self, "Thông báo", "Đã phát hết danh sách bài hát.")

    # hiển thị hình ảnh
    def setImageMusic(self,track_name,artist_name):
    # Truy vấn thông tin chi tiết của bài hát từ Spotify API
        response = self.spotify_client.search(q=f"track:{track_name} artist:{artist_name}", type="track", limit=1)
        if response['tracks']['items']:
            track_id = response['tracks']['items'][0]['id']

            # Lấy URL của ảnh đại diện từ Spotify API
            album_response = self.spotify_client.track(track_id)
            if album_response and album_response['album'] and album_response['album']['images']:
                image_url = album_response['album']['images'][0]['url']

                # Tải ảnh từ URL
                image_data = requests.get(image_url).content

                # Hiển thị ảnh trong QLabel
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.album_art_label.setPixmap(pixmap)
                self.album_art_label.setScaledContents(True)
            else:
                QMessageBox.information(self, "Thông báo", "Không có ảnh cho bài hát này.")
        else:
            QMessageBox.information(self, "Thông báo", "Không tìm thấy thông tin chi tiết của bài hát.")
    
    # chuyển qua bài tiếp theo khi thanh phát nhạc chạy hết
    def check_slider_position(self):
        # Lấy giá trị hiện tại của horizontal_slider
        current_slider_value = self.horizontal_slider.value()
        # Lấy giá trị tối đa của horizontal_slider
        max_slider_value = self.horizontal_slider.maximum()

        # Nếu giá trị hiện tại bằng giá trị tối đa, tức là thanh đã chạy hết
        if current_slider_value == max_slider_value:
            # Nếu chế độ repeat đang được bật, thì chuyển đến bài hát đầu tiên
            if self.is_repeating:
                self.media_player.setPosition(0)
            else:
                # Nếu không, chuyển đến bài tiếp theo
                self.next_track()

    # Chức năng lặp lại bài hát            
    def repeat_music(self):
        self.is_repeating = not self.is_repeating
        if self.is_repeating:
            self.repeat_button.setStyleSheet("background-color: red")
        else:
            self.repeat_button.setStyleSheet("")
    
    def get_track_url(self, track_name, artist_name):
        results = self.spotify_client.search(q=f"track:{track_name} artist:{artist_name}", type="track", limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            track_url = f"https://open.spotify.com/track/{track_id}"
            return track_url
        return None

    # Chức năng download bài hát xuống
    def download_track(self):
        index = self.track_list_widget.currentRow() 
        track_name, artist_name, preview_url = self.track_infos[index]
        print(preview_url)
        if preview_url:
            response = requests.get(preview_url)
            if response.status_code == 200:
                # Lưu nội dung tải về vào file mp3
                # file_name = f"{track_name} - {artist_name}.mp3"
                file_path, _ = QFileDialog.getSaveFileName(self, "Chọn nơi lưu file", f"{track_name} - {artist_name}.mp3", "MP3 Files (*.mp3)")
                if file_path:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                QMessageBox.information(self, "Thông báo", f"Đã tải bài hát '{track_name}' về máy thành công!")
            else:
                QMessageBox.warning(self, "Cảnh báo", f"Không thể tải bài hát '{track_name}' về máy.")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Bài hát không có URL để tải về.")
