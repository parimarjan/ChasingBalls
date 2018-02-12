import glob
import os
import subprocess as sp

os.remove("Snaps/img0000.png")
cmd = "ffmpeg -f image2 -r 48 -i img%04d.png -vcodec mpeg4 -y movie.mp4"
cmd = cmd.split()
process = sp.Popen(cmd, stdout=sp.PIPE)


