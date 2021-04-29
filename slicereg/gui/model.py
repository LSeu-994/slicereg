from dataclasses import dataclass, field
from typing import Tuple, Optional, List

from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider


@dataclass
class AppModel:
    window_title: str = "bg-slicereg"
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    section_image: Optional[ndarray] = None
    section_transform: Optional[ndarray] = None
    atlas_image: Optional[ndarray] = None
    atlas_volume: Optional[ndarray] = None
    highlighted_image_coords: Optional[Tuple[int, int]] = None
    highlighted_physical_coords: Optional[Tuple[float, float, float]] = None
    bgatlas_names: List[str] = field(default_factory=list)
    updated: Signal = field(default_factory=Signal)

    def update(self, **attrs):
        print(attrs)
        for attr, value in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise TypeError(f"Cannot set {attr}, {self.__class__.__name__} has no {attr} attribute.")
        self.updated.emit()

    def on_section_loaded(self, image: ndarray, atlas_image: ndarray, transform: ndarray, resolution_um: int) -> None:
        self.update(section_image=image, atlas_image=atlas_image, section_transform=transform)

    def on_channel_select(self, image: ndarray, channel: int) -> None:
        self.update(section_image=image)

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray,
                             atlas_image: ndarray) -> None:
        self.update(section_image=section_image, atlas_image=atlas_image, section_transform=transform)

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray) -> None:
        self.update(atlas_image=atlas_slice_image, section_transform=transform)

    def on_atlas_update(self, volume: ndarray, transform: ndarray) -> None:
        self.update(atlas_volume=volume)

    def on_bgatlas_list_update(self, atlas_names: List[str]) -> None:
        self.update(bgatlas_names=atlas_names)

    def on_image_coordinate_highlighted(self, image_coords, atlas_coords) -> None:
        self.update(highlighted_image_coords=image_coords, highlighted_physical_coords=atlas_coords)