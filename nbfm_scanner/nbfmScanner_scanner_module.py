import numpy as np

def avg_freq_power(data):
	weighted_power = 0
	sum_power = 0
	
	for index,sample in enumerate(data):
		weighted_power += index * float(sample)
		sum_power += float(sample)
		
	if len(data) <= 0:
		return 0,0
	else:
		return weighted_power/float(sum_power), sum_power

def estimate(spectrum, threshold):
	
	spectrum = np.append(spectrum, np.zeros(1))
	length   = len(spectrum)
	channels = []
	lnbins   = []
	bins     = []
	sum_powers = []
	index    = 0
	
	while index < length:
		if (spectrum[index] > threshold):
			bins.append(spectrum[index])
			index += 1
			
		elif (len(bins) > 3):
			avg_freq = avg_freq_power(bins)
			channels.append(index - len(bins) + avg_freq[0])
			
			lnbins.append(len(bins))
			sum_powers.append(avg_freq[1])
			index += 1
			bins = []
			
		else:
			index += 1
					
	return channels, lnbins, sum_powers
			
channels = []
lnbin = []
sum_powers = []
ret = [0,0, 0]
channel_spacing = 0.0005

last_frequency = 0
lastFreqSet = False;

def detect(data, fs, threshold, freq):
	global channels, lnbin, ret, channel_spacing, sum_powers, last_frequency, lastFreqSet
	
	if(lastFreqSet == False):
		last_frequency = freq
		lastFreqSet = True
	
	try:
		spectrum = list(data)
		spectrum = np.array([float(x) for x in spectrum])
		channels, lnbin, sum_powers = np.array(estimate(spectrum, threshold))
		
		if len(channels) > 0:
			resolution = fs / len(spectrum)
			channels = (channels - len(spectrum)/2)*resolution
			channels = np.round(channels/channel_spacing)*channel_spacing
			print(channels, lnbin)
			tmpf = []
			for ch in channels:
				tuned_channels = np.round((ch+freq*1e6),3)
				tmpf.append(tuned_channels)
			
			channels = tmpf
			idx = sum_powers.argmax(axis=0)
			#print("idx:" + str(idx))
			ret = [channels[idx], lnbin[idx], sum_powers[idx]]
			last_frequency = channels[idx]
		else:
			ret = [last_frequency,0,0]
	
	except Exception as e:
		print(e)
		pass
	
	print(ret)
	return ret

