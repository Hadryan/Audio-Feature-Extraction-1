#!/usr/bin/env ipython

# Authors: martijn.millecamp@student.kuleuven.be [Martijn Millecamp] & miro.masat@gmail.com [Miroslav Masat]
import sys
#sys.path.append('c:\\users\\myself\\appdata\\local\\programs\\python\\python37\\lib\\site-packages')
import librosa
import numpy
import matplotlib.pylab as plt



def extract_max(pitches,magnitudes, shape):
    new_pitches = []
    new_magnitudes = []
    for i in range(0, shape[1]):
        new_pitches.append(numpy.max(pitches[:,i]))
        new_magnitudes.append(numpy.max(magnitudes[:,i]))
    return (new_pitches,new_magnitudes)

def smooth(x,window_len=11,window='hanning'):
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
        s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=numpy.ones(window_len,'d')
        else:
                w=eval('numpy.'+window+'(window_len)')
        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]

def plot(vector, name, xlabel=None, ylabel=None):
    plt.figure()
    plt.plot(vector)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot()
    plt.savefig(name)
    #plt.show()


def set_variables(sample_f,duration,window_time,fmin,fmax,overlap):
    total_samples = sample_f * duration
    #There are sample_f/1000 samples / ms
    #windowsize = number of samples in one window
    window_size = sample_f/1000 * window_time
    hop_length = total_samples / window_size
    #Calculate number of windows needed
    needed_nb_windows = total_samples / (window_size - overlap)
    n_fft = needed_nb_windows * 2.0
    return total_samples, window_size, needed_nb_windows, n_fft, hop_length

def analyse(y,sr,n_fft,hop_length,fmin,fmax):
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, S=None, n_fft= n_fft, hop_length=hop_length, fmin=fmin, fmax=fmax, threshold=0.75)
    shape = numpy.shape(pitches)
    #nb_samples = total_samples / hop_length
    nb_samples = shape[0]
    #nb_windows = n_fft / 2
    nb_windows = shape[1]
    pitches,magnitudes = extract_max(pitches, magnitudes, shape)

    pitches1 = smooth(pitches,window_len=10)
    pitches2 = smooth(pitches,window_len=20)
    pitches3 = smooth(pitches,window_len=30)
    pitches4 = smooth(pitches,window_len=40)
    #
    # plot(pitches1, 'pitches1')
    # plot(pitches2, 'pitches2')
    # plot(pitches3, 'pitches3')
    # plot(pitches4, 'pitches4')
    # plot(magnitudes, 'magnitudes')
    # plot( y, 'audio')


def main():
    #Set all wanted variables

    #we want a sample frequency of 16 000
    sample_f = 44100
    #The duration of the voice sample
    duration = 50
    #We want a windowsize of 30 ms
    window_time = 60
    fmin = 20
    fmax = 10000
    #We want an overlap of 10 ms
    overlap = 20
    total_samples, window_size, needed_nb_windows, n_fft, hop_length = set_variables(sample_f, duration, window_time, fmin, fmax, overlap)
    print(needed_nb_windows)

    # y = audio time series
    # sr = sampling rate of y
    y, sr = librosa.load('brokenbiches (1).wav', sr=sample_f,duration = duration )
    print(len(y))
    #y1, sr1 = librosa.load('1', sr=sample_f, duration=duration)
    n_fft = int(n_fft)
    hop_length = int(hop_length)
    analyse(y, sr, n_fft, hop_length, fmin, fmax)
    #analyse(y1, sr1, n_fft, hop_length, fmin, fmax)



#main()


from scipy import signal
from scipy.io import wavfile
from skimage import util

M = 1024
song = 'brokenbiches (1).wav'
rate, audio = wavfile.read(song)
audio = numpy.mean(audio, axis=1)
print(rate)
N = audio.shape[0]
L = N / rate

print(f'Audio length: {L:.2f} seconds')


slices = util.view_as_windows(audio, window_shape=(M,), step=100)
print(f'Audio shape: {audio.shape}, Sliced audio shape: {slices.shape}')

win = numpy.hanning(M + 1)[:-1]
slices = slices * win

slices = slices.T
print('Shape of `slices`:', slices.shape)

spectrum = numpy.fft.fft(slices, axis=0)[:M // 2 + 1:-1]
spectrum = numpy.abs(spectrum)

import matplotlib.colors as colors
from matplotlib.colors import LogNorm
S = numpy.abs(spectrum)
S = 20 * numpy.log10(S / numpy.max(S))
#S = S[:][:1000]
F = []
for i in range(0,len(S)):
    F.append(S[i][:3000])
f, ax = plt.subplots(figsize=(4.8, 2.4))

ax.imshow(F, origin='lower', cmap='viridis',
          extent=(0, L, 0, 3000))
ax.axis('tight')
#ax.set_yscale('log')

ax.set_ylabel('Frequency [kHz]')
ax.set_xlabel('Time [s]')
plt.savefig('specc')
#plt.show()

print("BASS")
maxx = 0
#S[~numpy.isfinite(S)] = 0
print("LENGTH")
print(len(S))
fps = len(S)
i = 0
plt.figure()

#
# #winsound.PlaySound(song, winsound.SND_FILENAME)
# while i < len(S):
#
#
#     i+=1
#
#     print(i)
#     F = S[i]
#
#     #F[F < -100] = -100
#
#     G = sum(F)/len(F)
#     print(G)
#
#     plt.plot(F)
#     plt.pause(L/len(S))
#     plt.clf()
#
#


# Play the wav file
#
# print(rate)
# print(audio.shape[-1])
# freqs, times, Sx = signal.spectrogram(audio, fs=rate, window='hanning',
#                                       nperseg=1024, noverlap= 924,
#                                       detrend=False, scaling='spectrum')
#
# f, ax = plt.subplots(figsize=(4.8, 2.4))
# ax.pcolormesh(times, freqs / 1000, 10 * numpy.log10(Sx), cmap='viridis')
# ax.set_ylabel('Frequency [kHz]')
# ax.set_xlabel('Time [s]');