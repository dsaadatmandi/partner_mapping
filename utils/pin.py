# Sets up a custom marker for location pins

from svgpath2mpl import parse_path
import matplotlib as mpl

class LocationPin():
    def __init__(self):
        self.pin_raw = parse_path("M12 0c-4.198 0-8 3.403-8 7.602 0 4.198 3.469 9.21 8 16.398 4.531-7.188 8-12.2 8-16.398 0-4.199-3.801-7.602-8-7.602zm0 11c-1.657 0-3-1.343-3-3s1.343-3 3-3 3 1.343 3 3-1.343 3-3 3z")
        self.pin = self.setup_pin()

    def setup_pin(self):
        self.pin_raw.vertices -= self.pin_raw.vertices.mean(axis=0)
        return self.pin_raw.transformed(mpl.transforms.Affine2D().rotate_deg(180))