Air Canvas
This program is real-time grawing canvas that lets you draw just using hand movements and gestures. You can draw, erase and change colors.

Features
**Draw with Pinch Gestures: Pinch your thumb and index finger to draw lines on the canvas.
**Erase with Pinch Gestures: Pinch your thumb and middle finger to erase parts of the drawing.
**Color Selection: Choose from a set of colors by selecting from the on-screen color picker with a pinch gesture.
**Adjust Brush Size: Increase or decrease the brush size with on-screen + and - buttons.
**Clear Canvas: Use a dedicated button to clear the canvas entirely.

Customization
Tuning Pinch Detection
You can adjust the pinch detection sensitivity by modifying the pinch_distance_threshold in main.py. Increasing this value makes pinch detection more sensitive, while decreasing it requires closer pinching for detection.

Changing Color Picker Colors
To change the colors available in the color picker, modify the self.colors list in drawing_window.py.

Troubleshooting
Lag or Delayed Detection: Lower the smoothing_window_size value in main.py if the gesture detection feels delayed.
Pinch Not Detected Consistently: Adjust the pinch_distance_threshold in main.py to increase or decrease the sensitivity of pinch detection.
