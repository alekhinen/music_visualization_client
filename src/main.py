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

# for sending requests
from api_requests import post_colors

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
    # self.colorize_audio()

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
      while (j < (i + 1) * fragment_size and j < a_length ):
        # normalize sample on [-1, 1)
        normalized_sample = (a[j] / 256)*2-1
        # add to current_fragment array
        current_fragment.append(normalized_sample)
        # increment j
        j += 1

      # process current fragment through the FFT.
      processed_fragment = fft(current_fragment)
      # TODO: PROCESS SOME MO for visualization.
      self.colorize_audio(processed_fragment)
      # fragments.append(processed_fragment)

      i += 1

    print 'finished'
    # self.fragments = fragments

  def colorize_audio(self, fragment):
    # normalize the fragment by using the magnitude
    normalized_fragment = map(VisualizerCore.mag, fragment)
    
    # The upper-bounds for each band, binned logarithmically 
    boundaries = [20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480]
    # The Value in each band, initially should all be zero
    bin_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]

    band = 0 #The Index of the band being scanned
    for i in range(len(fragment)): #For each data point in the fragment
      if (i >= boundaries[band]): #Check if the band changed
        band += 1
      bin_values[band] += int(normalized_fragment[i]) #Add to the current band

    bin_max = 0
    bin_max_position = 0
    b = 0
    while ( b < len(bin_values) ):
      if bin_values[b] > bin_max:
        bin_max = bin_values[b]
        bin_max_position = b
      b += 1

    b = 0
    while ( b < len(bin_values) ):
      bin_values[b] = int(255 * (bin_values[b] / bin_max))
      b += 1

    print 'bin values:'
    print bin_values

    VisualizerCore.build_and_send_color_object(bin_values)

  @staticmethod
  def build_and_send_color_object(color_bins):
    color_object = {}
    i = 0
    for b in color_bins:
      key_name = 'color_' + str(i)
      color_object[key_name] = [b, 0, 0]
      i += 1
    print color_object
    post_colors(color_object)

  # mag()
  # @description: calculates the magnitude of a given number
  # @param: cnum - list of fragments
  # @author: Michael Chadbourne
  # @return: number
  @staticmethod
  def mag( cnum ):
    return math.sqrt(cnum.real**2 + cnum.imag**2)



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
