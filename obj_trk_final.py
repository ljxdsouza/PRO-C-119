import cv2
import time
import math

# Goal position
p1 = 530
p2 = 300

# Lists to store the coordinates
xs = []
ys = []

# Capture the video
video = cv2.VideoCapture("footvolleyball.mp4")

# Load the tracker
tracker = cv2.TrackerCSRT_create()

# Read the first frame of the video
success, img = video.read()

# Select the bounding box on the image
bbox = cv2.selectROI("tracking", img, False)

# Initialize the tracker on the img and the bounding box
tracker.init(img, bbox)

def goal_track(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    c1 = x + int(w / 2)
    c2 = y + int(h / 2)
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)

    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)
    dist = math.sqrt(((c1 - p1) ** 2) + (c2 - p2) ** 2)
    print(dist)

    if dist <= 20:
        cv2.putText(img, "Goal", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs) - 1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0, 0, 255), 5)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

while True:
    # Read a new frame
    check, img = video.read()
    if not check:
        break

    # Update the tracker
    success, bbox = tracker.update(img)

    # Check if tracking was successful
    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "LOST", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Call the goal_track function
    goal_track(img, bbox)

    # Display the result
    cv2.imshow("Tracking", img)

    # Exit if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()
