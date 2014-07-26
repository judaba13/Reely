import numpy as np # for numerical operations
from moviepy.editor import VideoFileClip, concatenate
import matplotlib.pyplot as plt #for visualization of sound data

"""
Plotting function using matplotlib
"""
def plotData(x_data,y_data,x_label,y_label,title):
	plt.plot(x_data,y_data)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(title)
	plt.show()

"""
Find the audio volume of each second of the match and store it
in volumes.
"""
clip = VideoFileClip("barca_madrid.mp4")
#get the video length to plot the sound data against it
vid_length = [x for x in range(0,int(clip.duration-11))]
cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=35000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in range(0,int(clip.duration-1))]
"""
This is a naive model for now, but smooth the volume data by 
computing the average volume over periods of 10 seconds
"""
smooth_volumes = np.array([sum(volumes[i:i+10])/10 
	for i in range(len(volumes)-10)])

#plot the game's sound data
plotData(vid_length,smooth_volumes,'Time(seconds)','Volume','Average Volume for the next 10 seconds for the video')