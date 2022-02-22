import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture('./b.mp4')
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 100, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)
pTime = 0
cTime = 0


while True:
    ret, img = cap.read()

    if ret:
        thumbX = []
        thumbY = []
        foreFingerY = []
        middleFingerY = []
        ringFingerY = []
        pinkyX = []
        pinkyY = []


        hand = 'None'
        backOfHand = 'None'
        number = [False] * 5

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(imgWidth * lm.x)
                    yPos = int(imgHeight * lm.y)
                    cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 255), 1)

                    if i <= 4 and i >= 0:
                        thumbX.append(xPos)
                        thumbY.append(yPos)
                    elif i <= 8 and i >= 5:
                        foreFingerY.append(yPos)
                    elif i <= 12 and i >= 9:
                        middleFingerY.append(yPos)
                    elif i <= 16 and i >= 13:
                        ringFingerY.append(yPos)
                    elif i <= 20 and i >= 17:
                        pinkyX.append(xPos)
                        pinkyY.append(yPos)

                    # if i == 4:
                    #     cv2.circle(img, (xPos, yPos), 10, (0, 0, 255), cv2.FILLED)
                    
            if len(thumbX) == 10:
                hand = "Two hands"
                if abs(thumbX[3] - thumbX[-2]) > abs(pinkyX[2] - pinkyX[-2]):
                    backOfHand = "Back"
                else:
                    backOfHand = "Calm"               
            else:
                for hand_handedness in result.multi_handedness:
                    # print(hand_handedness.classification[0].label)
                    if hand_handedness.classification[0].label == "Right":
                        hand = "Left"
                        if thumbX[1] < pinkyX[0]:
                            backOfHand = "Calm"
                            if thumbX[4] < thumbX[3] and thumbX[4] < thumbX[2]:
                                number[0] = True
                        else:
                            backOfHand = "Back"
                            if thumbX[4] > thumbX[3] and thumbX[4] > thumbX[2]:
                                number[0] = True
                    else:
                        hand = "Right"
                        if thumbX[1] > pinkyX[0]:
                            backOfHand = "Calm"
                            if thumbX[4] > thumbX[3] and thumbX[4] > thumbX[2]:
                                number[0] = True
                        else:
                            backOfHand = "Back"
                            if thumbX[4] < thumbX[3] and thumbX[4] < thumbX[2]:
                                number[0] = True
                    
                if foreFingerY[3] < foreFingerY[2] and foreFingerY[3] < foreFingerY[1]:
                    number[1] = True
                if middleFingerY[3] < middleFingerY[2] and middleFingerY[3] < middleFingerY[1]:
                    number[2] = True
                if ringFingerY[3] < ringFingerY[2] and ringFingerY[3] < ringFingerY[1]:
                    number[3] = True
                if pinkyY[3] < pinkyY[2] and pinkyY[3] < pinkyY[1]:
                    number[4] = True
                # print(np.std(middleFingerY, ddof=1))

                if number[1] != True and number[2] != True and number[3] != True and number[4] != True and number[0] != True:
                    cv2.putText(img, 'number: '+str(0), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif number[1] and number[2] != True and number[3] != True and number[4] != True and number[0] != True:
                    cv2.putText(img, 'number: '+str(1), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif number[1] and number[2] and number[3] != True and number[4] != True and number[0] != True:
                    cv2.putText(img, 'number: '+str(2), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif number[1] and number[2] and number[3] and number[4] != True and number[0] != True:
                    cv2.putText(img, 'number: '+str(3), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif number[1] and number[2] and number[3] and number[4] and number[0] != True:
                    cv2.putText(img, 'number: '+str(4), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif all(number):
                    cv2.putText(img, 'number: '+str(5), (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                else:
                    cv2.putText(img, 'None', (5,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)

        cTime = time.time()
        fps = int(1 / (cTime-pTime))
        pTime = cTime

        cv2.putText(img, 'FPS: '+str(fps), (5,20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)      
        cv2.putText(img, hand, (5,75), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
        cv2.putText(img, backOfHand, (5,100), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)

        cv2.imshow('video', img)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break
    