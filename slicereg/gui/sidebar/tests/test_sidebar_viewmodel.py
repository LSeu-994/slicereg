from functools import partial
from unittest.mock import Mock

import pytest
from hypothesis import given
from hypothesis.strategies import floats, text
from pytest import approx

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.utils import DependencyInjector


@pytest.fixture(scope='module')
def app_model():
    app_model = AppModel(_injector=Mock(DependencyInjector))
    return app_model


@pytest.fixture(scope='module')
def view_model(app_model):
    return SidebarViewModel(_model=app_model)


@given(resolution=floats(0.01, 100))
def test_resolution_updated_with_section_text_change(resolution, view_model: SidebarViewModel):
    view_model.section_resolution_text = str(resolution)
    assert view_model._model.section_image_resolution == approx(resolution)


def test_app_updates_with_None_when_viewmode_sets_resolution_to_empty_string(view_model: SidebarViewModel, app_model):
    view_model.section_resolution_text = ''
    assert view_model._model.section_image_resolution is None



@given(resolution=floats(0.01, 100))
def test_viewmodel_resolution_updated_when_app_updates(resolution, view_model: SidebarViewModel, app_model):
    app_model.section_image_resolution = resolution
    if resolution is None:
        assert view_model.section_resolution_text == ''
    else:
        assert view_model.section_resolution_text == str(resolution)


def test_viewmodel_resolution_is_emptry_string_when_app_is_none(view_model: SidebarViewModel, app_model):
    app_model.section_image_resolution = None
    assert view_model.section_resolution_text == ''


@given(text=text(alphabet="abcdefghijklmnopqrstuvwxyzäüö%&/()=?_'\"\\", min_size=1, max_size=10))
def test_viewmodel_resolution_text_does_not_accept_nonnumeric_strings(view_model, text):
    view_model.section_resolution_text = "3.1"
    view_model.section_resolution_text = text
    assert view_model.section_resolution_text == "3.1"



def test_viewmodel_bgatlas_dropdown_fills_with_atlas_names_when_app_gets_them(app_model, view_model: SidebarViewModel):
    atlases = ["atlas1", "mouse_atlas", "rat_atlas2"]
    app_model.bgatlas_names = atlases
    assert view_model.bgatlas_dropdown_entries == atlases
