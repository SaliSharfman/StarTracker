
<img width="637" alt="a1" src="https://user-images.githubusercontent.com/77780368/233840956-c0758212-5e45-4955-8cb2-3860094078f3.png">


# Part 1:

Detect and extract stars from both images using a star detection algorithm such as the Hough Transform or the Harris Corner Detector.
For each detected star in the first image, calculate its feature vector using a feature extraction algorithm such as Scale-Invariant Feature Transform (SIFT) or Speeded Up Robust Features (SURF). The feature vector should capture information about the star's brightness, color, texture, and orientation.
For each detected star in the second image, calculate its feature vector using the same feature extraction algorithm as in step 2.
Use a feature matching algorithm such as the Nearest Neighbor or the Random Sample Consensus (RANSAC) algorithm to match the feature vectors of the stars in both images. The feature matching algorithm should account for differences in brightness, color, and orientation between the two images.
Once all matches have been found, calculate the transformation matrix that maps the coordinates of the matched stars in the second image to the coordinates of the corresponding stars in the first image. This can be done using a method such as the Least-Squares Estimation.
Apply the transformation matrix to the coordinates of all stars in the second image to obtain their new positions in the first image.
Evaluate the accuracy of the matching algorithm by comparing the positions of the stars in the first image to their expected positions based on the database of star positions.

# Part 2:

How to run: <br>
 ``` python .\tracker.py ```

<img src="https://i.imgur.com/1504ZL3.jpg" alt="stars" hight= "800" width="1200"/> 

<img src="https://i.imgur.com/zrrSsIE.png" alt="stars csv" hight= "70" width="280"/>


# Part 3:

How to run: <br>
``` python .\findMatch.py <img1> <img2> ```
 
<img src="https://i.imgur.com/CdCaTPu.jpg" alt="Match" hight= "800" width="1200"/>


# Part 4:
[Assignment summary](https://github.com/SaliSharfman/StarTracker/blob/main/Assignment%20summary.pdf)
