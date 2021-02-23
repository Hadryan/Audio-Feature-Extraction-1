from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QWidget, QVBoxLayout, QGraphicsOpacityEffect, QPushButton, QGraphicsWidget, QHBoxLayout, QGraphicsColorizeEffect
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QParallelAnimationGroup, Qt, QPoint
from PyQt5.QtCore import pyqtSlot,QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QBrush, QColor, QRadialGradient
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

class widgetCircle(QLabel):
    def __init__(self, MainWindow, allColors, size, brush_size, start_pos):
        QWidget.__init__(self, parent=MainWindow)
        self.start_pos = start_pos
        self.color = allColors
        self.brush_size = brush_size
        self.size = size
        self.width = MainWindow.width - 200
        self.height = MainWindow.height - 200
        self.setGeometry((MainWindow.width - self.width)/2, (MainWindow.height - self.height)/2, self.width, self.height)
        self.setStyleSheet('background-color: rgba(255, 255, 255, 0);')

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setOpacity(.6)
        paint.setRenderHint(QPainter.Antialiasing)
        #a = QBrush(Qt.magenta)
        #paint.setBrush(a)
        paint.setPen(QPen(Qt.darkCyan, self.brush_size, Qt.SolidLine))
        paint.drawEllipse(self.width - (self.width + self.size) / 2, self.height - (self.height + self.size) / 2, self.size, self.size)

class widget(QLabel):
    def __init__(self, MainWindow, allColors, size, brush_size, start_pos):
        QWidget.__init__(self, parent=MainWindow)
        self.start_pos = start_pos
        self.color = allColors
        self.brush_size = brush_size
        self.size = size
        self.width = MainWindow.width - 200
        self.height = MainWindow.height - 200
        self.setGeometry((MainWindow.width - self.width)/2, (MainWindow.height - self.height)/2, self.width, self.height)
        self.setStyleSheet('background-color: rgba(255, 255, 255, 0);')



    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setOpacity(1)
        paint.setRenderHint(QPainter.Antialiasing)
        value = 10
        #a = QBrush(Qt.darkCyan)
        #paint.setBrush(a)
        #paint.drawEllipse(self.width - (self.width + self.size) / 2, self.height - (self.height + self.size) / 2, self.size, self.size)
        for i in range(0,value):
            paint.setPen(QPen(QColor((self.color[0] + self.color[1]*i/value)% 255, (self.color[1]+ self.color[2]*i/value)%255, (self.color[2]+ self.color[0]*i/value)%255), self.brush_size, Qt.SolidLine))
            paint.drawArc(self.width - (self.width + self.size) / 2, self.height - (self.height + self.size) / 2,
                          self.size, self.size, self.start_pos + 360/value*i*16, 1000/value)

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
        self.child_widget = self.set_widgets('circle')
        self.child_widget_circle = self.set_widgets('arc')
        #self.black_rectangle = QLabel(self)
        #self.black_rectangle.setGeometry(0, self.height/2-10, self.width, 20)
        #self.black_rectangle.setStyleSheet('background-color: rgba(0, 255, 255, 5);')
        self.set_static_frame()
        self.set_frame()
        self.startDetect()

        self.startSong(file, start_pos, end_pos, parts, volume)
        self.initUI()
        self.makeButton()

        self.show()

    def set_widgets(self, widget_type):
        self.amount_rings = 6
        child_widget = [[None for i in range(self.amount)] for j in range(self.amount_rings)]

        for i in reversed(range(0,self.amount)):
            color = (i % 3) * 100
            color2 = ((i + 1) % 3) * 100
            color3 = ((i + 2) % 3) * 100
            allColors = [color, color2, color3]
            for j in range(0,self.amount_rings):
                if widget_type == 'arc':
                    child = widget(self, allColors,  30*j + 30*self.amount_rings*i, 3 + i, 2*360*i)
                elif widget_type == 'circle':
                    child = widgetCircle(self, allColors, 30 * j + 30 * self.amount_rings * i, 3 + i, 2 * 360 * i)
                child_widget[j][i] = child
                effect = QGraphicsOpacityEffect()
                child_widget[j][i].setGraphicsEffect(effect)
                self.an = QPropertyAnimation(effect, b"opacity")
                self.an.setDuration(0 + i * 50)
                self.an.setStartValue(0)
                self.an.setEndValue(0)
                self.an.start()
        return child_widget



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

        self.anim = [[0 for i in range(self.amount)] for j in range(self.amount_rings)]
        self.anim_group = [None] * self.amount
        self.iterate = [0 for x in range(self.amount)]
        self.qTimer = QTimer()
        self.qTimer.timeout.connect(self.getSensorValue)
        self.qTimer.start()

    def doAnimation(self, which_animation):
        self.anim_group[which_animation] = QParallelAnimationGroup()
        for i in range(0,len(self.child_widget)):
            effect = QGraphicsOpacityEffect()
            self.child_widget[i][which_animation].setGraphicsEffect(effect)
            self.anim[i][which_animation] = QPropertyAnimation(effect, b"opacity")
            self.anim[i][which_animation].setDuration(500 + i*100)
            self.anim[i][which_animation].setStartValue(1)
            self.anim[i][which_animation].setEndValue(0)
            self.anim_group[which_animation].addAnimation(self.anim[i][which_animation])

            effect2 = QGraphicsOpacityEffect()
            self.child_widget_circle[i][which_animation].setGraphicsEffect(effect2)
            self.anim[i][which_animation] = QPropertyAnimation(effect2, b"opacity")
            self.anim[i][which_animation].setDuration(500 + i*100)
            self.anim[i][which_animation].setStartValue(1)
            self.anim[i][which_animation].setEndValue(0)
            self.anim_group[which_animation].addAnimation(self.anim[i][which_animation])
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
