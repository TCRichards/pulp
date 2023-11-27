import os
from contextlib import contextmanager
from pulp import LpProblem, PulpTimeoutError, PULP_CBC_CMD, GLPK_CMD


def testHardTimeLimit():
    for testcase in ((GLPK_CMD, "hanging.json"),
                     (PULP_CBC_CMD, "cbc_hang.test_mps")):
        solver = testcase[0](timeLimit=20, hardTimeLimit=30)
        hangFilePath = os.path.join(os.path.dirname(__file__), testcase[1])
        if hangFilePath.endswith(".mps"):
            _, prob = LpProblem.fromMPS(hangFilePath)
        elif hangFilePath.endswith(".json"):
            _, prob = LpProblem.from_json(hangFilePath)
        else:
            raise ValueError(f'Unknown file type: {hangFilePath}')

        try:
            prob.solve(solver)
        except PulpTimeoutError:
            pass
        else:
            raise AssertionError("PulpTimeoutError not raised")


if __name__ == '__main__':
    testHardTimeLimit()