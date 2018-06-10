import cv2
import time
from glob import glob
import sys
import keyboard
from Detector import WatchErrorDetector

# cmd line args: {folder, pos img index, neg img index}
folder = sys.argv[1]
p = int(sys.argv[2])
n = int(sys.argv[3])

# for writing text to OpenCV images
text_params = {
    'fontFace': cv2.FONT_HERSHEY_SIMPLEX,
    'org': (80, 150),
    'fontScale': 2,
    'thickness': 3,
    }

# grab the images to query
positives = glob('Sample {}/G/*'.format(folder))
negatives = glob('Sample {}/NG/*'.format(folder))
pos_img, neg_img = positives[p], negatives[n]
print('Comparing images: {} --VS-- {}'.format(pos_img, neg_img))

# perform image alignment
print('Performing Image Alignment with SIFT...')
Detector = WatchErrorDetector(pos_img, neg_img, debug=False, n_stds=0.7)
Detector.align_query_image()
img = {True: Detector.pos_img_align, False: Detector.neg_img}

# create a named window for displaying
window_name = 'image comparison'
cv2.namedWindow(window_name, 960)

status = True
while True:
    status = True if keyboard.is_pressed('a') else status
    status = False if keyboard.is_pressed('s') else status
    msg = 'Positive Image' if status else 'Query Image'
    color = (0, 255, 0) if status else (0, 0, 255)

    image = cv2.putText(img[status], msg, color=color, **text_params) 
    cv2.imshow(window_name, image)

    # exit gracefully
    if cv2.waitKey(1) & 0xFF == ord('\x1b'):
        break
