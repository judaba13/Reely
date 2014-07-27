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
#plotData(vid_length,smooth_volumes,'Time(seconds)','Volume','Average Volume for the next 10 seconds for the video')

"""
Select the times of the top 10 percent largest peaks.
The idea is that the loudest sections of the video are the most 
important to include in the highlights
"""
increases = np.diff(smooth_volumes)[:-1] >= 0
decreases = np.diff(smooth_volumes)[1:] <= 0
peak_times = (increases * decreases).nonzero()[0]
peak_volumes = smooth_volumes[peak_times]
peak_times = peak_times[peak_volumes > np.percentile(peak_volumes,90)]

"""
For at least sporting events we can refine the peak times to 
group those that are less than one minute apart. The assumption
is that these times most likely correspond to the same event
"""
highlight_times = [peak_times[0]]
for time in peak_times:
	if(time - highlight_times[-1]) < 60:
		if smooth_volumes[time] > smooth_volumes[highlight_times[-1]]:
			highlight_times[-1] = time #use the time with the highest volume in chunks of 60 sec
	else:
		highlight_times.append(time)

"""
Final times contains the times in seconds of the most important
events based on this naive sound model. For each event, we can now
cut the original video 5 seconds before its time and stop 5 seconds
after its time to get 11 second clips for each event. 
TODO: play around with this span
"""
final_highlights = concatenate([clip.subclip(max(time-5,0),min(time+5,clip.duration))
	for time in highlight_times])
final_highlights.to_videofile('barca_madrid_highlights.mp4',fps=60)
print "Reely is done generating highlight for the video"