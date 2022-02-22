import cv2

cap = cv2.VideoCapture('b.mp4')


while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (0, 0), fx=0.8,fy=0.8)
        cv2.imshow('video', frame)
    else:
        break
    if cv2.waitKey(20) == ord('q'):
        break