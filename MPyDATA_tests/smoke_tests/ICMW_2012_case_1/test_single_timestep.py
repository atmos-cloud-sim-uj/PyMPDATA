from MPyDATA.mpdata_factory import MPDATAFactory
# from MPyDATA.options import Options
import numpy as np
import pytest


# # @pytest.mark.skip # TODO: work in progress
# @pytest.mark.parametrize(
#     "opts", [
#         Options(nug=True),
#         Options(nug=True, fct=True),
#         Options(nug=True, fct=True, iga=True),
#         Options(nug=True, fct=True, tot=True),
#         Options(nug=True, fct=True, iga=True, tot=True),
#         Options(nug=True, fct=False, iga=True),
#         Options(nug=True, fct=False, tot=True),
#         Options(nug=True, fct=False, iga=True, tot=True)
#     ]
# )
def test_single_timestep():
    # Arrange
    grid = (75, 75)
    size = (1500, 1500)
    dt = 1
    w_max = .6

    def stream_function(xX, zZ):
        X = size[0]
        return - w_max * X / np.pi * np.sin(np.pi * zZ) * np.cos(2 * np.pi * xX)

    rhod_of = lambda z: 1 - z * 1e-4
    rhod = np.repeat(
        rhod_of(
            (np.arange(grid[1]) + 1 / 2) / grid[1]
        ).reshape((1, grid[1])),
        grid[0],
        axis=0
    )

    GC, eulerian_fields = MPDATAFactory.stream_function_2d(
        grid=grid, size=size, dt=dt,
        stream_function=stream_function,
        field_values={'th': np.full(grid, 300), 'qv': np.full(grid, .001)},
        g_factor=rhod
    )

    # Plot

    # Act
    eulerian_fields.step(nt=1, debug=True)

    # Assert
    for k, v in eulerian_fields.mpdatas.items():
        assert np.isfinite(v.curr.get()).all()
