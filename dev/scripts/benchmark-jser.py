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
    
    start = time.perf_counter()
    series = Series.openJser(jser_path)
    
    # Count sections to make sure the data is loaded
    num_sections = len(series.sections)
    elapsed = time.perf_counter() - start
    
    print(f"Total time: {elapsed:.3f}s")
    print(f"Sections: {num_sections}")
    
    # Time the page sections loading
    section_load_start = time.perf_counter()
    section_load_total = 0
    for snum in series.sections.keys(): 
        if snum is not None:
            section = series.loadSection(snum)
            section_load_total += 1
    section_load_elapsed = time.perf_counter() - section_load_start
    
    print(f"Page Sections time: {section_load_elapsed:.3f}s")
    
    # Time accessing all objects
    object_access_start = time.perf_counter()
    obj_names = series.objects.getNames()
    for obj_name in obj_names:
        obj = series.objects[obj_name]
        # Access some information to make sure the object data is loaded
        _ = obj.name
        _ = obj.count
        _ = obj.volume
    object_access_elapsed = time.perf_counter() - object_access_start
    
    print(f"Go to specific object time: {object_access_elapsed:.3f}s")
    
    series.close()


def main():
    parser = argparse.ArgumentParser(description="Benchmark JSER file loading")
    parser.add_argument("jser_file", help="Path to JSER file")
    args = parser.parse_args()
    
    benchmark_jser_file(args.jser_file)


if __name__ == "__main__":
    main()
