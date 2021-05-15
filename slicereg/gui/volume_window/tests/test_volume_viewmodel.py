from unittest.mock import Mock

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx

from slicereg.app.app_model import AppModel
from slicereg.gui.volume_window import VolumeViewModel
from slicereg.utils import DependencyInjector


@pytest.fixture()
def app_model():
    app_model = AppModel(_injector=Mock(DependencyInjector))
    return app_model


@pytest.fixture()
def view_model(app_model):
    return VolumeViewModel(_model=app_model)


def test_volume_viewmodel_updates_section_transform_when_it_updates_in_the_app(app_model, view_model):
    app_model.section_transform = np.random.random(size=(4, 4))
    npt.assert_almost_equal(app_model.section_transform, view_model.section_transform)


def test_volume_viewmodel_updates_section_clim_when_section_image_updates_in_the_app(app_model, view_model: VolumeViewModel):
    app_model.clim_3d = (0.5, 0.2)
    app_model.section_image = np.random.randint(0, 100, size=(10, 10), dtype=np.uint16)
    assert app_model.clim_3d_values == approx(view_model.clim)


def test_volume_viewmodel_updates_section_clim_when_clim_updates_in_the_app(app_model, view_model: VolumeViewModel):
    app_model.section_image = np.random.randint(0, 100, size=(10, 10), dtype=np.uint16)
    app_model.clim_3d = (0.5, 0.2)
    assert app_model.clim_3d_values == approx(view_model.clim)