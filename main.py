# Controller
"""
    TODO:
        make parameter boxes into fields
        when solve is called, pass parameter values as list (view to controller)
        parse parameter values to command line syntax
        pass syntax to model
        have model run



"""

import flet as ft
from model import *
from typing import Protocol

DEBUG_MODE = True

class SchedulerRunner(Protocol):
    def change_scheduler(self, new_scheduler: str):
        ...
    def solve(self):
        ...

class SchedulerView:
    def __init__(self, options: list[str]) -> None:
        self._scheduler_choice = ft.Dropdown(label='Pick scheduler to simulate',
                                            options=[ft.dropdown.Option(op) for op in options],
                                            on_change=self._change_scheduler)
        
        self._parameter_fields = ft.Column(spacing=2, scroll=ft.ScrollMode.ALWAYS)

        self._results = ft.Column(spacing=2)       

        self._submit_button = ft.ElevatedButton(text="Elevated button", on_click=self._solve, icon="forest")     

        self._debug_text = ft.Text()     

        self._scheduler_changer: SchedulerRunner

        self._page: ft.Page | None = None

    def _refresh_page(self):    # call every update of page
        if self._page:
            self._page.update()

    def _change_scheduler(self, _: ft.ControlEvent):
        if self._scheduler_choice.value is None:
            return

        new_scheduler = self._scheduler_choice.value
        self._scheduler_changer.change_scheduler(new_scheduler)

        self._scheduler_choice.focus()

    def _solve(self, _: ft.ControlEvent):
        parameters = {}

        for param in self._parameter_fields.controls:
            if param.value != None:
                continue
            parameters[param.label] = param.value

        self._scheduler_changer.solve(parameters)

    def register_scheduler_changer(self, callback: SchedulerRunner):
        self._scheduler_changer = callback

    def entrypoint(self, page: ft.Page):
        self._page = page

        page.add(self._scheduler_choice)
        page.add(self._parameter_fields)
        page.add(self._results)
        page.add(self._submit_button)
        if DEBUG_MODE:
            page.add(self._debug_text)

        self._scheduler_choice.focus()

    def show_debug_text(self, curr_sched:str):
        self._debug_text.value = f"Scheduler changed to {curr_sched}"
        self._refresh_page()

    def show_parameters(self, params: list[str], text_hints: dict[str,str]):
        content = [ft.TextField(label=param, hint_text=text_hints[param], width=750)
                for param in params]
        self._parameter_fields.controls = content
        self._refresh_page()
    
class SchedulerController:
    def __init__(self, model: SchedulerModel, view: SchedulerView):
        self._model = model
        self._view = view

    def start(self):
        self._view.register_scheduler_changer(self)
        ft.app(self._view.entrypoint)

    def change_scheduler(self, new_scheduler: str):
        model = self._model
        view = self._view

        model.change_scheduler(new_scheduler)

        view.show_debug_text(model.current_scheduler)

        view.show_parameters(model.scheduler_parameters, model.param_text_hints)

    def solve(self, parameters: dict[str,str]):
        self._model.solve(parameters)


def main():
    sched_options = ["Basic", "Lottery", "MLFQ", "Multi-CPU"]
    model = SchedulerModel()
    view = SchedulerView(sched_options)
    controller = SchedulerController(model, view)

    controller.start()

if __name__ == '__main__':
    main()
