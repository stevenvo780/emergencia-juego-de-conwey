"""Run the real App loop with finite events and no GUI, GPU or dependencies."""
import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, call, patch


SOURCE = Path(os.environ.get(
    "ZOOM_APP_SOURCE", Path(__file__).resolve().parents[1] / "game_of_life_app.py"))


def event(kind, **attributes):
    return SimpleNamespace(type=kind, **attributes)


def wheel(button, count=1):
    return [event("MOUSEBUTTONDOWN", button=button) for _ in range(count)]


class Grid:
    def __init__(self, cells):
        self.cells = cells

    def __getitem__(self, index):
        row, column = index
        return self.cells[row][column]


class ZoomBoundsTests(unittest.TestCase):
    def run_app(self, batches, offset=(0, 0), evolving=False):
        self.assertEqual(batches[-1][-1].type, "QUIT")
        pg = ModuleType("pygame")
        for name in ("QUIT", "KEYDOWN", "KEYUP", "MOUSEBUTTONDOWN",
                     "MOUSEBUTTONUP", "MOUSEMOTION", "RESIZABLE",
                     "K_LEFT", "K_RIGHT", "K_UP", "K_DOWN"):
            setattr(pg, name, name)
        rectangles, frames = [], []
        screen = SimpleNamespace(fill=Mock(side_effect=lambda color: rectangles.clear()))
        pg.init = Mock()
        pg.display = SimpleNamespace(
            set_mode=Mock(return_value=screen), set_caption=Mock(),
            update=Mock(side_effect=lambda: frames.append(tuple(rectangles))))
        pg.draw = SimpleNamespace(rect=Mock(
            side_effect=lambda surface, color, rect: rectangles.append(rect)))
        pg.event = SimpleNamespace(get=Mock(side_effect=batches))
        pg.time = SimpleNamespace(delay=Mock())
        cp = ModuleType("cupy")
        cp.asnumpy = Mock(side_effect=lambda grid: grid)
        grids = [Grid(((1, 0, 1), (0, 1, 0))), Grid(((0, 1, 0), (1, 0, 1)))]
        game = SimpleNamespace(rows=2, cols=3, grid=grids[0])
        used_grids = []

        def update():
            if evolving:
                game.grid = grids[len(used_grids) % 2]
            used_grids.append(game.grid)

        game.update = Mock(side_effect=update)
        with patch.dict(sys.modules, {"pygame": pg, "cupy": cp}):
            spec = importlib.util.spec_from_file_location("zoom_app_under_test", SOURCE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            app = module.App(game)
            self.assertEqual(app.cellSize, 10)
            app.view_offset[:] = offset
            app.run()
        count = len(batches)
        self.assertIs(app.game_of_life, game)
        self.assertEqual((game.rows, game.cols), (2, 3))
        self.assertEqual(game.update.call_count, count)
        self.assertEqual(cp.asnumpy.call_args_list, [call(grid) for grid in used_grids])
        self.assertEqual(pg.event.get.call_count, count)
        self.assertEqual(pg.display.update.call_count, count)
        self.assertEqual(pg.time.delay.call_args_list, [call(100)] * count)
        pg.init.assert_called_once_with()
        pg.display.set_mode.assert_called_once_with([1600, 820], pg.RESIZABLE)
        pg.display.set_caption.assert_called_once_with("Conway's Game of Life GPU Optimized")
        self.assertEqual(screen.fill.call_args_list, [call((0, 0, 0))] * count)
        for draw in pg.draw.rect.call_args_list:
            self.assertIs(draw.args[0], screen)
            self.assertEqual(draw.args[1], (255, 255, 255))
        return SimpleNamespace(app=app, game=game, frames=frames, grids=grids)

    def test_ten_and_many_down_events_keep_positive_rectangles(self):
        for count in (10, 1000):
            with self.subTest(events=count):
                result = self.run_app([wheel(5, count) + [event("QUIT")]], (7, -3))
                self.assertIs(type(result.app.cellSize), int)
                self.assertEqual(result.app.cellSize, 1)
                self.assertEqual(result.app.view_offset, [7, -3])
                self.assertEqual(result.frames, [((7, -3, 1, 1), (9, -3, 1, 1),
                                                 (8, -2, 1, 1))])

    def test_repeated_down_batches_stay_at_minimum(self):
        batches = [wheel(5, 10), wheel(5, 1000), wheel(5, 10) + [event("QUIT")]]
        for repetition in range(2):
            with self.subTest(repetition=repetition):
                result = self.run_app(batches)
                self.assertEqual(result.app.cellSize, 1)
                self.assertEqual(result.frames, [((0, 0, 1, 1), (2, 0, 1, 1),
                                                 (1, 1, 1, 1))] * 3)

    def test_normal_down_then_up(self):
        result = self.run_app([wheel(5), wheel(4) + [event("QUIT")]], (7, -3))
        self.assertEqual(result.app.cellSize, 10)
        self.assertEqual(result.frames, [((7, -3, 9, 9), (25, -3, 9, 9), (16, 6, 9, 9)),
                                         ((7, -3, 10, 10), (27, -3, 10, 10), (17, 7, 10, 10))])

    def test_up_from_saturation(self):
        result = self.run_app([wheel(5, 1000), wheel(4) + [event("QUIT")]], (7, -3))
        self.assertEqual(result.app.cellSize, 2)
        self.assertEqual(result.app.view_offset, [7, -3])
        self.assertEqual(result.frames, [((7, -3, 1, 1), (9, -3, 1, 1), (8, -2, 1, 1)),
                                         ((7, -3, 2, 2), (11, -3, 2, 2), (9, -1, 2, 2))])

    def test_panning_with_nonzero_offset_and_keyboard_state(self):
        batches = [[event("MOUSEBUTTONDOWN", button=1),
                    event("MOUSEMOTION", rel=(4, -6)), event("KEYDOWN", key="K_LEFT")]
                   + wheel(5),
                   [event("MOUSEBUTTONUP", button=1), event("MOUSEMOTION", rel=(99, 99)),
                    event("KEYUP", key="K_LEFT")] + wheel(4) + [event("QUIT")]]
        result = self.run_app(batches, (7, -3))
        self.assertEqual(result.app.cellSize, 10)
        self.assertEqual(result.app.view_offset, [11, -9])
        self.assertFalse(result.app.dragging)
        self.assertFalse(any(result.app.keys_pressed.values()))
        self.assertEqual(result.frames, [((11, -9, 9, 9), (29, -9, 9, 9), (20, 0, 9, 9)),
                                         ((11, -9, 10, 10), (31, -9, 10, 10), (21, 1, 10, 10))])

    def test_simulation_keeps_updating_each_frame_including_quit(self):
        for zoom in ([], wheel(5, 1000)):
            with self.subTest(zoom_events=len(zoom)):
                result = self.run_app([zoom, [], [event("QUIT")]], evolving=True)
                self.assertEqual(result.game.grid.cells, ((1, 0, 1), (0, 1, 0)))
                self.assertEqual([len(frame) for frame in result.frames], [3, 3, 3])
                self.assertEqual(result.frames[0], result.frames[2])
                self.assertNotEqual(result.frames[0], result.frames[1])

    def test_quit_iteration_still_updates_and_draws(self):
        result = self.run_app([[event("QUIT")]])
        self.assertEqual(result.app.cellSize, 10)
        self.assertEqual(result.frames, [((0, 0, 10, 10), (20, 0, 10, 10), (10, 10, 10, 10))])


if __name__ == "__main__":
    unittest.main()
