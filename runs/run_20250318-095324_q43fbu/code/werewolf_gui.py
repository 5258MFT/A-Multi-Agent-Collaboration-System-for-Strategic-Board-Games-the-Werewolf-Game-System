from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import pyqtSignal, QObject, QUrl, pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

class UserInputSignal(QObject):
    user_input_received = pyqtSignal(str)
    output_message = pyqtSignal(str)
    discussion_end_choice = pyqtSignal(bool)  # 添加讨论结束选择信号

class WerewolfGameWindow(QMainWindow):
    start_game_signal = pyqtSignal()  # 添加启动游戏信号

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Werewolf Game")

        # 加载初始背景图片和音乐
        self.load_initial_background()
        self.load_initial_music()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("background: transparent; color: white;")  # 设置背景透明，文本颜色为白色
        self.layout.addWidget(self.output_display)

        self.input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("background: transparent; color: white;")  # 设置背景透明，文本颜色为白色
        self.submit_button = QPushButton("Submit")
        self.input_layout.addWidget(self.input_box)
        self.input_layout.addWidget(self.submit_button)
        self.layout.addLayout(self.input_layout)

        self.user_input_signal = UserInputSignal()

        self.submit_button.clicked.connect(self.send_user_input)
        self.input_box.returnPressed.connect(self.send_user_input)
        self.user_input_signal.output_message.connect(self.append_output)  # 连接输出消息信号

        # 创建并添加可变位置的图片按钮
        self.create_image_button()

        # 初始隐藏输入框
        self.set_input_visibility(False)

        # 创建头像字典
        self.avatars = {
            "Player1": ("./res/other_res/player1.png", "magenta"),     # 玩家1颜色为洋红色
            "Player2": ("./res/other_res/player2.png", "green"),   # 玩家2颜色为绿色
            "Player3": ("./res/other_res/player3.png", "blue"),    # 玩家3颜色为蓝色
            "Player4": ("./res/other_res/player4.png", "purple"),  # 玩家4颜色为紫色
            "Player5": ("./res/other_res/player5.png", "orange"),  # 玩家5颜色为橙色
            "Player6": ("./res/other_res/player6.png", "yellow"),  # 玩家6颜色为黄色
            "Player7": ("./res/other_res/player7.png", "cyan"),   # 玩家7颜色为青色
            "玩家": ("./res/other_res/玩家.png", "white")     # 玩家7颜色为白色
        }

        self.background_changed = False  # 用于判断背景是否已切换

        # 添加讨论结束选择按钮
        self.create_discussion_end_buttons()

    def load_initial_background(self):
        self.background_image = QPixmap("./res/other_res/111.jpg")
        self.setFixedSize(self.background_image.size())  # 设置窗口大小与图片像素一致

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.background_image.width(), self.background_image.height())

    def load_initial_music(self):
        self.music_player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("./res/other_res/666.mp3")))  # 初始背景音乐
        self.music_player.setPlaylist(self.playlist)
        self.music_player.play()

    def create_image_button(self):
        pixmap = QPixmap("./res/other_res/222.jpg")
        self.image_button = QPushButton(self)
        self.image_button.setIcon(QIcon(pixmap))
        self.image_button.setIconSize(pixmap.size())
        self.image_button.setFixedSize(pixmap.size())
        self.image_button.setStyleSheet("border: none;")

        # 初始位置放在窗口中央
        button_x = (self.width() - self.image_button.width()) // 2
        button_y = (self.height() - self.image_button.height()) // 100 * 60
        self.image_button.move(button_x, button_y)

        # 连接按钮点击信号到切换背景方法
        self.image_button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.switch_background()
        self.start_game_signal.emit()  # 发射启动游戏信号

    def switch_background(self):
        # 切换背景图片
        self.background_image = QPixmap("./res/other_res/333.jpg")
        self.background_label.setPixmap(self.background_image)
        self.setFixedSize(self.background_image.size())
        self.background_label.setGeometry(0, 0, self.background_image.width(), self.background_image.height())

        # 切换背景音乐
        self.playlist.clear()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("./res/other_res/777.mp3")))
        self.music_player.setPlaylist(self.playlist)
        self.music_player.play()

        # 隐藏按钮
        self.image_button.hide()

        # 显示输入框
        self.set_input_visibility(True)

        # 标记背景已切换
        self.background_changed = True

    def create_discussion_end_buttons(self):
        self.discussion_end_layout = QHBoxLayout()

        self.true_button = QRadioButton("是")
        self.true_button.setStyleSheet("background-color: white; color: black;")  # 设置背景色为白色，文字颜色为黑色
        self.false_button = QRadioButton("否")
        self.false_button.setStyleSheet("background-color: white; color: black;")  # 设置背景色为白色，文字颜色为黑色

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.true_button)
        self.button_group.addButton(self.false_button)

        self.discussion_end_layout.addWidget(self.true_button)
        self.discussion_end_layout.addWidget(self.false_button)

        self.layout.addLayout(self.discussion_end_layout)

        self.true_button.clicked.connect(self.send_discussion_end_choice)
        self.false_button.clicked.connect(self.send_discussion_end_choice)

        self.set_discussion_end_buttons_visibility(False)  # 初始隐藏按钮

    @pyqtSlot(bool)
    def set_discussion_end_buttons_visibility(self, visible):
        self.true_button.setVisible(visible)
        self.false_button.setVisible(visible)

    def send_discussion_end_choice(self):
        choice = self.true_button.isChecked()
        self.user_input_signal.discussion_end_choice.emit(choice)
        self.set_discussion_end_buttons_visibility(False)

    def move_button(self, x, y):
        self.image_button.move(x, y)

    def append_output(self, text):
        avatar = ""
        colored_text = text

        if text.startswith("Moderator"):
            avatar = '<img src="./res/other_res/moderator.png" width="30" height="30">'
            colored_text = f'<span style="color: red;">{text}</span>'
        elif text.startswith("玩家"):
            avatar = '<img src="./res/other_res/玩家.png" width="30" height="30">'
            colored_text = f'<span style="color: white;">{text}</span>'
        else:
            found_player = False
            for player, (avatar_path, color) in self.avatars.items():
                if text.startswith(player):
                    avatar = f'<img src="{avatar_path}" width="30" height="30">'
                    colored_text = f'<span style="color: {color};">{text}</span>'
                    found_player = True
                    break
            if not found_player:
                colored_text = text

        self.output_display.append(f"{avatar} {colored_text}")


    def send_user_input(self):
        user_input = self.input_box.text()
        if user_input:
            self.user_input_signal.user_input_received.emit(user_input)  # 确保信号正确发射
            self.input_box.clear()

    def request_input(self, prompt):
        self.append_output(prompt)
        self.input_box.setPlaceholderText(prompt)
        self.input_box.setFocus()

    def set_input_visibility(self, visible):
        self.input_box.setVisible(visible)
        self.submit_button.setVisible(visible)
