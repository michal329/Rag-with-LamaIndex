import subprocess


def test_main_runs() -> None:
    result = subprocess.run(["python", "src/main.py"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "AI008 Python project is ready." in result.stdout
