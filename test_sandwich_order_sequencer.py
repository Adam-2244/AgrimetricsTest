"""
    Sandwich Sequencer task tests.

    @Author: Adam Cripps
"""
from datetime import datetime, timedelta
from freezegun import freeze_time
from sandwich_order_sequencer import SandwichShopScheduler


class TestSandwichShopScheduler:

    MAKE_SANDWICH_ACTION = 'Make Sandwich'
    SERVE_SANDWICH_ACTION = 'Serve Sandwich'
    TAKE_BREAK_ACTION = 'Take a break.'

    def setup_method(self):
        self.scheduler = SandwichShopScheduler()

    def test_print_action(self, capsys):
        seq_num = 5
        order_num = 10
        action = "do something"
        time = datetime.now()

        # With order_num
        self.scheduler.print_action(seq_num, time, action, order_num)

        captured = capsys.readouterr()
        assert captured.out == f' {seq_num}. {time.strftime("%M:%S")} {action} {order_num}\n'

        # Without order_num
        self.scheduler.print_action(seq_num, time, action)

        captured = capsys.readouterr()
        assert captured.out == f' {seq_num}. {time.strftime("%M:%S")} {action} \n'

    def test_finish_day(self, capsys):
        expected_seq_num = self.scheduler.sequence_number + 1
        prev_task_finish_time = self.scheduler.previous_task_finish_time

        self.scheduler.finish_day()

        captured = capsys.readouterr()
        assert captured.out == f' {expected_seq_num}. {prev_task_finish_time.strftime("%M:%S")} {self.TAKE_BREAK_ACTION} \n\n'
        assert self.scheduler.sequence_number == expected_seq_num

    def test_make_sandwich(self, capsys):
        order_num = 10
        expected_seq_num = self.scheduler.sequence_number + 1
        prev_task_finish_time = self.scheduler.previous_task_finish_time

        self.scheduler.make_sandwich(order_number=order_num)
        captured = capsys.readouterr()

        assert captured.out == f' {expected_seq_num}. {prev_task_finish_time.strftime("%M:%S")} {self.MAKE_SANDWICH_ACTION} {order_num}\n'
        assert self.scheduler.sequence_number == expected_seq_num
        assert self.scheduler.previous_task_finish_time == \
               prev_task_finish_time + timedelta(seconds=self.scheduler.SEC_TO_MAKE_SANDWICH)

    def test_serve_sandwich(self, capsys):
        order_num = 10
        expected_seq_num = self.scheduler.sequence_number + 1
        prev_task_finish_time = self.scheduler.previous_task_finish_time

        self.scheduler.serve_sandwich(order_number=order_num)
        captured = capsys.readouterr()

        assert captured.out == f' {expected_seq_num}. {prev_task_finish_time.strftime("%M:%S")} {self.SERVE_SANDWICH_ACTION} {order_num}\n'
        assert self.scheduler.sequence_number == expected_seq_num
        assert self.scheduler.previous_task_finish_time == \
               prev_task_finish_time + timedelta(seconds=self.scheduler.SEC_TO_SERVE_SANDWICH)

    def test_take_break(self, capsys):
        expected_seq_num = self.scheduler.sequence_number + 1
        next_order = datetime.now()
        prev_task_finish_time = self.scheduler.previous_task_finish_time

        self.scheduler.take_break(next_order=next_order)
        captured = capsys.readouterr()

        assert captured.out == f' {expected_seq_num}. {prev_task_finish_time.strftime("%M:%S")} {self.TAKE_BREAK_ACTION} \n'
        assert self.scheduler.sequence_number == expected_seq_num
        assert self.scheduler.previous_task_finish_time == next_order

    def test_reset_schedule(self):
        start_time = self.scheduler.start_time
        self.scheduler.previous_task_finish_time = datetime.now() + timedelta(seconds=100)
        self.scheduler.sequence_number = 1000

        self.scheduler.reset_schedule()

        assert self.scheduler.sequence_number == 0
        assert self.scheduler.previous_task_finish_time == start_time

    def test_recalculate_previous_task_finish_time(self):
        now = datetime.now()
        self.scheduler.previous_task_finish_time = now
        seconds_to_complete = 10

        self.scheduler.recalculate_previous_task_finish_time(seconds_to_complete=seconds_to_complete)

        assert self.scheduler.previous_task_finish_time == now + timedelta(seconds=seconds_to_complete)

    def test_maybe_take_break(self, capsys):
        next_order = self.scheduler.start_time
        init_seq_num = self.scheduler.sequence_number

        # Should not take break if time is the same as previous task finish time.
        self.scheduler.maybe_take_break(next_order)
        captured = capsys.readouterr()
        assert captured.out == ''
        assert self.scheduler.sequence_number == init_seq_num

        # Should not take break if not after previous task finish time.
        self.scheduler.previous_task_finish_time = next_order + timedelta(seconds=10)

        self.scheduler.maybe_take_break(next_order)
        captured = capsys.readouterr()
        assert captured.out == ''
        assert self.scheduler.sequence_number == init_seq_num

        # Should take a break if after previous task finish time.
        now = datetime.now()
        self.scheduler.previous_task_finish_time = now
        next_order = datetime.now() + timedelta(seconds=10)

        self.scheduler.maybe_take_break(next_order)

        captured = capsys.readouterr()
        assert captured.out == f' 1. {now.strftime("%M:%S")} {self.TAKE_BREAK_ACTION} \n'
        assert self.scheduler.sequence_number == init_seq_num + 1

    def test_add_order(self):
        with freeze_time(datetime.now()) as frozen_datetime:
            sec_between_orders = 10
            first_order = frozen_datetime().replace(microsecond=0)
            second_order = frozen_datetime().replace(microsecond=0) + timedelta(seconds=sec_between_orders)

            self.scheduler.add_order()

            assert len(self.scheduler.orders) == 1
            assert self.scheduler.orders == [first_order]

            frozen_datetime.tick(delta=timedelta(seconds=sec_between_orders))
            self.scheduler.add_order()

            assert len(self.scheduler.orders) == 2
            assert self.scheduler.orders == [first_order, second_order]

    def test_print_schedule(self, capsys):
        start_time = datetime.now()

        with freeze_time(start_time) as frozen_datetime:
            sec_between_orders = 10

            # Populate some orders
            with capsys.disabled():
                self.scheduler.add_order()
                frozen_datetime.tick(delta=timedelta(seconds=sec_between_orders))
                self.scheduler.add_order()

            self.scheduler.print_schedule()

            expected_make_sand_1 = start_time
            expected_serve_sand_1 = expected_make_sand_1 + timedelta(seconds=self.scheduler.SEC_TO_MAKE_SANDWICH)
            expected_make_sand_2 = expected_serve_sand_1 + timedelta(seconds=self.scheduler.SEC_TO_SERVE_SANDWICH)
            expected_serve_sand_2 = expected_make_sand_2 + timedelta(seconds=self.scheduler.SEC_TO_MAKE_SANDWICH)
            expected_break = expected_serve_sand_2 + timedelta(seconds=self.scheduler.SEC_TO_SERVE_SANDWICH)

            captured = capsys.readouterr()
            assert captured.out == f' 1. {expected_make_sand_1.strftime("%M:%S")} {self.MAKE_SANDWICH_ACTION} 1\n' \
                                   f' 2. {expected_serve_sand_1.strftime("%M:%S")} {self.SERVE_SANDWICH_ACTION} 1\n' \
                                   f' 3. {expected_make_sand_2.strftime("%M:%S")} {self.MAKE_SANDWICH_ACTION} 2\n' \
                                   f' 4. {expected_serve_sand_2.strftime("%M:%S")} {self.SERVE_SANDWICH_ACTION} 2\n' \
                                   f' 5. {expected_break.strftime("%M:%S")} {self.TAKE_BREAK_ACTION} \n\n'