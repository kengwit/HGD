# HGD Troubleshooting Guide

This guide helps you resolve common issues when installing and using HGD.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Performance Issues](#performance-issues)
- [Output Issues](#output-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Getting More Help](#getting-more-help)

---

## Installation Issues

### Problem: `pip install -e .` fails with "No module named 'skbuild'"

**Error message:**
```
ModuleNotFoundError: No module named 'skbuild'
```

**Solution:**
```bash
pip install --upgrade pip setuptools wheel
pip install scikit-build-core pybind11
pip install -e .
```

---

### Problem: CMake not found

**Error message:**
```
CMake Error: CMake was unable to find a build program corresponding to "Unix Makefiles"
```

**Solution:**
Install CMake:
- **Ubuntu/Debian:** `sudo apt-get install cmake`
- **macOS:** `brew install cmake`
- **Windows:** Download from [cmake.org](https://cmake.org/download/)

After installing, verify:
```bash
cmake --version  # Should show 3.15 or higher
```

---

### Problem: C++ compiler not found

**Error message:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```
or
```
error: command 'gcc' failed
```

**Solution:**

**Linux:**
```bash
sudo apt-get install build-essential g++
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
- Install [Visual Studio Community Edition](https://visualstudio.microsoft.com/)
- Select "Desktop development with C++" workload during installation

---

### Problem: OpenMP not found

**Error message:**
```
fatal error: omp.h: No such file or directory
```

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install libomp-dev
```

**macOS:**
```bash
brew install libomp
```

**Windows:**
OpenMP should be included with Visual Studio. If not, reinstall with C++ support.

---

### Problem: "No module named 'HGD'" after installation

**Symptoms:**
```python
>>> import HGD
ModuleNotFoundError: No module named 'HGD'
```

**Solution:**
1. Make sure you're in the correct directory:
   ```bash
   cd /path/to/HGD
   ```

2. Reinstall:
   ```bash
   pip install -e .
   ```

3. Verify Python is using the correct environment:
   ```bash
   which python  # or: where python on Windows
   pip list | grep HGD
   ```

4. If using virtual environment, make sure it's activated:
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

---

## Runtime Errors

### Problem: AttributeError: 'dict_to_class' object has no attribute 'defined_time_step_size'

**Error message:**
```
AttributeError: 'dict_to_class' object has no attribute 'defined_time_step_size'
```

**Cause:** When `inertia` is set to `true`, the parameter `defined_time_step_size` is required but missing.

**Solution:**
Add this line to your JSON5 configuration file:
```json5
{
    inertia: true,
    defined_time_step_size: 1e-3,  // Add this line
    // ... other parameters
}
```

The value `1e-3` is a reasonable starting point for most simulations. Adjust based on your needs:
- Smaller values (e.g., `1e-4`): More accurate but slower
- Larger values (e.g., `1e-2`): Faster but may be unstable

---

### Problem: Simulation starts but immediately crashes

**Error message:**
```
Traceback (most recent call last):
  ...
IndexError: index out of bounds
```

**Common causes:**

1. **Grid too small:** Increase `nx`, `ny`, or `nm`
   ```json5
   nx: 20,  // Minimum recommended
   ny: 20,
   nm: 10,
   ```

2. **Invalid boundary condition:** Check `boundaries` parameter
   ```json5
   boundaries: ["central_outlet"],  // Must be a list
   ```

3. **Incompatible parameters:** Some combinations don't work
   - Can't have outlet without appropriate boundary
   - `IC_mode` must match geometry

---

### Problem: KeyError or missing parameter

**Error message:**
```
KeyError: 'some_parameter'
```

**Solution:**
HGD uses default values from `json/defaults.json5`. If a required parameter is missing:

1. Check parameter name spelling
2. Ensure parameter is defined in either:
   - Your JSON5 file, or
   - `json/defaults.json5`

3. For new/custom parameters, make sure they're properly initialized

---

### Problem: "Cannot allocate memory" or MemoryError

**Error message:**
```
MemoryError: Unable to allocate array
```
or
```
numpy.core._exceptions._ArrayMemoryError
```

**Cause:** Grid resolution too high for available RAM.

**Solution:**

1. **Reduce resolution:**
   ```json5
   nx: 25,   // Reduced from 50
   ny: 25,   // Reduced from 50
   nm: 10,   // Reduced from 20
   ```

2. **Estimate memory usage:**
   - Memory ≈ `nx * ny * nm * 8 bytes * number_of_fields`
   - Example: 50×50×20 grid ≈ 50×50×20×8×10 = 40 MB (manageable)
   - Example: 100×100×100 grid ≈ 100×100×100×8×10 = 800 MB (high)

3. **Close other applications** to free RAM

4. **Use a machine with more memory**

---

### Problem: FileNotFoundError for JSON file

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'json/example.json5'
```

**Solution:**

1. **Check you're in the HGD directory:**
   ```bash
   ls json/  # Should list .json5 files
   ```

2. **Use relative or absolute path:**
   ```bash
   # From HGD directory
   python HGD/main.py json/hopper.json5
   
   # From anywhere with absolute path
   python /full/path/to/HGD/main.py /full/path/to/json/hopper.json5
   ```

---

## Performance Issues

### Problem: Simulation is very slow

**Symptoms:**
- Takes hours to complete
- Progress bar shows < 10 iterations/second

**Solutions:**

1. **Reduce resolution** (fastest improvement):
   ```json5
   nx: 25,  // Reduced from 100
   ny: 25,  // Reduced from 100
   ```

2. **Use faster motion model:**
   ```json5
   motion_model: 'd2q4_cpp',  // Fastest (C++)
   // instead of: 'd2q4_slow' (slowest, Python)
   ```

3. **Reduce simulation time:**
   ```json5
   t_f: 2,  // Shorter simulation
   ```

4. **Save less frequently:**
   ```json5
   save_inc: 100,  // Save every 100 steps instead of every step
   ```

5. **Disable unnecessary calculations:**
   ```json5
   calculate_stress: false,
   calculate_temperature: false,
   ```

6. **Use parallel execution:**
   ```json5
   max_workers: 4,  // Use 4 CPU cores
   ```

---

### Problem: Simulation uses 100% CPU but is still slow

**This is normal behavior.** Granular simulations are computationally intensive.

**To improve:**
- Use the C++ motion model (`d2q4_cpp`)
- Reduce grid resolution
- Ensure OpenMP is properly installed for parallel C++ execution

---

## Output Issues

### Problem: No output files generated

**Symptoms:**
- Simulation completes
- No files in `output/` directory

**Solutions:**

1. **Check plot/video parameters:**
   ```json5
   plot: ['nu', 's'],      // Must list what to plot
   videos: ['nu', 's'],    // Must list what to save as video
   ```

2. **Check save_inc is not too large:**
   ```json5
   save_inc: 1,  // Save every timestep
   ```

3. **Verify output directory:**
   ```bash
   ls -la output/  # Check if directory exists and has content
   ```

4. **Check for error messages** during simulation

---

### Problem: Videos are not created

**Symptoms:**
- PNG images are generated
- No MP4 files

**Cause:** ffmpeg is not installed or not in PATH.

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to system PATH

**Workaround:** Use PNG images directly or create videos manually:
```bash
cd output/hopper/repose_angle_30/
ffmpeg -framerate 10 -pattern_type glob -i 'nu_*.png' -c:v libx264 nu.mp4
```

---

### Problem: Images look wrong or corrupted

**Symptoms:**
- All white or all black images
- Strange patterns
- NaN values

**Solutions:**

1. **Check initial conditions:**
   ```json5
   IC_mode: "column",  // Valid: "column", "random", "top", "full", "empty"
   nu_fill: 0.5,       // Should be 0 < nu_fill < 1
   ```

2. **Check material properties:**
   ```json5
   s_m: 0.001,   // Must be positive
   nu_cs: 0.5,   // Typically 0.5-0.65
   ```

3. **Reduce time step** if using inertia:
   ```json5
   defined_time_step_size: 1e-4,  // Smaller = more stable
   ```

---

## Platform-Specific Issues

### macOS: "Library not loaded" error

**Error message:**
```
Library not loaded: @rpath/libomp.dylib
```

**Solution:**
```bash
brew install libomp
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$DYLD_LIBRARY_PATH
```

Add the export line to your `~/.zshrc` or `~/.bash_profile`.

---

### Windows: "DLL load failed"

**Error message:**
```
ImportError: DLL load failed while importing module
```

**Solution:**
1. Install Visual C++ Redistributable from Microsoft
2. Reinstall with Visual Studio C++ tools properly configured
3. Use Python from python.org (not Microsoft Store version)

---

### Linux: "Permission denied" when running

**Error message:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Make sure you have write permission in the directory
chmod +x HGD/main.py
# Or run from your home directory with full paths
```

---

## Getting More Help

If your problem isn't listed here:

### 1. Check Existing Issues
Visit [GitHub Issues](https://github.com/benjym/HGD/issues) to see if others have encountered the same problem.

### 2. Enable Debug Output
Run with verbose output:
```bash
python -v HGD/main.py json/example.json5
```

### 3. Check Your Configuration
Verify your JSON5 file syntax:
```bash
python -c "import json5; json5.load(open('json/your_file.json5'))"
```

### 4. Gather Information
When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- HGD version/commit
- Complete error message
- JSON5 configuration file
- Steps to reproduce

### 5. Ask for Help

- **Matrix Chat:** [https://matrix.to/#/!UZnyhaLhQymfFbLJYI:matrix.org?via=matrix.org](https://matrix.to/#/!UZnyhaLhQymfFbLJYI:matrix.org?via=matrix.org)
- **GitHub Issues:** [https://github.com/benjym/HGD/issues](https://github.com/benjym/HGD/issues)
- **Email:** Contact authors listed in README.md

### 6. Minimal Example
When asking for help, create a minimal example that reproduces the issue:
```json5
{
    // Minimal configuration that shows the problem
    nx: 20,
    ny: 20,
    nm: 10,
    H: 1,
    t_f: 1,
}
```

---

## Common Warnings (Not Errors)

These warnings are usually safe to ignore:

```
FutureWarning: The 'warn' parameter is deprecated
```
- From numpy/matplotlib, not from HGD
- Does not affect functionality

```
/usr/lib/python3.*/dist-packages/matplotlib/...
```
- matplotlib backend warnings
- Usually harmless

```
tqdm: ... position is incorrect
```
- Progress bar display issue
- Doesn't affect simulation accuracy

---

## Quick Diagnostic Checklist

When something goes wrong, check:

- [ ] Python 3.9+ installed?
- [ ] C++ compiler installed?
- [ ] CMake 3.15+ installed?
- [ ] OpenMP installed?
- [ ] `pip install -e .` completed successfully?
- [ ] Running from HGD directory?
- [ ] JSON5 file exists and is valid?
- [ ] JSON5 file has required parameters?
- [ ] Sufficient RAM for grid size?
- [ ] Enough disk space for output?

---

Happy troubleshooting! If all else fails, start with the simplest example (`collapse.json5`) and build up from there. 🔧
