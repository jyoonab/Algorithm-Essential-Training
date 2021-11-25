import torchvision.transforms as transforms
import torch.utils.data
import numpy as np
from PIL import Image

import time

def get_transform(opt):
    transform_list = []

    osize = [opt.crop_size, opt.crop_size]
    method = Image.BICUBIC
    transform_list.append(transforms.Resize(osize, method))
    transform_list.append(transforms.RandomCrop(opt.crop_size))

    transform_list.append(transforms.Lambda(lambda img: __make_power_2(img, base=4, method=method)))

    transform_list += [transforms.ToTensor()]
    transform_list += [transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]

    print(transforms.Compose(transform_list))

    return transforms.Compose(transform_list)

def __make_power_2(img, base, method=Image.BICUBIC):
    ow, oh = img.size
    h = int(round(oh / base) * base)
    w = int(round(ow / base) * base)
    if h == oh and w == ow:
        return img

    return img.resize((w, h), method)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def tensor2im(input_image, imtype=np.uint8):
    if not isinstance(input_image, np.ndarray):
        if isinstance(input_image, torch.Tensor):  # get the data from a variable
            image_tensor = input_image.data
        else:
            return input_image
        image_numpy = image_tensor[0].clamp(-1.0, 1.0).cpu().detach().numpy()  # convert it into a numpy array
        if image_numpy.shape[0] == 1:  # grayscale to RGB
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0  # post-processing: tranpose and scaling
    else:  # if it is a numpy array, do nothing
        image_numpy = input_image

    return image_numpy.astype(imtype)

'''
def tensor2im(image_tensor, imtype=np.uint8):
    start = time.time()
    image_numpy = image_tensor[0].cpu().float().numpy()
    image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    print("time inside :", time.time() - start)
    return image_numpy.astype(imtype)
'''
