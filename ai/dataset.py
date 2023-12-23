from PIL import Image


# image padding to prevent distortion of image
class Padding(object):
    def __init__(self, fill):
        self.fill = fill

    def __call__(self, src):
        w, h = src.size

        if w == h:
            return src
        elif w > h:
            out = Image.new(src.mode, (w, w), self.fill)
            out.paste(src, (0, (w - h) // 2))
            return out
        else:
            out = Image.new(src.mode, (h, h), self.fill)
            out.paste(src, ((h - w) // 2, 0))
            return out
