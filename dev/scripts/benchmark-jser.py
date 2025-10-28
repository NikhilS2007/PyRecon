"""Benchmark JSER file loading time.

How to Use:
    python benchmark-jser.py <path-to-jser-file>

Arguments:
    path-to-jser-file: Path to the JSER file you want to benchmark.
                      This can be a relative or absolute path.
"""

import os
import sys
import time
import argparse
import shutil
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PyReconstruct.modules.datatypes import Series
from pathlib import Path as PathLib


# Initialize Qt for a series operation
app = QApplication(sys.argv)

def benchmark_jser_file(jser_path):
    # Check if the file exists
    if not os.path.exists(jser_path):
        print(f"Error: File not found: {jser_path}")
        sys.exit(1)
    
    # Check if the file is a JSER file
    if not jser_path.lower().endswith('.jser'):
        print(f"Error: Not a JSER file: {jser_path}")
        sys.exit(1)
    
    # Get the file size in MB
    file_size = os.path.getsize(jser_path) / (1024 * 1024)
    
    # Delete any cached hidden folder to get a fresh load
    # This is because in series.py, the hidden folder is cached to speed up loading.
    # If the hidden folder exists, it will be used instead of creating a new one.
    sdir = os.path.dirname(jser_path)
    sname = Path(jser_path).stem
    hidden_dir = os.path.join(sdir, f".{sname}")
    
    if os.path.exists(hidden_dir):
        shutil.rmtree(hidden_dir)
    
    # Time the loading operation
    print(f"File: {os.path.basename(jser_path)} ({file_size:.2f} MB)")
    print("Loading... ", end="", flush=True)
    
    start = time.perf_counter()
    series = Series.openJser(jser_path)
    
    # Count sections to ensure data loaded
    num_sections = len([s for s in series.sections if s is not None])
    elapsed = time.perf_counter() - start
    
    print(f"{elapsed:.3f}s")
    print(f"Sections: {num_sections}")
    print(f"Time: {elapsed:.3f}s")
    
    series.close()


def main():
    parser = argparse.ArgumentParser(description="Benchmark JSER file loading")
    parser.add_argument("jser_file", help="Path to JSER file")
    args = parser.parse_args()
    
    benchmark_jser_file(args.jser_file)


if __name__ == "__main__":
    main()
