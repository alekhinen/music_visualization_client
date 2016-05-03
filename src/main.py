from pydub import AudioSegment
from shutil import rmtree
from os import makedirs
from os import chmod
import os.path


class VisualizerCore:

  # directory of temporary audio files
  tmpDir = './tmp/'

  music_file = ''
  sample_rate = 44100

  def __init__(self, music_file):
    self.music_file = music_file
    music = AudioSegment.from_mp3(music_file)
    self.createTmpDirectories()
    music.export('./tmp/', format='wav')

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
