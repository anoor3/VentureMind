"""Unit tests for the Python executor tool."""
from venturemind.tools.python_executor import PythonExecutor


def test_python_executor_runs_code():
    executor = PythonExecutor()
    result = executor.run("result = sum(values)", {"values": [1, 2, 3]})
    assert result["result"] == 6
