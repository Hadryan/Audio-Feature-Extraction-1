from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QParallelAnimationGroup, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
import time
from pygame import mixer  # Load the popular external library
from pydub import AudioSegment
import sys
import numpy


class MainWindow(QMainWindow):
    # constructor
    def __init__(self, all_frequencies_times):
        # QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        self.times = all_frequencies_times
        self.amount = numpy.array(self.times).shape[0]

        self.set_label()
        self.set_static_frame()
        self.set_frame()
        self.startDetect()

        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle('Equalizer')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def set_label(self):
        self.static_label = []
        startPosX = 50
        startPosY = 50
        for i in range(self.amount):
            self.qLbl = QLabel(self)
            self.qLbl.move(200, 100 + startPosY * i)
            self.qLbl.setStyleSheet("color: red;")
            self.static_label.append(self.qLbl)

    def set_static_frame(self):
        self.static_frames = []
        startPosX = 50
        startPosY = 100
        for i in range(self.amount):
            self.child = QWidget(self)
            self.child.setStyleSheet("background-color:red;border-radius:15px;")
            self.child.setGeometry(i * startPosX, 0, 50, 100)
            self.static_frames.append(self.child)

    def set_frame(self):
        self.framar = []
        startPosX = 50
        startPosY = 100
        for i in range(self.amount):
            self.child = QWidget(self)
            self.child.setStyleSheet("background-color:blue;border-radius:15px;")
            self.opacity_effect = QGraphicsOpacityEffect()

            # setting opacity level
            self.opacity_effect.setOpacity(0)

            # adding opacity effect to the label
            self.child.setGraphicsEffect(self.opacity_effect)
            self.child.setGeometry(i * startPosX, 0, 50, 100)
            self.framar.append(self.child)

    def getSensorValue(self):
        for i in range(self.amount):
            check_time = round(self.times[i][self.iterate[i]], 3)
            curr_time = round(time.time() - self.start_time, 3)
            if curr_time >= check_time:
                self.doAnimation(i)
                self.iterate[i] += 1
                self.static_label[i].setText('%d' % self.iterate[i])
                self.static_label[i].adjustSize()

    def startDetect(self):

        self.anim = [None] * self.amount
        self.iterate = [0 for x in range(self.amount)]
        self.start_time = time.time()
        self.qTimer = QTimer()
        self.qTimer.timeout.connect(self.getSensorValue)
        self.qTimer.start()

    def doAnimation(self, which_animation):
        self.effect = QGraphicsOpacityEffect()
        self.framar[which_animation].setGraphicsEffect(self.effect)
        self.anim[which_animation] = QPropertyAnimation(self.effect, b"opacity")
        self.anim[which_animation].setDuration(1400)
        self.anim[which_animation].setStartValue(1)
        self.anim[which_animation].setEndValue(0)
        self.anim[which_animation].start()

    def getSong(self, file, start, end, parts):
        audio = AudioSegment.from_wav(file)
        curr_audio = audio[start * len(audio) // parts:(end * len(audio) // parts) - 1]
        curr_audio.export(file, format="wav")
        self.song = mixer
        self.song.init()
        self.song.music.load(file)

    def playSong(self, volume):
        self.song.music.set_volume(volume)
        self.song.music.play()

    def stopSong(self):
        self.song.quit()
        print('Song stopped')

    def closeEvent(self, event):
        print('closing')
        self.deleteLater()


def startProgram(q_app, file, start_pos, end_pos, parts, volume, all_frequencies_times):
    import sys

    def my_excepthook(type, value, tback):
        # log the exception here

        # then call the default handler
        sys.__excepthook__(type, value, tback)

    sys.excepthook = my_excepthook
    q_win = MainWindow(all_frequencies_times)

    q_win.getSong(file, start_pos, end_pos, parts)
    q_win.playSong(volume)
    q_app.aboutToQuit.connect(q_win.stopSong)  # myExitHandler is a callable

    try:
        sys.exit(q_app.exec_())
    except:
        print('exiting')
