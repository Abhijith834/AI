# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:38:02 2023

@author: Abhijith Saji
"""

import cv2
import mediapipe as mp

class TrackingVisualizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def visualize_tracking(self, frame):
        # Mirror the frame horizontally
        frame = cv2.flip(frame, 1)

        results = self.hands.process(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame
