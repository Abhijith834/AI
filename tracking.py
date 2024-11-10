# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:30:18 2023

@author: Abhijith Saji
"""

import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def get_hand_landmarks(self, frame):
        results = self.hands.process(frame)
        return results.multi_hand_landmarks

# You might need additional setup based on your specific requirements
