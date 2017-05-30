# Computational Photography

Experiments and algorithms in computational photography. I am currently taking the Udacity computation photography course offered at Georgia Tech as CS 6475. https://www.udacity.com/course/computational-photography--ud955. Here I will play around with some topics from the course and publish and assignments. 

### About the Course: 

This class explores how computation impacts the entire workflow of photography, which is traditionally aimed at capturing light from a 3D scene to form a 2D image. Topics include the relationship between pictorial techniques and the human visual system; intrinsic limitations of 2D representations and their possible compensations; and technical issues involving capturing light to form images. Technical aspects of image capture and rendering, and exploration of how such a medium can be used to its maximum potential, will be examined.

## Seam Carving 

My first experiment with a technique that looks like magic. I used python's openCV and scikit image to build a few seam carving algroithms. The first, seam_carving_slider.py, is a tool that allows the user to upload an image and use a trackbar to compress the image as desired, using the Content-Aware Image Resizing technique. The technique was famounsly invented by Avidan and Shamir from Mitsubishi Electric Research Labs in 2007. My second algorthim, seam_carving_iter.py is a loop implementation that allows the user to input a percent of the original image to compress into, and save consecutive images as one seam is removed per iteration. The advatnage here is that the algorithm recursively recalculates the energy maps and seams to allow more seamless compression. 

In both algorithms I wrote my own energy map function that uses a Sobel magnitude gradient paired with minimal smoothing and resizing. The openCV implementation runs much quicker that the scikit image tutorials that are out there. 

