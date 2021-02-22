import config
from PyQt5.QtWidgets import QApplication
import graphicize
import sys
import librosa



M = 2048
drums = 'splitoutput\\temp0\\drums.wav'
bass = 'splitoutput\\temp0\\bass.wav'
volume = 0.3
startPos = 1
endPos = 2
parts = 2

frequencies, times, S, timeLength = config.getSpectrogramParameters(drums, startPos, endPos, parts, M)

# config.plotSpectrogram(times,newfreqs,Sx,False)

snarePeaks, frequencyRange = config.getPeaks(S, frequencies, prom=50, height=95,
                                             lowerFreqValue=1000, upperFreqValue=1500)
config.plotPeaks(snarePeaks, frequencyRange, 'Snare', showPlot=False)
snareTimes = times[snarePeaks]

kickPeaks, frequencyRange = config.getPeaks(S, frequencies, prom=25, height=130,
                                            lowerFreqValue=100, upperFreqValue=200)
config.plotPeaks(kickPeaks, frequencyRange, 'Kick', showPlot=False)
kickTimes = times[kickPeaks]

hihatPeaks, frequencyRange = config.getPeaks(S, frequencies, prom=25, height=20,
                                            lowerFreqValue=1000, upperFreqValue=10000)
config.plotPeaks(hihatPeaks, frequencyRange, 'Hihat', showPlot=False)
hihatTimes = times[hihatPeaks]

frequencies, times, S, timeLength = config.getSpectrogramParameters(bass, startPos, endPos, parts, M)
bassPeaks, frequencyRange = config.getPeaks(S, frequencies, prom=20, height=80,
                                            lowerFreqValue=20, upperFreqValue=200)
config.plotPeaks(bassPeaks, frequencyRange, 'Bass', showPlot=False)
bassTimes = times[bassPeaks]

all_frequencies_times = []
all_frequencies_times.append(bassTimes)
all_frequencies_times.append(kickTimes)
all_frequencies_times.append(snareTimes)
all_frequencies_times.append(hihatTimes)
all_frequencies_times.append(bassTimes)
all_frequencies_times.append(kickTimes)
all_frequencies_times.append(snareTimes)
all_frequencies_times.append(kickTimes)
all_frequencies_times.append(snareTimes)
all_frequencies_times.append(hihatTimes)
all_frequencies_times.append(kickTimes)
all_frequencies_times.append(hihatTimes)

all_frequencies_times.append(snareTimes)

qApp = QApplication(sys.argv)

fullsong = config.splitSong('letgo.mp3', 0, 1, 4)
graphicize.startProgram(qApp, fullsong, startPos, endPos, parts, volume, all_frequencies_times)
