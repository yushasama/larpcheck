import subprocess, tempfile, os, time
from pathlib import Path
import shutil
import json

def load_test_cases(problem_id):
    path = Path("../problem_bank/") + problem_id

    with open(path, 'r') as f:
        data = json.load(f)

    return [(tc["input"], tc["output"]) for tc in data
    ["test_cases"]]

def get_python():
    if shutil.which('python3'):
        return 'python3'
    elif shutil.which('python'):
        return 'python'
    else:
        raise RuntimeError('No Python found')

def judge_submission(file_path, problem_id):
    with open(file_path, 'r') as f:
        source_code = f.read()

    test_cases = load_test_cases(problem_id)

    ext = os.path.splitext(file_path)[1].lower()

    binary = None

    if ext == ".cpp":
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False, mode='w') as f:
            f.write(source_code)
            src = f.name
            
            binary = src.replace('.cpp', '')
            
            compile_result = subprocess.run(
                ['g++', '-O2', '-std=c++17', '-o', binary, src],
                capture_output=True, text=True
            )

            if compile_result.returncode != 0:
                os.unlink(src)

                return {'status': 'Compile Error', 'detail': compile_result.stderr}

            file_type = 'C++'
            
    elif ext == ".py":
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
            f.write(source_code)
            src = f.name

            file_type = 'PY'

    else:
       raise Exception("Please submit a valid CPP or Python file.")

    results = []

    test_cases = ""

    for i, (stdin, expected) in enumerate(test_cases):
        start = time.time()

        try:
            run = subprocess.run(
                [binary] if file_type == 'C++' else [get_python(), src],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=2 if file_type == 'C++' else 5.0
            )
    
            elapsed = time.time() - start
            actual = run.stdout.strip()
            expected = expected.strip()
    
            status = 'AC' if actual == expected else 'WA'

            results.append({
                'case': i+1,
                'status': status,
                'time_ms': round(elapsed * 1000),
                'expected': expected,
                'actual': actual,
                'stderr': run.stderr
            })

        except subprocess.TimeoutExpired:
            results.append({'case': i+1, 'status': 'TLE'})

    os.unlink(src)

    if binary and os.path.exists(binary):
        os.unlink(binary)

    return results

def judge(file_path, problem_id):
    ext = os.path.splitext(file_path)[1].lower()

    return judge_submission(file_path, problem_id)