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
    def solve(self, parameters: dict[str,str]) -> list[str]:
        ...

class SchedulerView:
    def __init__(self, options: list[str]) -> None:
        self._scheduler_choice = ft.Dropdown(label='Pick scheduler to simulate',
                                            options=[ft.dropdown.Option(op) for op in options],
                                            on_change=self._change_scheduler)
        
        self._parameter_fields = ft.Column(spacing=2)

        self._parameters = []

        self._given = ft.Column(spacing=2)  

        self._results = ft.Column(spacing=2)       

        self._submit_button = ft.ElevatedButton(text="Solve", on_click=self._solve, icon="forest")     

        self._results_button = ft.ElevatedButton(text="Show results", on_click=self._show_results, icon="forest")     

        self._debug_text = ft.Text()     

        self._saved_results: str

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

        for param in self._parameters:
            if not param.value:
                continue
            parameters[param.label] = param.value

        given, results = self._scheduler_changer.solve(parameters)

        self._saved_results = results

        self._given.controls = [ft.Text(value=given)]
        self._refresh_page()


    def _show_results(self, _: ft.ControlEvent):
        self._results.controls = [ft.Text(value=self._saved_results)]
        self._refresh_page()

    def register_scheduler_changer(self, callback: SchedulerRunner):
        self._scheduler_changer = callback

    def entrypoint(self, page: ft.Page):
        self._page = page
        contents = []

        contents.append(self._scheduler_choice)
        contents.append(self._parameter_fields)
        contents.append(self._results)
        contents.append(self._submit_button)
        if DEBUG_MODE:
            contents.append(self._debug_text)
        contents.append(self._given)
        contents.append(self._results_button)
        contents.append(self._results)

        entries = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, controls = contents)

        page.add(entries)

        self._scheduler_choice.focus()

        self._refresh_page()

    def show_debug_text(self, curr_sched:str):
        self._debug_text.value = f"Scheduler changed to {curr_sched}"
        self._refresh_page()

    def show_parameters(self, params: list[str], text_hints: dict[str,str]):
        content = [ft.TextField(label=param, hint_text=text_hints[param], width=750)
                for param in params]
        self._parameters = content
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

    def solve(self, parameters: dict[str,str]) -> list[str]:
        return self._model.solve(parameters)


def main():
    sched_options = ["Basic", "Lottery", "MLFQ", "Multi-CPU"]
    model = SchedulerModel()
    view = SchedulerView(sched_options)
    controller = SchedulerController(model, view)

    controller.start()

if __name__ == '__main__':
    main()
