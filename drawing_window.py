import cv2
import numpy as np
import mediapipe as mp
from tracking import HandTracker
from drawing_window import DrawingWindow
from collections import deque

def calculate_moving_average(positions, new_position, window_size=5):
    # Append new position to the queue and keep only the last 'window_size' elements
    positions.append(new_position)
    if len(positions) > window_size:
        positions.popleft()
    # Calculate the average position
    avg_x = int(sum(pos[0] for pos in positions) / len(positions))
    avg_y = int(sum(pos[1] for pos in positions) / len(positions))
    return (avg_x, avg_y)

def main():
    cap = cv2.VideoCapture(0)  # Adjust the camera index if needed
    width, height = int(cap.get(3)), int(cap.get(4))

    hand_tracker = HandTracker()
    drawing_window = DrawingWindow(width, height)
    
    tracked_path_index = []
    tracked_path_middle = []

    # Buffers to store recent positions for smoothing
    thumb_positions = deque()
    index_positions = deque()
    middle_positions = deque()

    # Parameters for pinch detection
    pinch_distance_threshold = 0.05 * width  # Tunable distance threshold
    smoothing_window_size = 5  # Moving average window for smoothing

    drawing_active = False
    erasing_active = False

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Mirror the frame horizontally

        # Hand tracking and landmark detection
        landmarks = hand_tracker.get_hand_landmarks(frame)
        thumb_position = (width // 2, height // 2)  # Default position

        if landmarks:
            # Get the scaled pixel positions of thumb, index, and middle fingertips
            thumb_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            index_finger_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Calculate smoothed positions
            thumb_position = calculate_moving_average(thumb_positions, (int(thumb_tip.x * width), int(thumb_tip.y * height)), smoothing_window_size)
            index_position = calculate_moving_average(index_positions, (int(index_finger_tip.x * width), int(index_finger_tip.y * height)), smoothing_window_size)
            middle_position = calculate_moving_average(middle_positions, (int(middle_finger_tip.x * width), int(middle_finger_tip.y * height)), smoothing_window_size)

            # Calculate distances between thumb and index, and thumb and middle fingers
            distance_index = np.sqrt((thumb_position[0] - index_position[0]) ** 2 + (thumb_position[1] - index_position[1]) ** 2)
            distance_middle = np.sqrt((thumb_position[0] - middle_position[0]) ** 2 + (thumb_position[1] - middle_position[1]) ** 2)

            # Drawing: Check if thumb-index are close
            if distance_index < pinch_distance_threshold:
                if drawing_window.check_clear_button(thumb_position[0], thumb_position[1]):
                    # Clear the canvas if pinched inside the Clear All button
                    drawing_window.clear_canvas()
                elif drawing_window.check_button_press(thumb_position[0], thumb_position[1]):
                    # Adjust size if pinched inside plus/minus buttons
                    pass
                elif drawing_window.check_color_selection(thumb_position[0], thumb_position[1]):
                    # Change color if pinched on the color picker
                    pass
                else:
                    # Start drawing if not currently drawing
                    if not drawing_active:
                        tracked_path_index = []  # Clear path for a new line
                    drawing_active = True
                    erasing_active = False  # Ensure erasing is inactive
                    drawing_window.is_drawing = True
                    drawing_window.is_erasing = False
                    tracked_path_index.append(index_position)
                    tracked_path_middle = []  # Clear erasing path

            else:
                # Pinch released; reset for new drawing path
                drawing_active = False
                drawing_window.is_drawing = False

            # Erasing: Check if thumb-middle are close
            if distance_middle < pinch_distance_threshold:
                if not erasing_active:
                    tracked_path_middle = []  # Clear path for a new erasing line
                erasing_active = True
                drawing_active = False  # Ensure drawing is inactive
                drawing_window.is_erasing = True
                drawing_window.is_drawing = False
                tracked_path_middle.append(middle_position)
                tracked_path_index = []  # Clear drawing path

            else:
                # Pinch released; reset for new erasing path
                erasing_active = False
                drawing_window.is_erasing = False

        # Update canvas and display
        drawing_window.thumb_position = thumb_position  # Update thumb position
        drawing_window.update_canvas(tracked_path_index, tracked_path_middle)
        drawing_window.show_canvas()

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
