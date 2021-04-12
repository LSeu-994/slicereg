from unittest.mock import Mock

import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import AtlasRepo

@pytest.fixture
def repo():
    repo = Mock(AtlasRepo)
    repo.list_available_atlases.return_value = ['awesome_atlas', 'super_atlas']
    return repo


@pytest.fixture
def command(repo):
    return ListBgAtlasesCommand(_repo=repo, atlas_list_updated=Mock(Signal))


@scenario("load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@given("I am connected to the internet")
def step_impl(repo: AtlasRepo):
    assert repo.list_available_atlases()


@when("I check brainglobe")
def step_impl(command: ListBgAtlasesCommand):
    command()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(command: ListBgAtlasesCommand):
    view_model = command.atlas_list_updated.emit.call_args[1]
    assert view_model['atlas_names'] == ['awesome_atlas', 'super_atlas']
