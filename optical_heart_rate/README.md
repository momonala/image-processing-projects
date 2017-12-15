# Optical Heart Rate Detection via Webcam 

-----------------------------------------------------------------------------

<img src="optical_heart_rate/master/img/disp.png" width="700" alt="raw" />

------------------------------------------------------------------------------

This software uses real-time computer vision to measure heart-rate from changes in optical intensity measured via a webcam. This is a sort of ensemble implementation, drawing from software written by others in academia and as a hobby. Specifically, I draw heaviest from the techniques of [Ming-Zher Poh et. al.](https://encrypted.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=0ahUKEwiQ54iTs8LWAhUPJ1AKHawNCzEQFgg4MAI&url=https%3A%2F%2Fdspace.mit.edu%2Fopenaccess-disseminate%2F1721.1%2F66243%3Fapppush&usg=AFQjCNEStO7soqdfrhUdgwJtRTAgQX8IWA), while making the processing lighter weight and more readable. Remote signal aquisition (not in direct contact with the user) of heart rate, offers potential advantages over traditional ECG or finger pulse oximetry, including comfort to the user and no risk of irritation, which is especially import for neonatal usecases. 

The technique uses photoplethymography (PPG), which is a  means of sensing a cardiovascular pulse wave (blood volume of a heart beat) through variations in transmitted or reflected light. Interestingly, this is an information dense criteria, offering insight into the heart rate, arterial blood oxygenation saturation, blood pressure, cardiac output, and autonomic function. If you'd like to hear more about what the folks at MIT are doing, click the link to Ming's paper above. 

### Methods 

I tested this code on a HP Spectre running Windows 10. I was able to get roughly a 7Hz sampling frequency after image processing, which means a max beats-per-minute (BPM) of 210, according to the Nyquist frequency (max frequency resolution is 1/2 sampling frequency). I'd be interested to hear what sampling frequency your machine gets. 

**Face, Forehead, Brighness Extractions**

The first step of the pipeline is image aquisition via webcam. I then use a pretrained Haar Cascade Classifier to extract the face. The pipeline can only handle one face per frame. I extract and resize the face to 150 pixels squared for standardization, and use predefined setpoints to extract the forehead. The forehead has thin skin and is the easiest measurement location for optical intensity of blood on the face. I split the forehead winow into its RGB components and find the brightness of each channel. Each is then appended into a 100 frame buffer stream (about 15 seconds) of brightness values. I apply a simple moving average (kernel size=4) to each channel buffer to remove high frequency noise. This is then detrended with scipy and normalized via x_norm = (x - u)/s where u and s are the mean and standard deviation of the buffer, respectively. This ensures 0 mean and 1 unit variance and eliminates any baseline shift. 

<img src="optical_heart_rate/master/img/raw.png" width="900" alt="raw" />

<img src="optical_heart_rate/master/img/processed.png" width="900" alt="raw" />


**Independent Component Analysis**

Next I perform a Independent Component Analysis (ICA) on each normalized channel buffer with sklearn.decomposition.FastICA. The ICA is unique to Ming's technique for webcam-based pulse readings (from my research). ICA is a  powerful technique to separate linearly mixed signal sources into additive subcomponents. Ex. The cocktail party problem of identifying a single voice out of many at in a loud room. Here I are making the assumption that the signals (RGB buffer streams) are independent of eachother and non-Gaussian. 

ICA transforms the data to minimize Gaussianity on each axis. With this, ICA is able to recover the original signal sources, which are statistically independent. This property comes from the Central Limit Theorem which states that any linear mixture of 2 independent random variables (our RGB signals) is more Gaussian than the original variables. In theory, we've extracted our signal of optical changes from the noise. Clever, eh? ICA is a rapidly expanding technique in mixed signal and biomedical signal engineering, namely ECG and EEG processing. 

<img src="optical_heart_rate/master/img/ICA.png" width="900" alt="raw" />


**Fourier Transform**

The ICA transformed data is still in the time domain, so I use scipy's Fourier Transfrom method to convert to the frequency domain. Its important to note that I extract time range of the channel buffers, but interpolate between the two endpoints for the Fourier. This makes the assumption that the channel buffer data points are perfectly spaced out, but there is minor variation. The variation between aquired frames looked to be about 0.0005 seconds, but I have not tested if this is significant. The dominant frequency from the Fourier is then taken via argmax and converted from Hz to BPM. I average the BPM over 20 frames and display. 

<img src="optical_heart_rate/master/img/fourier.png" width="900" alt="raw" />

**Display**

The webcam feed is displayed and the frequency domain is plotten via matplotlib. Time elapsed and BPM is reported on the feed. If the user looks away from the camera, or a Haar Cascade lock is lost, the buffers clear but the application stays open. Reinitilization of the buffers are needed. 

### Considerations and Future Steps: 

I am uploading this working prototype for now, but hope to improve it in the future if time permits. Specifically, I would like to find a better way to pick the dominant frequency (now I switch between the red and green channels, whatever provides the best results). I would also like to create a Flask app backend to display the webcam feed, time domain, and frequency plots to a web dashboard (and maybe some other stats). Additionally, compiling the software to an executable would be cool if I am able to fine tune the functionality. 

Any other ideas for improvement are welcome! 

### Dependences: 
    
    Python 3.5
    OpenCV 
    Scipy 
    Scikit Learn 
    Numpy 
    
### Additional Resources: 

[Thearn's implementation](https://github.com/thearn/webcam-pulse-detector) (poorly documented... :( )

[Optical Pulse Detection via Mobile Phone with Matlab](http://www.ignaciomellado.es/blog/Measuring-heart-rate-with-a-smartphone-camera)

[ICA explained](http://arnauddelorme.com/ica_for_dummies/)