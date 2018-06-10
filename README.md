# Image Processing and Computer Vision 

A place for my smaller projects & experiments in image processing, computer vision, and computational photography.  

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Anomoly Detection for Watch Faces](/watch_faces)

This project was a proof of concept for a small watch company with the goal of using computer vision to detect errors in the manufacturing process of watches. An image is taken of a watch face and analyzed for errors in its design. These errors can include things like misplaced numbers, unwanted color variations, misalignment of features on the watch etc. My algorithm works by comparing a positive example of a watch pre-determined to be manufactured correctly with the new query watch. The images are aligned with OpenCV's SIFT Detector. Matches are filtered using a custom statistcal model based of a Gaussian Kernel Density Estimation of the SIFT transformation features. A Homography Transform is aligned so all of the watch features should line up, if both watches are identical. If the query watch has errors, they will become immediately visible by comparison. 

Once the two images are aligned, they are normalized and blurred (Gaussian) and subtracted from eachother to visualize the differences. These differences are highlighted for easy localization and detection. Future work of this project includes automation of a pipeline to capture the images and sort the watches. 

In the examples below, the top image shows a watch face with errors, denoted by the highlighted "III" which is missing. The second exmaple is a perfect watch and does not show this error.

#### Watch Face With Errors 
<img src="/watch_faces/img/error.jpg" width="1000" alt="raw" />

#### Watch Face Without Errors
<img src="/watch_faces/img/no_error.jpg" width="1000" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Cell Counting with Hough Circles](/cell_counting)

For my work with the Synethetic Biology Company, Amyris, I built an in-depth pipeline to detect cells on a 96 well-plate agar dish. This was for a project which involved a larger pipeline of cell counting and colony picking with a robot. I included parameters to filter the desired radius size of the cell, the separation of cells within each plate (close-by cells can otherwise be incorrecly grouped as the same colony, even though they have genetic differences. This avoids that). My algorithm was 4 times faster and improved average cell localization accuracy to 93% (previously 79%). It was based on using OpenCV Hough Circles as the shape finding algorithm, with a whole lot of numpy to itemize the well plates and cell ranking. 

<img src="/cell_counting/img/disp.png" width="1000" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Optical Heart Rate Recognition via Webcam](/optical_heart_rate)

This software uses real-time computer vision to measure heart-rate from changes in optical intensity measured via a webcam. This is a sort of ensemble implementation, drawing from software written by others in academia and as a hobby. Specifically, I draw heaviest from the techniques of Ming-Zher Poh et. al., while making the processing lighter weight and more readable. The technique uses feature extraction, Independent Component Analysis (ICA) and a fast fourrier transform to detect heart rate. 

<img src="/optical_heart_rate/img/disp.png" width="900" alt="raw" />
<img src="/optical_heart_rate/img/ICA.png" width="900" alt="raw" />

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

<img src="/background_removal/output.png" width="900" alt="raw" />

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Math Gifs](/math_gifs)

Because math is beautiful. 

<p align="center">
   <img src="/math_gifs/toroid_revolver/toroid_compressed.gif" width="400" alt="raw" />
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Seam Carving](https://github.com/momonala/imaging_and_vision/tree/master/seam_carving)

An experiment with a technique that looks like magic. Content-Aware Image Resizing - a technique invented by Avidan and Shamir from Mitsubishi Electric Research Labs in 2007. 

<p align="center">
    <a href="https://www.youtube.com/watch?v=gIVqbKQdSGs " target="_blank"><img src="/seam_carving/img.png"  alt="_" width="700" border="10" /></a>
</p>
I used python's openCV and scikit image to build a few seam carving algroithms. The first, seam_carving_slider.py, is a tool that allows the user to upload an image and use a trackbar to compress the image as desired. My second algorthim, seam_carving_iter.py is a loop implementation that allows the user to input a percent of the original image to compress into, and save consecutive images as one seam is removed per iteration. My algorithm takes in inputs for direction,  compression ratio and number of seams per iteration. Hardcoded is the energy mapping function, which does Gaussian smoothing and measures the Sobel gradient magnitude in openCV, much faster than scikit. In the loop I recursively carve (scikit) and recompute the energy map which makes the seam cutting more seamless. 

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Layering with Open Source NASA Map Images](/earth_layers)

The code works as a series of transformations and image overlays on Equirectangular maps. I used population data and Earth at Night (lights) data from NASA's image repo, [Visible Earth](https://www.visibleearth.nasa.gov/). You can adjust the parameters of one image to highlight certain aspects of the image data, and overlap images to see how population and light interact.

<p align="center">
    <img src="/earth_layers/earth_layers2.jpg" width="800" alt="Combined Image" />
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Cython Ising Model](/cython_ising)

Following along a tutorial, posting for Cython reference in the future.   

-----------------------------------------------------------------------------------------------------------------------------------------------

## [Image Generator for Machine Learning](/generator)

This is an image generator I built from scratch for an interview with [BrighterAI](https://www.brighter.ai/#!), an deep learning company that uses image augmentation for security and self-driving-cars. The generator has a basic version plus a version for GPU support and image augmentation. 