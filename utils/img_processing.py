import cv2
from PIL import Image
import PIL.ImageOps   
from rembg import remove


class Masker:
    def __init__(self, design_path, mask_path, destination_path):
        self.design_path = design_path
        self.mask_path = mask_path
        self.destination_path = destination_path

    def run(self):
        self._read_files()
        self._resize_design()
        self._mask()
        # self._remove_bg()
        self._make_transparent()
        self._write_result()

    def _read_files(self):
        self.design = cv2.imread(self.design_path)
        self.mask = cv2.imread(self.mask_path)

    def _resize_design(self):
        self.design = self.design[0 : self.mask.shape[0], 0 : self.mask.shape[1], :]

    def _mask(self):
        self.result = cv2.bitwise_and(self.design, self.mask)

    def _make_transparent(self):
        tmp = cv2.cvtColor(self.result, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp, 10, 255, cv2.THRESH_BINARY)

        b, g, r = cv2.split(self.result)
        rgba = [b,g,r, alpha]
        self.result = cv2.merge(rgba,4)
        
    def _remove_bg(self):
        self.result = remove(self.result)


    def _write_result(self):

        cv2.imwrite(self.destination_path, self.result)


def invert_img(filepath):
    image = Image.open(filepath)
    image = image.convert('L')

    inverted_image = PIL.ImageOps.invert(image)

    inverted_image.save(filepath)