#!/usr/bin/env python3
"""
HGD Installation Validation Script

This script checks if HGD is properly installed and all dependencies are available.
Run it after installing HGD to verify everything is working.

Usage:
    python validate_installation.py
"""

import sys
import subprocess
import importlib
import os
import tempfile
import json5


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_result(test_name, passed, message=""):
    """Print a test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[92m" if passed else "\033[91m"  # Green or Red
    reset = "\033[0m"
    
    print(f"{color}{status}{reset} - {test_name}")
    if message:
        print(f"      {message}")


def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    required = (3, 9)
    
    passed = version >= required
    message = f"Python {version.major}.{version.minor}.{version.micro}"
    if not passed:
        message += f" (Required: {required[0]}.{required[1]}+)"
    
    return passed, message


def check_module(module_name, package_name=None):
    """Check if a Python module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        return True, f"{package_name} is installed"
    except ImportError:
        return False, f"{package_name} is NOT installed"


def check_command(command):
    """Check if a command-line tool is available"""
    try:
        result = subprocess.run(
            [command, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        return True, f"{command} is available"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, f"{command} is NOT available"


def check_hgd_import():
    """Check if HGD can be imported and has expected modules"""
    try:
        import HGD
        import HGD.main
        import HGD.params
        import HGD.operators
        return True, "HGD package is properly installed"
    except ImportError as e:
        return False, f"HGD import failed: {e}"


def check_cpp_extension():
    """Check if C++ extension module is available"""
    try:
        import HGD.motion.d2q4_cpp
        return True, "C++ extension (d2q4_cpp) is available"
    except ImportError:
        return False, "C++ extension is NOT available (compilation may have failed)"


def run_minimal_test():
    """Try to run a minimal simulation"""
    # Create a minimal test configuration
    config = {
        "nx": 10,
        "ny": 10,
        "nm": 5,
        "H": 1,
        "t_f": 0.1,
        "IC_mode": "column",
        "nu_fill": 0.5,
        "fill_ratio": 0.5,
        "plot": [],
        "videos": [],
        "save_inc": 100,
    }
    
    # Write temporary config using cross-platform temp directory
    test_dir = os.path.join(tempfile.gettempdir(), "hgd_validation_test")
    os.makedirs(test_dir, exist_ok=True)
    config_path = os.path.join(test_dir, "test.json5")
    
    with open(config_path, "w") as f:
        json5.dump(config, f)
    
    # Try to run simulation
    try:
        result = subprocess.run(
            [sys.executable, "-m", "HGD.main", config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            return True, "Minimal simulation completed successfully"
        else:
            error = result.stderr.decode()[:200]
            return False, f"Simulation failed: {error}"
    except subprocess.TimeoutExpired:
        return False, "Simulation timed out (may indicate a problem)"
    except Exception as e:
        return False, f"Could not run simulation: {e}"


def main():
    """Run all validation checks"""
    print_header("HGD Installation Validation")
    
    all_passed = True
    
    # Check Python version
    print("\n📋 Checking Python version...")
    passed, msg = check_python_version()
    print_result("Python version", passed, msg)
    all_passed &= passed
    
    # Check required Python packages
    print("\n📦 Checking required Python packages...")
    packages = [
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("scipy", "scipy"),
        ("tqdm", "tqdm"),
        ("json5", "json5"),
    ]
    
    for module, package in packages:
        passed, msg = check_module(module, package)
        print_result(package, passed, msg)
        all_passed &= passed
    
    # Check HGD installation
    print("\n🔧 Checking HGD installation...")
    passed, msg = check_hgd_import()
    print_result("HGD package", passed, msg)
    all_passed &= passed
    
    # Check C++ extension
    if all_passed:
        passed, msg = check_cpp_extension()
        print_result("C++ extension", passed, msg)
        if not passed:
            print("      Note: Python-only mode will still work but be slower")
    
    # Check optional tools
    print("\n🛠️  Checking optional tools...")
    passed, msg = check_command("ffmpeg")
    print_result("ffmpeg (for videos)", passed, msg)
    if not passed:
        print("      Note: You can still run simulations, just no video output")
    
    passed, msg = check_command("cmake")
    print_result("CMake", passed, msg)
    
    # Summary
    print_header("Validation Summary")
    
    if all_passed:
        print("\n✅ SUCCESS! HGD is properly installed and ready to use.")
        print("\nNext steps:")
        print("  1. Try the quick test:")
        print("     python HGD/main.py json/minimal_test.json5")
        print("\n  2. Read the getting started guide:")
        print("     See GETTING_STARTED.md")
        print("\n  3. Explore examples:")
        print("     See EXAMPLES.md")
    else:
        print("\n❌ INSTALLATION INCOMPLETE")
        print("\nSome components are missing. Please:")
        print("  1. Review the error messages above")
        print("  2. Check TROUBLESHOOTING.md for solutions")
        print("  3. Ensure you ran: pip install -e .")
        print("\n  If problems persist, contact the development team:")
        print("  https://matrix.to/#/!UZnyhaLhQymfFbLJYI:matrix.org?via=matrix.org")
    
    print("\n" + "=" * 70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
