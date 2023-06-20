import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch.nn.functional as F
import cv2
from PIL import Image, ImageEnhance, ImageOps
from PIL import Image
import os

class IncrementNode4Anime_animeStepIndex:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "anime_step":("INT", {
                    "default": 0,
                    "min": 0,
                })
            }
        }
    CATEGORY = "anime"

    RETURN_TYPES = ("CONDITION",)
    FUNCTION = "increment_number"

    def increment_number(self, anime_step):
        # if not hasattr(self, "startIndex"):
        #     self.startIndex = startIndex
        # self.startIndex = self.startIndex + 1
        return ([anime_step],)

class LoadImageNode4Anime:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "index":("CONDITION",),
                "image_path":("STRING",{
                    "default":"",
                    "multiline":True
                }),
                "image_file_matching":("STRING",{
                    "default":"%d.png",
                    "multiline":True
                })
            }
        }
    CATEGORY = "anime"

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image_by_index"

    def load_image_by_index(self, index, image_path, image_file_matching):
        filePath = os.path.join(image_path, (image_file_matching % (index[0])))
        print("读取目标：", filePath)
        
        i = Image.open(filePath)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (image, mask)

# class LoadImages4Anime:
#     @classmethod
#     def INPUT_TYPES(s):
#         input_dir = folder_paths.get_input_directory()
#         files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
#         return {"required":
#                     {"image": (sorted(files), )},
#                 }

#     CATEGORY = "anime/image"

#     RETURN_TYPES = ("IMAGE", "MASK")
#     FUNCTION = "load_image"
#     def load_image(self, image):
#         image_path = folder_paths.get_annotated_filepath(image)
#         i = Image.open(image_path)
#         i = ImageOps.exif_transpose(i)
#         image = i.convert("RGB")
#         image = np.array(image).astype(np.float32) / 255.0
#         image = torch.from_numpy(image)[None,]
#         if 'A' in i.getbands():
#             mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
#             mask = 1. - torch.from_numpy(mask)
#         else:
#             mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
#         return (image, mask)


NODE_CLASS_MAPPINGS = {
    "IncrementNode4Anime_animeStepIndex": IncrementNode4Anime_animeStepIndex,
    "LoadImageNode4Anime": LoadImageNode4Anime,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IncrementNode4Anime_animeStepIndex": "IncrementNode4Anime",
    "LoadImageNode4Anime": "LoadImageNode4Anime",
}