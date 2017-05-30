# Computational Photography

Experiments and algorithms in computational photography! I am currently taking the Udacity computational photography course offered at Georgia Tech as CS 6475. https://www.udacity.com/course/computational-photography--ud955. Here I will play around with some topics from the course and publish assignments. 

### About the Course: 

This class explores how computation impacts the entire workflow of photography, which is traditionally aimed at capturing light from a 3D scene to form a 2D image. It covers many techniques for image manipulation, mostly rooted in linear algebra. 

## Seam Carving 

My first experiment with a technique that looks like magic. Content-Aware Image Resizing technique was invented by Avidan and Shamir from Mitsubishi Electric Research Labs in 2007. https://www.youtube.com/watch?v=qadw0BRKeMk

I used python's openCV and scikit image to build a few seam carving algroithms. The first, seam_carving_slider.py, is a tool that allows the user to upload an image and use a trackbar to compress the image as desired. My second algorthim, seam_carving_iter.py is a loop implementation that allows the user to input a percent of the original image to compress into, and save consecutive images as one seam is removed per iteration. Though slower, the advantage here is that the algorithm recursively recalculates the energy maps and seams to allow significantly cleaner resizing. 

In both algorithms I wrote my own energy map function that uses a Sobel magnitude gradient paired with minimal smoothing and resizing. The openCV implementation runs much quicker that the scikit image tutorials that are out there. 

