import numpy as np # for numerical operations
from moviepy.editor import VideoFileClip, concatenate

"""
Find the audio volume of each second of the match and store it
in volumes.
"""
clip = VideoFileClip("barca_madrid.mp4")
cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=35000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in range(0,int(clip.duration-1))]