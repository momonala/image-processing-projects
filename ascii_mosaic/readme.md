## Pixels to Ascii Characters

This code is inspired from the [BitsOfCode](https://bitesofcode.wordpress.com/2017/01/19/converting-images-to-ascii-art-part-1/) blog post on converting pixel values of an image to ascii characters. I created an image processor in [AsciiMosiac.py](AsciiMosiac.py) to do this efficiently, making use of numpy's `np.vectorize` function to vectorize iterating through the image and mapping the pixels to ascii characters. A rough workflow is explained in [test_ascii_mosiac_gif.ipynb](test_ascii_mosiac_gif.ipynb), where I convert an image to the ascii characters, and create a gif to zoom in on the detail. 

<img src="obama/obama_ascii_2.png" width="600" alt="raw" />

I decided to go one step further and select specific text for the ascii character mapping. This was accomplished by getting the transcript of a speech and selecting the intensity of the background to match that of the pixel which is behind it. The process was actually simpler than the random character mapping, but maybe that is because I had solved random mapping already. The processor code is under [Text2Img.py](Text2Img.py). I also wrote a few scripts to zoom in on the detail for the output video. 

## VIDEO HERE