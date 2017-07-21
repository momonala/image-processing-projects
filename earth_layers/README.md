# Earth-Layers
Experiment with openCV and NASA map data 

The code works as a series of transformations and image overlays. You can adjust the parameters of one image to highlight certain aspects of the image data, and overlap images to see how various features interact. I have only tested the image processing with equirectangular views, but it should theoretically work with any type of map data, as long as they are the same type of map projections. See: https://en.wikipedia.org/wiki/List_of_map_projections

I collected the image data from NASA's Visible Earth open source data collection. They've got a mind boggling amount of open satellite images, so go crazy. 

https://visibleearth.nasa.gov/

# To Use: 
1) Use earth_color_change.py to to change the color of your image to highlight features of your image data you want compare. 

2) Use earth_layers.py to overlay the set of images you want to compare features against. Both python files use sliders to control the image processing. 

<img src="https://raw.githubusercontent.com/momonala/imaging_and_vision/master/earth_layers/earth_layers2.jpg" width="480" alt="Combined Image" />

