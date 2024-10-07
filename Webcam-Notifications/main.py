import cv2
import time
from emailing import send_email


video = cv2.VideoCapture(0)
time.sleep(1)

# Set var for first frame, which will be used to compare with later frames and
# to determine if there were changes/movement
first_frame = None
status_list = []

while True:
    status = 0
    check, frame = video.read()

    # Convert image to greyscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur is a type of image-blurring technique used in image processing to reduce noise and detail
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Display what's visible on the cam
    #cv2.imshow("My video", gray_frame_gau)

    # A trick to store the first frame only once
    if first_frame is None:
        first_frame = gray_frame_gau

    # Compare frames to detect motion
    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    # A check if object exited the frame
    if status_list[0] == 1 and status_list[1] == 0:
        send_email()


    cv2.imshow("My video", frame)

    # Create key shortcut to quit the program
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

# Release the CPU and mem resources that were allocated for the cam
video.release()