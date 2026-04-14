import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
import hashlib, base64, hmac
from ransomware.crypto import make_fernet

TESTCASES_PATH = Path(__file__).resolve().parent.parent / "problem_bank" / "testcases"
CPP_TIMEOUT_SECONDS = 2
PYTHON_TIMEOUT_SECONDS = 5.0
SEGFAULT_RETURN_CODE = -11


def load_io(problem_id: str) -> tuple[str, str]:
    input_path = TESTCASES_PATH / f"{problem_id}.in"
    enc_path   = TESTCASES_PATH / f"{problem_id}.out.enc"
    stdin = input_path.read_text()
    expected = make_fernet().decrypt(enc_path.read_bytes()).decode()
    return stdin, expected


def get_python() -> str:
    if shutil.which("python3"):
        return "python3"
    if shutil.which("python"):
        return "python"
    raise RuntimeError("No Python found")


def judge_submission(file_path, problem_id):
    source_path = Path(file_path)
    source_code = source_path.read_text()
    stdin_text, expected_text = load_io(problem_id)

    ext = source_path.suffix.lower()
    binary = None
    runtime_command: list[str]
    timeout_seconds: float

    if ext == ".cpp":
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w") as handle:
            handle.write(source_code)
            src = handle.name

        binary = src.replace(".cpp", "")
        compile_result = subprocess.run(
            ["g++", "-O2", "-std=c++17", "-o", binary, src],
            capture_output=True,
            text=True,
        )
        if compile_result.returncode != 0:
            os.unlink(src)
            return {"status": "Compile Error", "detail": compile_result.stderr}

        runtime_command = [binary]
        timeout_seconds = CPP_TIMEOUT_SECONDS
    elif ext == ".py":
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as handle:
            handle.write(source_code)
            src = handle.name

        runtime_command = [get_python(), src]
        timeout_seconds = PYTHON_TIMEOUT_SECONDS
    else:
        raise Exception("Please submit a valid CPP or Python file.")

    start = time.time()
    try:
        run = subprocess.run(
            runtime_command,
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        elapsed = time.time() - start
        actual = run.stdout.strip()
        expected = expected_text.strip()
        if run.returncode != 0:
            stderr_lower = run.stderr.lower()
            if run.returncode == SEGFAULT_RETURN_CODE or "segmentation fault" in stderr_lower:
                status = "SEGFAULT"
            else:
                status = "RTE"
        elif actual == expected:
            status = "AC"
        else:
            status = "WA"
        return [
            {
                "case": 1,
                "status": status,
                "time_ms": round(elapsed * 1000),
                "expected": expected,
                "actual": actual,
                "stderr": run.stderr,
            }
        ]
    except subprocess.TimeoutExpired:
        return [{"case": 1, "status": "TLE"}]
    finally:
        os.unlink(src)
        if binary and os.path.exists(binary):
            os.unlink(binary)


def judge(file_path, problem_id):
    return judge_submission(file_path, problem_id)
