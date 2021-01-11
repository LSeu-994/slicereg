from src.gui.main_view import MainView
from src.gui.presenters import LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, SelectChannelPresenter
from src.workflows.load_atlas import BrainglobeAtlasRepo, LoadAtlasWorkflow
from src.workflows.load_section import OmeTiffReader, LoadSectionWorkflow
from src.workflows.move_section import MoveSectionWorkflow
from src.workflows.select_channel import SelectChannelWorkflow
from src.workflows.shared.repos.section_repo import InMemorySectionRepo
from src.workflows.provider import WorkflowProvider


def launch_gui():
    win = MainView(title="Registration App")

    workflows = WorkflowProvider(
        load_section=LoadSectionWorkflow(
            repo=InMemorySectionRepo(),
            presenter=LoadSectionPresenter(
                view=win
            ),
            reader=OmeTiffReader()
        ),
        select_channel=SelectChannelWorkflow(
            repo=InMemorySectionRepo(),
            presenter=SelectChannelPresenter(
                view=win
            )
        ),
        load_atlas=LoadAtlasWorkflow(
            repo=BrainglobeAtlasRepo(),
            presenter=LoadAtlasPresenter(
                view=win
            )
        ),
        move_section=MoveSectionWorkflow(
            repo=InMemorySectionRepo(),
            presenter=MoveSectionPresenter(
                view=win
            )
        )
    )
    win.register_workflows(app=workflows)
    win.run()


if __name__ == '__main__':
    launch_gui()
