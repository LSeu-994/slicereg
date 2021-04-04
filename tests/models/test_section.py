import numpy as np
import pytest
from hypothesis import strategies as st, given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.image import ImageData
from slicereg.models.section import Section
from slicereg.models.transforms import Image2DTransform, AtlasTransform

sensible_floats = floats(allow_nan=False, allow_infinity=False)



@given(
    i=integers(0, 2), j=integers(0, 3), # Image coordinates
    right=sensible_floats, superior=sensible_floats, anterior=sensible_floats,
    pixel_resolution=floats(min_value=1e-12, allow_nan=False, allow_infinity=False),
)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(i, j, right, superior, anterior, pixel_resolution):
    section = Section(
        image=ImageData(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=pixel_resolution,
        ),
        plane_3d=AtlasTransform(right=right, superior=superior, anterior=anterior),
    )
    x, y, z = section.pos_from_coord(i=i, j=j)  # observed 3D positions
    assert x == approx((j * pixel_resolution) + right)
    assert y == approx((-i * pixel_resolution) + superior)
    assert z == approx(anterior)


@given(
    j=integers(0, 39),  # image coordinates on i-intercept to simplify trig math (e.g. (0, j))
    pixel_resolution=floats(min_value=.0001, max_value=1000, allow_nan=False, allow_infinity=False),
    x_shift=sensible_floats, y_shift=sensible_floats,  # planar shifts
    theta=sensible_floats,  # planar rotations
)
def test_can_get_correct_3d_position_with_image_shifts_and_planar_rotations(j, pixel_resolution, x_shift, y_shift, theta):
    section = Section(
        image=ImageData(channels=arange(2400).reshape(2, 30, 40), pixel_resolution_um=pixel_resolution),
        plane_2d=Image2DTransform(i=x_shift, j=y_shift, theta=theta),
    )
    x, y, z = section.pos_from_coord(i=0, j=j)
    assert x == approx((pixel_resolution) * (j * cos(radians(theta)) + x_shift))
    assert y == approx((pixel_resolution) * (j * sin(radians(theta)) + y_shift))
    assert z == 0



@given(i=st.integers(), j=st.integers())
def test_nonexistent_image_coords_raise_error_and_doesnt_if_exists(i, j):
    section = Section(
        image=ImageData(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
    )
    if i < 0 or i >= section.image.height or j < 0 or j >= section.image.width:
        with pytest.raises(ValueError):
            section.pos_from_coord(i=i, j=j)
    else:
        assert section.pos_from_coord(i=i, j=j)


@given(width=st.integers(2, 1000), height=st.integers(2, 1000))
def test_section_origin_set_sets_shift_to_half_half_and_shift_matrix_to_half_width_height(width, height):
    section = Section(image=ImageData(channels=np.random.random((3, height, width)), pixel_resolution_um=120))
    assert section.plane_2d.i == 0 and section.plane_2d.j == 0
    section2 = section.set_image_origin_to_center()
    res = section2.image.pixel_resolution_um
    height, width = section2.image.height, section2.image.width
    assert section2.plane_2d.i == -0.5 and section2.plane_2d.j == -0.5
    expected_shift_matrix = np.array([
        [res, 0, 0, -res * height / 2],
        [0, res, 0, -res * width / 2],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(section2.shift_matrix, expected_shift_matrix))


def test_resample_section_gets_new_section_with_resampled_image():
    section = Section(image=ImageData(channels=np.random.random((3, 4, 4)), pixel_resolution_um=12))
    section2 = section.resample(resolution_um=24)
    assert isinstance(section2, Section)
    assert section2.image.pixel_resolution_um == 24
    

    