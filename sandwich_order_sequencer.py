"""
    This library is intended to solve the Sandwich problem outlined by Agrimetrics.
    Assumptions:
        - There is only one type of sandwich.
        - Sandwiches are made one at a time.
        - Priority is given to whoever ordered first.
        - The orders cannot be canceled after being placed.
        - The timezone is local to where the application is run.
        - A break does not have a defined limit but must be at least a second.
        - Time is measured in minutes/seconds, hours are not used.

    Tested with python version: 3.8.3

    @Author: Adam Cripps
"""
from datetime import datetime, timedelta
from functools import wraps


class SandwichShopScheduler:
    """Schedules the workload of a sandwich shop employee."""

    SEC_TO_MAKE_SANDWICH: int = 150
    SEC_TO_SERVE_SANDWICH: int = 60

    version = "1.1"

    def __init__(self):
        self.start_time = datetime.now().replace(microsecond=0)
        self.orders = []
        self.previous_task_finish_time = None
        self.sequence_number = 0

    def action(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.sequence_number +=1
            func(self, *args, **kwargs)
        return wrapper

    def add_order(self) -> None:
        self.orders.append(datetime.now().replace(microsecond=0))
        self.print_schedule()

    def print_schedule(self) -> None:
        self.reset_day()

        for index, order in enumerate(self.orders):
            self.maybe_take_break(next_order=order)

            order_number = index + 1
            self.make_sandwich(order_number=order_number)
            self.serve_sandwich(order_number=order_number)
        else:
            self.finish_day()

    def maybe_take_break(self, next_order: datetime) -> None:
        if next_order > self.previous_task_finish_time:
            self.take_break(next_order)

    def recalculate_previous_task_finish_time(self, seconds_to_complete: int) -> None:
        self.previous_task_finish_time = self.previous_task_finish_time + timedelta(seconds=seconds_to_complete)

    @action
    def take_break(self, next_order) -> None:
        self.print_action(sequence_number=self.sequence_number,
                              time=self.previous_task_finish_time,
                              action='Take a break.')

        # A break finishes when the next order comes in.
        self.previous_task_finish_time = next_order
        
    @action
    def make_sandwich(self, order_number: int) -> None:
        self.print_action(sequence_number=self.sequence_number,
                          time=self.previous_task_finish_time,
                          action='Make Sandwich',
                          order_number=order_number)

        self.recalculate_previous_task_finish_time(seconds_to_complete=self.SEC_TO_MAKE_SANDWICH)

    @action
    def serve_sandwich(self, order_number: int) -> None:
        self.print_action(sequence_number=self.sequence_number,
                          time=self.previous_task_finish_time,
                          action='Serve Sandwich',
                          order_number=order_number)

        self.recalculate_previous_task_finish_time(seconds_to_complete=self.SEC_TO_SERVE_SANDWICH)

    @action
    def finish_day(self) -> None:
        self.print_action(sequence_number=self.sequence_number,
                          time=self.previous_task_finish_time, action='Take a break.')
        print()

    def reset_day(self) -> None:
        self.previous_task_finish_time = self.start_time
        self.sequence_number = 0

    @staticmethod
    def print_action(sequence_number: int, time: datetime, action: str, order_number: int = None) -> None:
        order_num = str(order_number) if order_number is not None else ''
        print(f' {sequence_number}. {time.strftime("%M:%S")} {action} {order_num}')


if __name__ == '__main__':
    print('This library is not intended to be run as main.')
