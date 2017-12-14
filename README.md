# Making images! 

A place for my smaller projects & experiments in image processing, computer vision, and computational photography.  

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Cell Counting with Hough Circles](/cell_counting)

I built a pretty in depth pipeline to detect cells on a 96 well-plate agar dish. This was for a project at work which involved a larger pipeline of cell counting and colony picking with a robot. My algorithm vastly improved the existing default technique. I included parameters to filter the desired radius size of the cell, the separation of cells within each plate (close-by cells can otherwise be incorrecly grouped as the same colony, even though they have genetic differences. This avoids that), and had an overall higher accuracy at finding cells. It was based on using Hough Circles as the shape finding algorithm, with a whole lot of numpy to itemize the well plates and cell ranking. 

<img src="/cell_counting/img/disp.png" width="1000" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Ascii Characters to Pixels](/ascii_mosaic)

This code is inspired from the [BitsOfCode](https://bitesofcode.wordpress.com/2017/01/19/converting-images-to-ascii-art-part-1/) blog post on converting pixel values of an image to ascii characters. I built a similar processor using my own technique in Python. I also went one step further and created a method to convert specifc text, in my case a speech transcript, to create map pixel intensities to specific text. The results are quite cool! 

<p align="center">
    <img src="/ascii_mosaic/obama/obama_ascii_compressed.gif" width="600" alt="raw" />
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Video Background Removal with Singular Value Decompostion](/background_removal)

This notebook shows the use of Singular Value Decomposition for the purpose of background removal from a survelliance video stream. The project idea originally comes from Rachel Thomas' FastAI course for 
[Computational Linear Algebra - Chapter 3](https://github.com/fastai/numerical-linear-algebra). The dataset comes from the [BMC 2012 Background Models Challenge Dataset](http://bmc.iut-auvergne.com/?page_id=24)

<img src="/background_removal/output.png" width="1000" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Math Gifs](/math_gifs)

Because math is beautiful. 

<p align="center">
   <img src="/math_gifs/toroid_revolver/toroid_compressed.gif" width="400" alt="raw" />
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Layering with Open Source NASA Map Images](/earth_layers)

The code works as a series of transformations and image overlays on Equirectangular maps. I used population data and Earth at Night (lights) data from NASA's image repo, [Visible Earth](https://www.visibleearth.nasa.gov/). You can adjust the parameters of one image to highlight certain aspects of the image data, and overlap images to see how population and light interact.

<p align="center">
    <img src="/earth_layers/earth_layers2.jpg" width="800" alt="Combined Image" />
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Keras Prototype](/keras_prototype)

Built a keras prototype for Keras to copy, paste, and modify for other purposes. Includes CNN architecture, lambda layer preprocessing, optimizers, metrics, losses, visualizations, and tensorboard, mostly so I can copy and paste for later projects :)  

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Generator for Machine Learning](/generator)

This is an image generator I built from scratch for an interview with [BrighterAI](), an deep learning company that uses image augmentation for security and self-driving-cars. The generator has a basic version plus a version for GPU support and image augmentation. 

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Seam Carving](https://github.com/momonala/imaging_and_vision/tree/master/seam_carving)

An experiment with a technique that looks like magic. Content-Aware Image Resizing - a technique invented by Avidan and Shamir from Mitsubishi Electric Research Labs in 2007. 

<p align="center">
    <a href="https://www.youtube.com/watch?v=gIVqbKQdSGs " target="_blank"><img src="/seam_carving/img.png"  alt="_" width="700" border="10" /></a>
</p>
I used python's openCV and scikit image to build a few seam carving algroithms. The first, seam_carving_slider.py, is a tool that allows the user to upload an image and use a trackbar to compress the image as desired. My second algorthim, seam_carving_iter.py is a loop implementation that allows the user to input a percent of the original image to compress into, and save consecutive images as one seam is removed per iteration. My algorithm takes in inputs for direction,  compression ratio and number of seams per iteration. Hardcoded is the energy mapping function, which does Gaussian smoothing and measures the Sobel gradient magnitude in openCV, much faster than scikit. In the loop I recursively carve (scikit) and recompute the energy map which makes the seam cutting more seamless. 