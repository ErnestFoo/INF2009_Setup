#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Read the first two frames for initial processing (frame1, frame2)
_, frame1 = cap.read()
_, frame2 = cap.read()

while True:
    # Calculate the absolute difference between the two frames
    # This function highlights changes between two frames, which is key in detecting movement.
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference image to grayscale for better processing
    # Grayscale reduces complexity, making it easier to detect changes in intensity.
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth the image and reduce noise
    # Gaussian blur helps to reduce small, irrelevant details that could be falsely detected as movement.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to highlight the areas with significant changes (movement)
    # This function converts the grayscale image to binary, where white pixels represent movement.
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the binary image to fill in gaps in detected movement
    # This function helps to make sure that small movement is also detected by enlarging contours.
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours of the areas with changes (movement)
    # Contours help to outline the regions where movement occurred, making it possible to highlight the movement.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and highlight significant movement
    for contour in contours:
        # Get the bounding rectangle around each detected contour
        (x, y, w, h) = cv2.boundingRect(contour)

        # Filter out small contours (unwanted noise) based on contour area
        # This condition helps eliminate false positives by ignoring small, irrelevant movements.
        if cv2.contourArea(contour) < 900:
            continue

        # Draw rectangles around detected movement areas
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Label the detected movement on the frame
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    # Display the current frame with movement rectangles
    cv2.imshow("feed", frame1)

    # Shift frames for next loop (frame1 becomes frame2, new frame is captured)
    frame1 = frame2
    _, frame2 = cap.read()

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(40) == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

