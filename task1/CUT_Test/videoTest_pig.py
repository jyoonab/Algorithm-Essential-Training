import cv2
import numpy as np
import time
import mediapipe as mp

from CUTGan import CUTGan
from math import hypot

nose_image = cv2.imread("pig_nose.png")

class FaceDetector_v1:
    def __init__(self) -> None:
        super(FaceDetector_v1, self).__init__()
        self.model_name: str = 'Face Detection through mediapipe'
        self.model_version: str = '1.0.0'
        self.model_description: str = 'Face Detection through mediapipe'

        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh()
        self.model_status = bool(True)

    def get_facial_landmarks(self, input_frame: np.ndarray) -> np.ndarray:
        input_frame: np.ndarray = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
        inference_result: object = self.face_mesh.process(input_frame)

        if inference_result.multi_face_landmarks:
            landmarks_list = list()
            for facial_landmarks in inference_result.multi_face_landmarks:
                for index in range(0, 468):
                    landmark_point: mp.framework = facial_landmarks.landmark[index]
                    x, y = int(landmark_point.x * input_frame.shape[1]), int(landmark_point.y * input_frame.shape[0])
                    landmarks_list.append([x, y])

            del inference_result  # memory free
            return np.array(landmarks_list, np.int32)
        else:
            return None

if __name__ == '__main__':
    '''Preload Pig Nose'''
    nose_image = cv2.imread("pig_nose.png")
    nose_image = cv2.cvtColor(nose_image, cv2.COLOR_RGB2BGR)

    face_detector = FaceDetector_v1()
    cut_gan = CUTGan('./images\\4.png')

    cap = cv2.VideoCapture(0)
    while cv2.waitKey(33) < 0:
        success, frame = cap.read()
        if success:
            ''' Pre-setting '''
            start_time = time.time()
            frame = cv2.resize(frame, dsize=(512, 512), interpolation=cv2.INTER_LINEAR)
            face_extracted_frame: np.ndarray = frame.copy()
            frame_height, frame_width, frame_channel = frame.shape
            frame.flags.writeable = False

            ''' Get Face-Landmarks '''
            landmarks = face_detector.get_facial_landmarks(frame)
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if landmarks is not None:
                print('center', landmarks[0], 'top', landmarks[4], 'left', landmarks[114], 'right', landmarks[343])

                ''' Calc Nose Shape '''
                top_nose = landmarks[0]
                center_nose = landmarks[4]
                left_nose = landmarks[114]
                right_nose = landmarks[343]

                nose_width = int(hypot(left_nose[0] - right_nose[0],
                                   left_nose[1] - right_nose[1]) * 1.7)
                nose_height = int(nose_width * 0.77)

                top_left = (int(center_nose[0] - nose_width / 2),
                                      int(center_nose[1] - nose_height / 2))
                bottom_right = (int(center_nose[0] + nose_width / 2),
                               int(center_nose[1] + nose_height / 2))

                ''' Pig Nose '''
                nose_pig = cv2.resize(nose_image, (nose_width, nose_height))
                nose_pig_gray = cv2.cvtColor(nose_pig, cv2.COLOR_BGR2GRAY)
                _, nose_mask = cv2.threshold(nose_pig_gray, 25, 255, cv2.THRESH_BINARY_INV)

                nose_area = frame[top_left[1]: top_left[1] + nose_height,
                            top_left[0]: top_left[0] + nose_width]
                nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
                final_nose = cv2.add(nose_area_no_nose, nose_pig)

                frame[top_left[1]: top_left[1] + nose_height,
                            top_left[0]: top_left[0] + nose_width] = final_nose

                convex_hull = cv2.convexHull(landmarks)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                ''' Extract the face '''
                mask = np.zeros((512, 512), np.uint8)
                cv2.fillConvexPoly(mask, convex_hull, 255, lineType=cv2.LINE_AA)
                face_extracted_frame: np.ndarray = cv2.bitwise_and(face_extracted_frame, face_extracted_frame, mask=mask)

                ''' start cartoonizing '''
                toonified_frame = cut_gan.start_converting(frame)

                background_mask = cv2.bitwise_not(mask)
                background = cv2.bitwise_and(frame, frame, mask=background_mask)

                #result_frame = cv2.add(background, toonified_frame)
                result_frame = frame
                #alpha = 0.3
                #result_frame = cv2.addWeighted(background, alpha, toonified_frame, (1-alpha), 0)
                #result_frame = frame

            else:
                print("No Face Found")
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result_frame = frame

            end_time = time.time()
            fps = np.round(1 / np.round(end_time - start_time, 3), 1)

            print(fps)
            cv2.imshow('video', result_frame)
    cap.release()
    cv2.destroyAllWindows()
