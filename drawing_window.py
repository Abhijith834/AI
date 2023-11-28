# drawing_window.py
import cv2
import numpy as np

class DrawingWindow:
    def __init__(self, width, height):
        self.canvas = 255 * (np.ones((height, width, 3), np.uint8))
        self.thumb_circle_radius = 15
        self.thumb_position = (width // 2, height // 2)
        self.prev_thumb_position = None

    def update_canvas(self, tracked_path_index, tracked_path_middle):
        # Draw white lines (thumb and middle)
        for i in range(1, len(tracked_path_middle)):
            cv2.line(self.canvas, tracked_path_middle[i - 1], tracked_path_middle[i], (255, 255, 255), 3)

        # Draw black lines (thumb and index) only if a white line is not being created
        if not tracked_path_middle:
            for i in range(1, len(tracked_path_index)):
                cv2.line(self.canvas, tracked_path_index[i - 1], tracked_path_index[i], (0, 0, 0), 3)

        # Draw a circle at the latest thumb position
        cv2.circle(self.canvas, self.thumb_position, self.thumb_circle_radius, (0, 255, 0), -1)

        # Clear the previous thumb circle if a new circle is drawn
        if self.prev_thumb_position and self.prev_thumb_position != self.thumb_position:
            cv2.circle(self.canvas, self.prev_thumb_position, self.thumb_circle_radius, (255, 255, 255), -1)

        # Update previous thumb position
        self.prev_thumb_position = self.thumb_position

    def show_canvas(self):
        cv2.imshow("Canvas", self.canvas)
        print("Canvas updated and displayed.")
