import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips =[8, 12, 16, 20]
thumb_tip= 4
finger_fold_status = []

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)


    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            #acessando os pontos de referência pela sua posição
            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

             #O código vai aqui  
            for tip in finger_tips:
                x, y = int(lm_list[tip].x*w), int(lm_list[tip].y*h)
                cv2.circle(img, (x,y,), 15, (255,0,255), cv2.FILLED)

                print(finger_fold_status)

                if lm_list[tip].x > lm_list[tip-3].x and lm_list[9].x < lm_list[0].x:
                    cv2.circle(img, (x,y), 15, (30, 200, 30), cv2.FILLED)
                    finger_fold_status.append(True)
                elif lm_list[tip].x < lm_list[tip-3].x and lm_list[9].x > lm_list[0].x:
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

                if all(finger_fold_status):
                    if lm_list[thumb_tip].y < lm_list[thumb_tip -1].y < lm_list[thumb_tip -2].y:
                        print("Curtida")
                        cv2.putText(img, "Curtida", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255, 0), 3)
                    if lm_list[thumb_tip].y > lm_list[thumb_tip -1].y > lm_list[thumb_tip -2].y:
                        print("Curtida")
                        cv2.putText(img, "Descurtida", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (80,80, 255), 3)

                finger_fold_status = []


            mp_draw.draw_landmarks(img, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((255,50,50),4,2))
    

    cv2.imshow("detector de maos", img)
    cv2.waitKey(1)