from app.lib.process import *
import cv2
from app.lib.cv.classify import *
from app.lib.cv.facial import *

def cv(filename):
    # loop through frames
    labels = []
    ltimes = []
    people = []
    ptimes = []
    fr = FaceRecognize()

    capture = cv2.VideoCapture(filename)f[]
    first = True
    counter = -1
    while True:
        _, frame = capture.read()
        
        if frame == None: 
            break
        if first:
            cv2.imwrite('app/static/raw/thumb.jpg', frame)
            first = False

        counter += 1

        cv2.imwrite('app/lib/cv/frame.jpg', frame)

        # classification
        classes = classify()
        for cls in classes:
            if cls not in labels:
                labels.append(cls)
                ltimes.append(counter)

        # facial detection
        try: 
            cropped = cv2.resize(frame, (37, 50))
            cropped.resize((1850, 3))
            cropped.resize((1, 1850))
            person = fr.test(cropped)

            if person not in people:
                people.append(person)
                ptimes.append(counter)
        except:
            continue

        Process('rm app/lib/cv/frame.jpg').run()
    capture.release()

    print 'labels', labels
    print 'people', people

    return {
        'objects': [
            {'object': obj, 'time': time}
            for obj, time in zip(labels, ltimes)
        ],
        'people': [
            {'person': per, 'time': time}
            for per, time in zip(people, ptimes)
        ]
    }