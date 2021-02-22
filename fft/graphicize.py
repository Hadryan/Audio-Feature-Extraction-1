from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QWidget, QVBoxLayout, QGraphicsOpacityEffect, QPushButton, QGraphicsWidget, QHBoxLayout, QGraphicsColorizeEffect
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QParallelAnimationGroup, Qt, QPoint
from PyQt5.QtCore import pyqtSlot,QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QBrush, QColor
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


class widget(QLabel):
    def __init__(self, MainWindow, color, size):
        QWidget.__init__(self, parent=MainWindow)
        self.color = color
        self.size = size
        self.width = MainWindow.width - 200
        self.height = MainWindow.height - 200
        self.setGeometry((MainWindow.width - self.width)/2, (MainWindow.height - self.height)/2, self.width, self.height)
        self.setStyleSheet('background-color: rgba(255, 255, 255, 0);')



    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setOpacity(1)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setPen(QPen(self.color, 6, Qt.SolidLine))
        paint.drawEllipse(self.width - (self.width + self.size)/2, self.height - (self.height + self.size)/2, self.size, self.size)

class MainWindow(QMainWindow):
    # constructor
    def __init__(self, all_frequencies_times, file, start_pos, end_pos, parts, volume):
        super(MainWindow, self).__init__()
        self.top = 100
        self.left = 100
        self.width = 1200
        self.height = 800
        self.times = all_frequencies_times
        self.amount = numpy.array(self.times).shape[0]

        self.set_widgets()
        self.set_static_frame()
        self.set_frame()
        self.startDetect()

        self.startSong(file, start_pos, end_pos, parts, volume)
        self.initUI()
        self.makeButton()

        self.show()

    def set_widgets(self):
        self.child_widget = []
        self.child_widget_red = []
        changer = 50
        for i in reversed(range(0,self.amount)):
            child = widget(self, QColor(20,100 ,100+ changer), 0+30*i)
            self.child_widget.append(child)
            changer +=13
        changer = 20
        for i in (range(0,self.amount)):
            child = widget(self, QColor(150, 0, 50+changer), 0+30*i +15)
            self.child_widget_red.append(child)
            changer +=12


    def startSong(self,file, start_pos, end_pos, parts,volume):
        self.main_song = MainSong()
        self.main_song.getSong(file, start_pos, end_pos, parts)
        self.main_song.playSong(volume)

    def makeButton(self):

        self.button1 = QPushButton('PyQt5 button',self)
        self.button1.setStyleSheet("background-color: red")
        self.buttonX = self.width - self.button1.width()
        self.buttonY = 0
        self.button1.setText("Pause")
        self.button1.move(self.buttonX, self.buttonY)
        self.button1.clicked.connect(self.on_click)
        self.button_count = 0

    def paintEvent(self, event):

        c = self.button1.rect().center()
        a = QPoint(self.buttonX, self.buttonY)
        c = c + a
        startPosX = 50
        paint = QPainter(self)

        if self.button_count % 2 == 1:
            paint.setOpacity(1)
            paint.setPen(QPen(Qt.blue, 8, Qt.SolidLine))
            for i in range(self.amount):
                paint.drawEllipse(i * startPosX, 0, 50, 50)

            painter = QPainter(self)
            painter.setPen(QPen(Qt.blue, 8, Qt.SolidLine))
            painter.drawEllipse(c, 100, 50)
            self.update()
        else:
            paint.setOpacity(1)
            paint.setPen(QPen(Qt.black, 8, Qt.SolidLine))
            for i in range(self.amount):
                paint.drawEllipse(i * startPosX, 0, 50, 50)
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

    def set_static_frame(self):
        self.static_frames = []

    def set_frame(self):
        self.framar = []

    def getSensorValue(self):
        for i in range(self.amount):
            if self.iterate[i] >= self.times[i].size:
                continue
            check_time = round(self.times[i][self.iterate[i]], 3)
            curr_time = round(self.main_song.song.music.get_pos()/1000, 3)
            if curr_time >= check_time:
                self.doAnimation(i)
                self.iterate[i] += 1


    def startDetect(self):

        self.anim = [None] * self.amount
        self.animo = [None] * self.amount
        self.anim_group = [None] * self.amount
        self.iterate = [0 for x in range(self.amount)]
        self.qTimer = QTimer()
        self.qTimer.timeout.connect(self.getSensorValue)
        self.qTimer.start()

    def doAnimation(self, which_animation):
        effect = QGraphicsOpacityEffect()
        self.child_widget[which_animation].setGraphicsEffect(effect)
        self.anim[which_animation] = QPropertyAnimation(effect, b"opacity")
        self.anim[which_animation].setDuration(700)
        self.anim[which_animation].setStartValue(1)
        self.anim[which_animation].setEndValue(0)

        effect2 = QGraphicsOpacityEffect()
        self.child_widget_red[which_animation].setGraphicsEffect(effect2)
        self.animo[which_animation] = QPropertyAnimation(effect2, b"opacity")
        self.animo[which_animation].setDuration(1200)
        self.animo[which_animation].setStartValue(1)
        self.animo[which_animation].setEndValue(0)

        self.anim_group[which_animation] = QParallelAnimationGroup()
        self.anim_group[which_animation].addAnimation(self.anim[which_animation])
        self.anim_group[which_animation].addAnimation(self.animo[which_animation])

        self.anim_group[which_animation].start()




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
