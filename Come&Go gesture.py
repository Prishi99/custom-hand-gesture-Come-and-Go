import cv2
import mediapipe as mp
import pyautogui

x1 = y1 = x2 = y2 = x3 = y3 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    ret, image = webcam.read()
    if not ret:
        continue

    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 12:
                    cv2.circle(img=image, center=(x, y), radius=5, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=5, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
                if id == 0:
                    cv2.circle(img=image, center=(x, y), radius=5, color=(0, 0, 255), thickness=3)
                    x3 = x
                    y3 = y

        dist1 = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5 // 4
        dist2 = ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5 // 4
        cv2.line(image, (x1, y1), (x3, y3), (0, 255, 0), 5)
        cv2.line(image, (x2, y2), (x3, y3), (0, 255, 0), 5)

        if dist1 < 30 and dist2 < 30:
            text = "come"
        else:
            text = "go"
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Hand volume control using python", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
