# for temp directory stuff.
from shutil import rmtree
from os import makedirs
from os import chmod
import os.path

# for audio processing
from pydub import AudioSegment
import scipy.io.wavfile as wavfile


class VisualizerCore:

  # directory of temporary audio files
  tmpDir = './tmp/'

  original_music_file = ''
  normalized_music_file = ''
  sample_rate = 44100

  def __init__(self, music_file):
    self.original_music_file = music_file
    # normalize audio to a canonical format.
    self.normalize_audio()
    # process normalized audio by fft'ing, chunking, etc.
    self.process_audio()

  def normalize_audio(self):
    music = AudioSegment.from_mp3(self.original_music_file)
    self.createTmpDirectories()
    self.normalized_music_file = './tmp/sleep_deprivation'
    music.export(self.normalized_music_file, format='wav')

  def process_audio(self):
    # read the file
    samplingRate, data = wavfile.read( self.normalized_music_file )
    # get audio track data (mono)
    a = data.T
    # get length of amount of samples
    aLength = len(a)

    print 'audio track data'
    print a


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
