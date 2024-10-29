import imageio.v3
from utils import Log

log = Log("AnimatedGIF")


class AnimatedGIF:
    def __init__(self, image_file_list: list, duration_ms: float = 0.5):
        self.image_file_list = image_file_list
        self.duration_ms = duration_ms

    def save(self, gif_file_name: str):
        imgs = list(map(imageio.v3.imread, self.image_file_list))
        imageio.mimsave(gif_file_name, imgs, duration=self.duration_ms)
        log.info(f"Saved animated gif to {gif_file_name}")
        return gif_file_name
