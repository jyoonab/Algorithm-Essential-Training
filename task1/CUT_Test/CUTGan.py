from createModel import create_model
from utility import get_transform, tensor2im
from PIL import Image

import torch.utils.data
import numpy as np
import cv2
import argparse
import json

import time

class CUTGan():
    def __init__(self, target_image):
        '''Create Options'''
        parser = argparse.ArgumentParser()

        with open('option.json', 'r') as f:
            json_data = json.load(f)

        for key in json_data:
            parser.add_argument(key, nargs='?', default=json_data[key])

        self.opt = parser.parse_args()
        self.target_image_path = target_image

        # hard-code some parameters for test
        self.opt.num_threads = 0   # test code only supports num_threads = 1
        self.opt.batch_size = 1    # test code only supports batch_size = 1
        self.opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
        self.opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
        self.opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
        self.opt.crop_size = 512
        self.opt.name = "face2cartoon_v3_CUT"

        print(self.opt.name)

        self.init_model()


    '''initialize model'''
    def init_model(self):
        '''Create Model'''
        self.model = create_model(self.opt)      # create a model given opt.model and other options
        self.transform = get_transform(self.opt)

        init_A_path = './images\\7.png'

        init_A_image = Image.open(init_A_path).convert('RGB')
        init_B_image = Image.open(self.target_image_path).convert('RGB')

        init_A = self.transform(init_A_image)
        init_B = self.transform(init_B_image)

        preprocessed_init_data = torch.utils.data.DataLoader(
            [{'A': init_A, 'B': init_B, 'A_paths': init_A_path, 'B_paths': self.target_image_path}],
            batch_size = self.opt.batch_size,
            shuffle = not self.opt.serial_batches,
            num_workers = int(0),
            drop_last = False,
            )

        for i, data in enumerate(preprocessed_init_data):
            self.model.data_dependent_initialize(data)
            self.model.setup(self.opt)               # regular setup: load and print networks; create schedulers
            self.model.parallelize()


    '''Start Converting Image'''
    def start_converting(self, input_frame):
        '''Preprocess Image'''
        input_frame = cv2.cvtColor(input_frame, cv2.COLOR_RGB2BGR)
        A_image = Image.fromarray(np.uint8(input_frame))
        B_image = Image.open(self.target_image_path).convert('RGB')

        A = self.transform(A_image)
        B = self.transform(B_image)

        preprocessed_data = torch.utils.data.DataLoader(
            [{'A': A, 'B': B, 'A_paths': "", 'B_paths': self.target_image_path}],
            batch_size = self.opt.batch_size,
            shuffle = not self.opt.serial_batches,
            num_workers = int(0),
            drop_last = False,
            )


        '''Start Converting Image'''
        for i, data in enumerate(preprocessed_data):
            self.model.set_input(data)  # unpack data from data loader
            self.model.test()           # run inference

            visuals = self.model.get_current_visuals()  # get image results
            image_result = tensor2im(visuals['fake_B'])

        image_result = cv2.cvtColor(image_result, cv2.COLOR_RGB2BGR)

        return image_result



'''TEST CODE'''
if __name__ == '__main__':
    start = time.time()
    cut = CUTGan('./images\\4.png')
    print("time :", time.time() - start)

    test_image = Image.open('./images\\test.png')
    #test_image_np = np.array(test_image)
    test_image_np = cv2.cvtColor(np.array(test_image), cv2.COLOR_BGR2RGB)

    for i in range(1):
        start = time.time()
        image_result = cut.start_converting(test_image_np)
        cv2.imshow('video', image_result)
        cv2.waitKey(0)
        print("time :", time.time() - start)
