from typing import Optional

from numpy.core._multiarray_umath import ndarray

from src.core.load_atlas.load_atlas import BasePresenter as LAPresenter
from src.core.load_section.load_section import BasePresenter as BLSPresenter
from src.core.section.move_section import BaseMoveSectionPresenter
from src.core.select_channel.select_channel import BasePresenter
from src.gui.window import Window


class Presenter(LAPresenter, BasePresenter, BLSPresenter, BaseMoveSectionPresenter):

    def __init__(self, win: Window):
        self.win = win

    def show_atlas(self, volume: ndarray, transform: ndarray):
        self.win.volume_view.view_atlas(volume=volume, transform=transform)

    def show_error(self, msg: str) -> None:
        self.win.show_temp_title(msg)

    def update_section_image(self, image: ndarray):
        self.win.volume_view.update_image(image=image)
        self.win.slice_view.update_slice_image(image=image)

    def update_section_transform(self, transform: ndarray):
        self.win.volume_view.update_transform(transform=transform)

    def show_section(self, image: ndarray, transform: Optional[ndarray] = None) -> None:
        self.win.volume_view.view_section(image=image, transform=transform)
        self.win.slice_view.update_slice_image(image=image)

    def show_ref_image(self, ref_image: ndarray):
        self.win.slice_view.update_ref_slice_image(image=ref_image)
