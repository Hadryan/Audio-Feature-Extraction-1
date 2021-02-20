from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QWidget, QVBoxLayout, QGraphicsOpacityEffect, QPushButton
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QParallelAnimationGroup, Qt, QPoint
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QBrush

import time
from pygame import mixer  # Load the popular external library
from pydub import AudioSegment
import numpy


class MainSong():

    def getSong(self, file, start, end, parts):
        typ = file.split('.')[1]
        if(typ == 'mp3'):
            audio = AudioSegment.from_mp3(file)
        else:
            audio = AudioSegment.from_wav(file)

        self.curr_audio = audio[start * len(audio) // parts:(end * len(audio) // parts) - 1]
        self.curr_audio.export(file)
        self.song = mixer
        self.song.init()
        self.song.music.load(file)

    def playSong(self, volume):
        self.song.music.set_volume(volume)
        self.song.music.play()

    def stopSong(self):
        self.song.quit()
        print('Song stopped')

class MainWindow(QMainWindow):
    # constructor
    def __init__(self, all_frequencies_times, file, start_pos, end_pos, parts, volume):
        # QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        self.times = all_frequencies_times
        self.amount = numpy.array(self.times).shape[0]


        #self.set_label()
        self.set_static_frame()
        self.set_frame()
        self.startDetect()
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.startSong(file, start_pos, end_pos, parts, volume)
        self.initUI()
        self.makeButton()

        self.show()

    def startSong(self,file, start_pos, end_pos, parts,volume):
        self.main_song = MainSong()
        self.main_song.getSong(file, start_pos, end_pos, parts)
        self.main_song.playSong(volume)

    def makeButton(self):
        self.buttonX = 200
        self.buttonY = 200
        self.button1 = QPushButton('PyQt5 button',self)
        self.button1.setStyleSheet("background-color: red")
        self.button1.setText("Pause")
        self.button1.move(self.buttonX, self.buttonY)
        self.button1.clicked.connect(self.on_click)
        self.button_count = 0

    def paintEvent(self, event):
        c = self.button1.rect().center()
        a = QPoint(self.buttonX, self.buttonY)
        c = c + a
        if self.button_count % 2 == 1:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.blue, 8, Qt.SolidLine))
            painter.drawEllipse(c, 100, 50)
            self.update()
        else:
            self.update()

    @pyqtSlot()
    def on_click(self):
        self.button_count+=1
        if self.button_count % 2 == 0:
            self.main_song.song.music.unpause()
            self.button1.setText("Pause")
        else:
            self.main_song.song.music.pause()
            self.update()
            self.button1.setText("Unpause")


    def initUI(self):
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle('Equalizer')
        self.setGeometry(self.left, self.top, self.width, self.height)


    def set_label(self):
        self.static_label = []
        startPosY = 50
        for i in range(self.amount):
            self.qLbl = QLabel(self)
            self.qLbl.move(200, 100 + startPosY * i)
            self.qLbl.setStyleSheet("color: red;")
            self.static_label.append(self.qLbl)

    def set_static_frame(self):
        self.static_frames = []
        # startPosX = 50
        # for i in range(self.amount):
        #     self.child = QWidget(self)
        #     self.child.setStyleSheet("background-color:red;border-radius:15px;")
        #     self.child.setGeometry(i * startPosX, 0, 50, 100)
        #     self.static_frames.append(self.child)

    def set_frame(self):
        self.framar = []


        startPosX = 50
        for i in range(self.amount):
            self.child = QWidget(self)
            self.child.setStyleSheet("background-color:blue;border-radius:15px;")
            self.opacity_effect = QGraphicsOpacityEffect()
            self.opacity_effect.setOpacity(0)
            self.child.setGraphicsEffect(self.opacity_effect)
            self.child.setGeometry(i * startPosX, 0, 50, 100)
            self.framar.append(self.child)

    def getSensorValue(self):
        for i in range(self.amount):
            if self.iterate[i] >= self.times[i].size:
                continue
            check_time = round(self.times[i][self.iterate[i]], 3)
            #curr_time = round(time.time() - self.start_time, 3)
            curr_time = round(self.main_song.song.music.get_pos()/1000, 3)

            if curr_time >= check_time:
                self.doAnimation(i)
                self.iterate[i] += 1
                #self.static_label[i].setText('%d' % self.iterate[i])
                #self.static_label[i].adjustSize()

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
    q_win = MainWindow(all_frequencies_times, file, start_pos, end_pos, parts, volume)
    q_app.aboutToQuit.connect(q_win.main_song.stopSong)  # myExitHandler is a callable

    try:
        sys.exit(q_app.exec_())
    except:
        print('exiting')
