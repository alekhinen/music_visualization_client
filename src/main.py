# for temp directory stuff.
from shutil import rmtree
from os import makedirs
from os import chmod
import os.path

# for audio processing
import math
from pydub import AudioSegment
import scipy.io.wavfile as wavfile
from scipy.fftpack import fft


class VisualizerCore:

  # directory of temporary audio files
  tmpDir = './tmp/'

  original_music_file = ''
  normalized_music_file = ''
  
  audio_fragment_size = 0.125

  # the fourier-transformed, time-bucketed fragments.
  fragments = []

  def __init__(self, music_file):
    self.original_music_file = music_file
    # normalize audio to a canonical format.
    self.normalize_audio()
    # process normalized audio by fft'ing, chunking, etc.
    self.process_audio()
    # computer color values for the fragmented audio segments
    self.colorize_audio()

  def normalize_audio(self):
    music = AudioSegment.from_mp3(self.original_music_file)
    self.createTmpDirectories()
    self.normalized_music_file = './tmp/sleep_deprivation'
    # TODO: need to ensure this is being normalized to a mono channel (update: it ain't).
    music.export(self.normalized_music_file, format='wav', parameters=['ac', '1'])

  def process_audio(self):
    # read the file
    sampling_rate, data = wavfile.read( self.normalized_music_file )
    # TODO: getting the first channel. should be single channel from the start.
    # get audio track data (mono)
    a = data.T[0]
    # get the amount of samples
    a_length = len(a)

    print a_length

    # setting up chunking process
    fragment_size = int(sampling_rate * self.audio_fragment_size)
    fragment_count = int(2 * math.floor(a_length / fragment_size) - 1)
    fragments    = []

    # TODO: debug
    print 'processing'
    print 'fragment_count: '
    print fragment_count
    print 'fragment_size: '
    print fragment_size

    i = 0
    # build each fragment up
    while (i < fragment_count):
      current_fragment = []
      
      j = i * fragment_size
      # get each individual sample for the fragment
      while ((j < (i + 1) * fragment_size) and j < a_length):
        # normalize sample on [-1, 1)
        normalized_sample = (a[j] / 256)*2-1
        # add to current_fragment array
        current_fragment.append(normalized_sample)
        # increment j
        j += 1

      # process current fragment through the FFT.
      processed_fragment = fft(current_fragment)
      # TODO: PROCESS SOME MO for visualization.
      fragments.append(processed_fragment)

      i += 1

    # TODO: debug
    print fragments
    self.fragments = fragments

  def colorize_audio(self):
    pass



  # -------------------------------------------------------------------------- #
  # Conversion #

  # createTmpDirectories()
  # @description: creates tmp directories
  # @returns: void
  # @author: Nick Alekhine, Charles Perrone
  # @version: 11-11-2014
  def createTmpDirectories(self):
    # set read/write/execute  permissions on current directory
    chmod('./', 0777)
    # remove tmp directory if it exists.
    self.removeTmpDirectories()
    # create the tmp directory
    makedirs(self.tmpDir)
    # set read/write/execute on tmp directory
    chmod(self.tmpDir, 0777)

  # removeTmpDirectories()
  # @description: removes tmp directories
  # @returns: void
  # @author: Nick Alekhine, Charles Perrone
  # @version: 11-11-2014
  def removeTmpDirectories( self ):
    # check if tmp directory exist. if so, delete them.
    if ( os.path.exists( self.tmpDir ) ):
      rmtree( self.tmpDir )



if __name__ == '__main__':
  print "Going to visualize music."
  core = VisualizerCore('./assets/sleep_deprivation.mp3')
