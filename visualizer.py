import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QGraphicsBlurEffect
from PySide6.QtGui import QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImageReader


class SpotifyVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Visualizer")
        self.setGeometry(200, 200, 900, 500)
        self.setStyleSheet("background-color: #003366; color: white;")

        # Main container
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Layout for the album cover and track info
        self.header_layout = QHBoxLayout()
        self.layout.addLayout(self.header_layout)

        # Album cover and blurred background
        self.cover_label = QLabel(self)
        self.cover_label.setFixedSize(300, 300)
        self.cover_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("/tmp/cover.jpeg")
        self.cover_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

        # Applying sharp cover image with rounded corners
        self.cover_label.setStyleSheet("""
            border-radius: 20px;
            border: 2px solid white;
        """)

        self.header_layout.addWidget(self.cover_label)

        # Track info
        self.track_info_label = QLabel(self)
        self.track_info_label.setFont(QFont("Arial", 14))
        self.track_info_label.setWordWrap(True)
        self.track_info_label.setText(
            "Song Title (from the series Arcane League of Legends)\n2024 - Arcane, Stromae, Pomme"
        )

        self.header_layout.addWidget(self.track_info_label)

        # Progress bar
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.slider.setStyleSheet(
            """
            QSlider::groove:horizontal {background: #0055AA; height: 10px;}
            QSlider::handle:horizontal {background: #FFFFFF; width: 15px; border-radius: 7px;}
            """
        )
        self.layout.addWidget(self.slider, alignment=Qt.AlignCenter)

        # Time labels
        self.time_label_layout = QVBoxLayout()
        self.elapsed_label = QLabel("0:00", self)
        self.elapsed_label.setFont(QFont("Arial", 12))
        self.elapsed_label.setAlignment(Qt.AlignLeft)

        self.remaining_label = QLabel("2:27", self)
        self.remaining_label.setFont(QFont("Arial", 12))
        self.remaining_label.setAlignment(Qt.AlignRight)

        self.layout.addWidget(self.elapsed_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.remaining_label, alignment=Qt.AlignCenter)

        # Lyrics scrolling
        self.lyrics_label = QLabel(self)
        self.lyrics_label.setFont(QFont("Arial", 18))
        self.lyrics_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        self.lyrics_label.setWordWrap(True)

        with open("tmp/lyrics.txt", "r") as f:
            self.lyrics_text = f.read()
        self.lyrics_lines = self.lyrics_text.split("\n")
        self.current_line_index = 0
        self.lyrics_label.setText("\n".join(self.lyrics_lines[:3]))
        self.layout.addWidget(self.lyrics_label, alignment=Qt.AlignCenter)

        # Timer for progress and lyrics scrolling
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every second

        self.progress = 0

    def update_display(self):
        # Update progress slider
        self.progress += 1
        self.slider.setValue((self.progress / 147) * 100)  # Assuming 147 seconds total
        self.elapsed_label.setText(f"{self.progress // 60}:{self.progress % 60:02}")
        remaining_time = 147 - self.progress
        self.remaining_label.setText(f"{remaining_time // 60}:{remaining_time % 60:02}")

        # Update lyrics display
        if self.current_line_index < len(self.lyrics_lines) - 3:
            self.current_line_index += 1
            self.lyrics_label.setText("\n".join(self.lyrics_lines[self.current_line_index:self.current_line_index + 3]))

    def update_data(self, track_data, cover_image_path, lyrics_text):
        """
        Function to update UI components with new real-time data.
        """
        # Update track info
        track_name = track_data.get("name", "Unknown")
        artists = ", ".join(artist['name'] for artist in track_data.get("artists", []))
        self.track_info_label.setText(f"{track_name}\n{artists}")

        # Update cover image
        pixmap = QPixmap(cover_image_path)
        self.cover_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

        # Set the background color to the average color of the album cover
        avg_color = self.get_average_color(cover_image_path)
        self.set_background_color(avg_color)

        # Update lyrics
        self.lyrics_text = lyrics_text
        self.lyrics_lines = self.lyrics_text.split("\n")
        self.current_line_index = 0
        self.lyrics_label.setText("\n".join(self.lyrics_lines[:3]))

        # You can add more dynamic data (like popularity, album name, etc.) if desired
        # Example: track_data.get('popularity', 'Unknown')

    def get_average_color(self, image_path):
        """
        Get the average color of an image.
        """
        image = QImageReader(image_path).read()
        color = QColor(image.pixel(0, 0))  # Get the color of the top-left pixel for simplicity
        return color

    def set_background_color(self, color):
        """
        Set the background color of the main window.
        """
        color_hex = color.name()  # Get the color as hex
        self.setStyleSheet(f"background-color: {color_hex}; color: white;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpotifyVisualizer()
    window.show()

    # Example of updating data dynamically after some time or event
    def simulate_data_update():
        track_data = {
            "name": "Fuis-Moi",
            "artists": [{"name": "Stromae"}],
            "album": {"name": "Arcane (Season 2)"},
        }
        cover_image_path = "tmp/cover.jpeg"
        lyrics_text = """Mais ma meilleure
ennemie, c'est toi
Fuis-moi
Le pire, c'est toi et moi
..."""  # Add lyrics text

        window.update_data(track_data, cover_image_path, lyrics_text)

    QTimer.singleShot(3000, simulate_data_update)  # Simulate data update after 3 seconds

    sys.exit(app.exec())
