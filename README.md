# Invisibility-Cloak
To make an invisibile cloak using a regular colored cloth is the primary goal of this project. We can achieve this by using simple computer vision techniques in OpenCV with the help of image processing techique called Color Detection and Segmentation.
# Working
The project works on the technique of removing the foreground frame from the video. By removing a single predefined color and replacing it with a pre-existing same background which we recorded earlier, we can create the immersion of invisibility cloak.
# Case where it fails
It may fail to give us an invisible cloak when we use a different color cloth rather than the one defined earlier in our code. Like, if we used the red color values in the code but we use green color cloth in the video footage, then it fails to give us an immerson of invisibility.
# Deploying it on Flask
To look how our project works when we use it on a web server, we deploy it on flask.
We make a HTML file in which we create a web page and then we link it with the flask.
