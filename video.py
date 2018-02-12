import glob
import os
import subprocess as sp

try:
    os.remove("Snaps/img0000.png")
except:
    pass

cmd = "ffmpeg -f image2 -r 48 -i Snaps/img%04d.png -vcodec mpeg4 -y movie.mp4"
cmd = cmd.split()
process = sp.Popen(cmd, stdout=sp.PIPE)
process.wait()
print("done making video!")


