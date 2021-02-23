from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import matplotlib.pylab as plt
from scipy.signal import find_peaks
from matplotlib.pyplot import figure
from scipy import signal

def getSpectrogramParameters(file, startPos, endPos, parts,M):
    rate, curraudio, timeLength = loadSong(file, startPos, endPos, parts)

    frequencies, times, Sx = signal.spectrogram(curraudio, fs=rate, window='hanning',
                                                nperseg=M, noverlap=M - 250,
                                                detrend=False, scaling='spectrum')
    Sx = 20 * np.log10(Sx)  # converting to db
    S = Sx.T
    return frequencies, times, S, timeLength

def loadSong(file,start,end,parts):
    song = 'wavs\\' + file
    rate, audio = wavfile.read(song)
    audio = np.mean(audio, axis=1)
    curraudio = audio[start*len(audio)//parts:end*len(audio)//parts - 1]
    N = curraudio.shape[0]
    L = N / rate
    return rate,curraudio,L

def plotSpectrogram(times,newfreqs,newSx,showPlot):
    f, ax = plt.subplots(figsize=(4.8, 2.4))
    ax.pcolormesh(times, newfreqs / 1000, newSx, cmap='viridis')
    ax.set_ylabel('Frequency [kHz]')
    ax.set_xlabel('Time [s]')
    plt.savefig('spectrograms\\spec')

    if showPlot:
        plt.show()
    plt.clf()


def getPeaks(F, frequencies, prom, height, lowerFreqValue, upperFreqValue, width = None):
    lowerFreqPos, upperFreqPos = getFrequencies(frequencies, lowerFreqValue, upperFreqValue)
    figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
    frequencyRange = 0
    for i in range(lowerFreqPos, upperFreqPos):
        frequencyRange += F.T[i]
    frequencyRange /= (upperFreqPos - lowerFreqPos)
    peaks, _ = find_peaks(frequencyRange, prominence=prom, height=height, distance = width)  # BEST!

    return peaks,frequencyRange

def getFrequencies(freqs,hertzlower,hertzupper):
    lower = -1
    upper = -1
    for i in range(0, len(freqs)):
        if lower == -1 and freqs[i] <= hertzlower and freqs[i+1] > hertzlower:
            lower = i
        if i > 0 and freqs[i] >= hertzupper:
            upper = i+1
            break
    return lower,upper


def plotPeaks(peaks,frequencyRange,name,showPlot):
    plt.plot(peaks, frequencyRange[peaks], "ob");plt.plot(frequencyRange);plt.legend(['prominence'])
    plt.savefig('peaks\\peaks'+str(name))
    if showPlot:
        plt.show()
    plt.clf()


def splitSong(file,start,end,parts, specific_name = ''):
    typ = file.split('.')[1]
    if typ == 'mp3':
        audio = AudioSegment.from_mp3('mp3\\' + file)
        pt = 'mp3\\' + 'temp'+ specific_name + '.mp3'

    else:
        audio = AudioSegment.from_wav('wavs\\' + file)
        pt = 'wavs\\' + 'temp'+ specific_name + '.wav'
    curraudio = audio[start*len(audio)//parts:(end*len(audio)//parts) - 1]
    curraudio.export(pt)
    return pt

