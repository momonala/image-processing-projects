# Images! 

Experiments and algorithms in image processing, computer vision, and computational photography! Projects inspired by personal curiosity, classes, and the Udacity's courses in [Ariticial Intelligence](https://www.udacity.com/course/artificial-intelligence-nanodegree--nd889) and [Computational Photography](https://www.udacity.com/course/computational-photography--ud955) offered at Georgia Tech as CS 6475. 

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Cell Counting with Hough Circles](/cell_counting)

I built a pretty in depth pipeline to detect cells on a 96 well-plate agar dish. This was for a project at work which involved a larger pipeline of cell counting and colony picking with a robot. My algorithm vastly improved the existing default technique. I included parameters to filter the desired radius size of the cell, the separation of cells within each plate (close-by cells can otherwise be incorrecly grouped as the same colony, even though they have genetic differences. This avoids that), and had an overall higher accuracy at finding cells. It was based on using Hough Circles as the shape finding algorithm, with a whole lot of numpy to itemize the well plates and cell ranking. 

<img src="/cell_counting/img/disp.png" width="1000" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Layering with Open Source NASA Map Images](/earth_layers)

The code works as a series of transformations and image overlays on Equirectangular maps. I used population data and Earth at Night (lights) data from NASA's image repo, [Visible Earth](https://www.visibleearth.nasa.gov/). You can adjust the parameters of one image to highlight certain aspects of the image data, and overlap images to see how population and light interact.

<img src="/earth_layers/earth_layers2.jpg" width="800" alt="Combined Image" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Keras Prototype](/keras_prototype)

Built a keras prototype for Keras to copy, paste, and modify for other purposes. Includes CNN architecture, lambda layer preprocessing, optimizers, metrics, losses, visualizations, and tensorboard. 

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Generator for Machine Learning](/generator)

This is an image generator I built from scratch for an interview with [BrighterAI](), an deep learning company that uses image augmentation for security and self-driving-cars. The generator has a basic version plus a version for GPU support and image augmentation. 

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Seam Carving](https://github.com/momonala/imaging_and_vision/tree/master/seam_carving)

My first experiment with a technique that looks like magic. Content-Aware Image Resizing technique was invented by Avidan and Shamir from Mitsubishi Electric Research Labs in 2007. 

<a href="https://www.youtube.com/watch?v=gIVqbKQdSGs " target="_blank"><img src="/seam_carving/img.png"  alt="_" width="700" border="10" /></a>

I used python's openCV and scikit image to build a few seam carving algroithms. The first, seam_carving_slider.py, is a tool that allows the user to upload an image and use a trackbar to compress the image as desired. My second algorthim, seam_carving_iter.py is a loop implementation that allows the user to input a percent of the original image to compress into, and save consecutive images as one seam is removed per iteration. My algorithm takes in inputs for direction,  compression ratio and number of seams per iteration. Hardcoded is the energy mapping function, which does Gaussian smoothing and measures the Sobel gradient magnitude in openCV, much faster than scikit. In the loop I recursively carve (scikit) and recompute the energy map which makes the seam cutting more seamless. 