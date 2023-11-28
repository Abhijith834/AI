# main.py
import cv2
import numpy as np
import mediapipe as mp
from tracking import HandTracker
from drawing_window import DrawingWindow

def main():
    cap = cv2.VideoCapture(0)  # Adjust the camera index if needed
    width, height = int(cap.get(3)), int(cap.get(4))

    hand_tracker = HandTracker()
    drawing_window = DrawingWindow(width, height)
    
    tracked_path_index = []
    tracked_path_middle = []

    drawing_black_line = False

    while True:
        ret, frame = cap.read()

        # Mirror the frame horizontally
        frame = cv2.flip(frame, 1)

        # Hand tracking
        landmarks = hand_tracker.get_hand_landmarks(frame)

        # Check if thumb is detected
        thumb_position = (width // 2, height // 2)  # Reset to default position

        if landmarks:
            thumb_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            thumb_position = (int(thumb_tip.x * width), int(thumb_tip.y * height))

            # Check if thumb and index or middle fingers are touching
            index_finger_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = landmarks[0].landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]

            distance_threshold = 0.05  # Adjust as needed

            # Check thumb and index fingers
            distance_index = np.sqrt((thumb_tip.x - index_finger_tip.x)**2 + (thumb_tip.y - index_finger_tip.y)**2)
            if distance_index < distance_threshold:
                # Check if it's a new touch
                if not drawing_black_line:
                    tracked_path_index = []  # Start a new black line
                    drawing_black_line = True

                tracked_path_index.append((int(index_finger_tip.x * width), int(index_finger_tip.y * height)))

                # Reset tracked_path_middle if thumb and index are touching
                tracked_path_middle = []

            else:
                drawing_black_line = False

            # Check thumb and middle fingers
            distance_middle = np.sqrt((thumb_tip.x - middle_finger_tip.x)**2 + (thumb_tip.y - middle_finger_tip.y)**2)
            if distance_middle < distance_threshold:
                tracked_path_middle.append((int(middle_finger_tip.x * width), int(middle_finger_tip.y * height)))

                # Reset tracked_path_index if thumb and middle are touching
                tracked_path_index = []

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
