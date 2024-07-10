import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time

# Define colors for boxes and black squares
box_color = (255, 0, 0)  # Red
square_color = (0, 0, 0)  # Black


# Function to detect objects from the screen
def detect_objects():
    # Capture the current screen frame
    image = np.array(ImageGrab.grab(bbox=(0, 0, pyautogui.size().width, pyautogui.size().height)))

    # Convert image to HSV color space for better color-based segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for boxes and black squares
    box_lower = np.array([0, 50, 50])
    box_upper = np.array([10, 255, 255])
    square_lower = np.array([0, 0, 0])
    square_upper = np.array([180, 255, 50])

    # Create masks for boxes and black squares
    box_mask = cv2.inRange(hsv, box_lower, box_upper)
    square_mask = cv2.inRange(hsv, square_lower, square_upper)

    # Find contours (boundaries) of boxes and black squares
    box_contours, _ = cv2.findContours(box_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    square_contours, _ = cv2.findContours(square_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return box_contours, square_contours, image


# Function to move a box towards its target square
def move_box(box, target_square, image):
    try:
        box_moments = cv2.moments(box)
        square_moments = cv2.moments(target_square)

        if box_moments['m00'] == 0 or square_moments['m00'] == 0:
            return

        box_center = np.array([box_moments['m10'] / box_moments['m00'], box_moments['m01'] / box_moments['m00']])
        square_center = np.array(
            [square_moments['m10'] / square_moments['m00'], square_moments['m01'] / square_moments['m00']])
        distance = np.linalg.norm(box_center - square_center)
    except ZeroDivisionError:
        print("Error: Invalid box contour")
        return

    # Move the box towards the target square in small steps
    while distance > 5:
        # Determine direction of movement
        direction = square_center - box_center

        # Calculate movement vector
        movement = direction / distance * 5

        # Update box position
        box_center = box_center + movement

        # Simulate moving the box using pyautogui
        pyautogui.moveTo(box_center[0], box_center[1])
        pyautogui.dragTo(square_center[0], square_center[1], duration=0.5)

        # Calculate updated distance
        distance = np.linalg.norm(box_center - square_center)

        # Draw the moved box on the image
        cv2.drawContours(image, [box.astype(int)], -1, box_color, 2)

        # Show the image
        cv2.imshow('Movement', image)

        # Check for 'K' key press to pause
        if cv2.waitKey(1) & 0xFF == ord('k'):
            return


# Main execution loop
paused = False

while True:
    # Check for 'K' key press to pause or resume
    if cv2.waitKey(1) & 0xFF == ord('k'):
        paused = not paused
        time.sleep(0.2)  # Prevent rapid toggling

    if not paused:
        # Detect boxes and black squares from the screen
        box_contours, square_contours, image = detect_objects()

        # Match boxes to their corresponding black squares
        for box in box_contours:
            closest_square = None
            closest_distance = float('inf')

            for square in square_contours:
                box_moments = cv2.moments(box)
                square_moments = cv2.moments(square)

                if box_moments['m00'] == 0 or square_moments['m00'] == 0:
                    continue

                box_center = np.array(
                    [box_moments['m10'] / box_moments['m00'], box_moments['m01'] / box_moments['m00']])
                square_center = np.array(
                    [square_moments['m10'] / square_moments['m00'], square_moments['m01'] / square_moments['m00']])
                distance = np.linalg.norm(box_center - square_center)

                if distance < closest_distance:
                    closest_square = square
                    closest_distance = distance

            # Move the box towards its matched black square
            if closest_square is not None:
                move_box(box, closest_square, image)

        # Display the current frame
        cv2.imshow('Detection', image)

    # Check for 'Q' key press to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
