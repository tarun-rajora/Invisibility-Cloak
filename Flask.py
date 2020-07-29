from flask import Flask, render_template, url_for, Response
import cv2
import time
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    #Accessing the HTML file
    #This will be our home page
    return render_template('index.html')

def gen():
    # Capturing from web cam
    cap = cv2.VideoCapture(0)

    # Preparation for writing the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    # Give the camera time(in seconds) for warming up
    time.sleep(3)
    count = 0
    background = 0

    # Capture the background in range of 60
    # So as to give it some time to capture the background properly
    for i in range(60):
        ret, background = cap.read()
    background = np.flip(background, axis=1)

    # Read every frame from the web cam
    while (cap.isOpened()):
        ret, image = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        count += 1
        image = np.flip(image, axis=1)

        # Convert the image from BGR to HSV for better detection of red color
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Ranges should be carefully chosen
        # Setting the lower and upper range of mask1
        lower_red = np.array([0, 120, 50])
        upper_red = np.array([10, 255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Setting the lower and upper range of mask2
        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        mask1 = mask1 + mask2

        # Mask refinement corresponding to the detected red color
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        # Create an inverted mask to segment out the red color from the frame
        mask2 = cv2.bitwise_not(mask1)

        # Segment the red color part out of the frame using bitwise and with the inverted mask
        res1 = cv2.bitwise_and(image, image, mask=mask2)

        # Create image showing static background frame pixels only for the masked region
        res2 = cv2.bitwise_and(background, background, mask=mask1)

        # Generating the final output
        finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
        output.write(finalOutput)
        cv2.imshow("magic", finalOutput)
        cv2.waitKey(1)

    # Release the capture at the last
    cap.release()
    output.release()
    cv2.destroyAllWindows()
    
        
        
@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True) 

