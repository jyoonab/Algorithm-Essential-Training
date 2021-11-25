import cv2
import numpy as np
import time
import statistics

from datetime import datetime
from CUTGan import CUTGan

def remove_shadow(img):
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    return result

    #cv2.imshow('shadows_out.png', result)
    #cv2.imshow('shadows_out_norm.png', result_norm)

if __name__ == '__main__':
    total_fps = []
    fps_count = 0

    cut_gan = CUTGan('./images\\4.png')
    fgbg = cv2.createBackgroundSubtractorMOG2(128,cv2.THRESH_BINARY,1)

    start = datetime.now()

    cap = cv2.VideoCapture(0)
    while cv2.waitKey(33) < 0:
        '''stop after 10 sec'''
        time_delta = datetime.now() - start
        if time_delta.total_seconds() >= 10:
            break

        ret, frame = cap.read()
        if ret:
            #alpha = 1.0
            #frame = np.clip((1 + alpha) * frame - 128 * alpha, 0, 255).astype(np.uint8)

            #frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)

            #new_frame = remove_shadow(frame)
            #frame = fgbg.apply(frame)

            frame = cv2.resize(frame, dsize=(512, 512), interpolation=cv2.INTER_LINEAR)

            start_time = time.time()
            image_result = cut_gan.start_converting(frame)
            end_time = time.time()
            fps_count += 1
            fps = np.round(1 / np.round(end_time - start_time, 3), 1)
            total_fps.append(fps)

            #print(fps)
            cv2.imshow('video', image_result)
            #cv2.imshow('video_orig', frame)
            #cv2.imshow('video_new', new_frame)
    print(total_fps)
    print('# of Frame', len(total_fps), fps_count)
    print('Average FPS', statistics.mean(total_fps))


    cap.release()
    cv2.destroyAllWindows()
