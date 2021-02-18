import config
from PyQt5.QtWidgets import QApplication
import graphicize
import sys



M = 2048
file = 'splitoutput\\temp0\\drums.wav'
volume = 0.3
startPos = 1
endPos = 2
parts = 2

frequencies, times, S, timeLength = config.getSpectrogramParameters(file, startPos, endPos, parts, M)

#config.plotSpectrogram(times,newfreqs,Sx,False)


snarePeaks, frequencyRange = config.getPeaks(S, frequencies, prom=50, height=95,
                                             lowerFreqValue=1000, upperFreqValue=1500)
config.plotPeaks(snarePeaks, frequencyRange, 'Snare', showPlot=False)
snareTimes = times[snarePeaks]


bassPeaks, frequencyRange = config.getPeaks(S, frequencies, prom=25, height=130,
                                            lowerFreqValue=100, upperFreqValue=200)
config.plotPeaks(bassPeaks,frequencyRange, 'Bass', showPlot=False)
bassTimes = times[bassPeaks]

all_frequencies_times = []
all_frequencies_times.append(bassTimes)
all_frequencies_times.append(snareTimes)
# all_frequencies_times.append(bassTimes)

qApp = QApplication(sys.argv)

graphicize.startProgram(qApp, file, startPos, endPos, parts, volume, all_frequencies_times)




