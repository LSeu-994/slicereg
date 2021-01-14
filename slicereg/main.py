from PySide2.QtWidgets import QApplication

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.provider import CommandProvider
from slicereg.gui.view_model import ViewModel, LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, \
    SelectChannelPresenter
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.repos.brainglobe_atlas import BrainglobeAtlasRepo
from slicereg.repos.inmemory_section import InMemorySectionRepo


def launch_gui():
    app = QApplication([])

    view_model = ViewModel()
    repo = InMemorySectionRepo()

    commands = CommandProvider(
        load_section=LoadImageCommand(
            repo=repo,
            presenter=LoadSectionPresenter(
                view_model=view_model
            ),
            reader=OmeTiffReader()
        ),
        select_channel=SelectChannelCommand(
            repo=repo,
            presenter=SelectChannelPresenter(
                view_model=view_model
            )
        ),
        load_atlas=LoadAtlasCommand(
            repo=BrainglobeAtlasRepo(),
            presenter=LoadAtlasPresenter(
                view_model=view_model
            )
        ),
        move_section=MoveSectionCommand(
            repo=repo,
            presenter=MoveSectionPresenter(
                view_model=view_model
            )
        )
    )

    volume_view = VolumeView(model=view_model, commands=commands)
    MainWindow(model=view_model, commands=commands, volume_widget=volume_view.qt_widget)
    app.exec_()


if __name__ == '__main__':
    launch_gui()
