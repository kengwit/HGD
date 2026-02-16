# Getting Started with HGD

Welcome to Heterarchical Granular Dynamics (HGD)! This guide will help you install and run your first granular mechanics simulation.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Verify Installation](#verify-installation)
4. [Your First Simulation](#your-first-simulation)
5. [Understanding the Output](#understanding-the-output)
6. [Next Steps](#next-steps)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

Before installing HGD, ensure your system has the following:

#### Required Software

- **Python 3.9 or newer** (Python 3.11+ recommended)
- **C++ Compiler** with C++11 support:
  - Linux: `g++` (usually pre-installed)
  - macOS: Xcode Command Line Tools
  - Windows: Visual Studio with C++ support or MinGW
- **CMake 3.15 or newer**
- **OpenMP** (for parallel C++ execution)

#### Installing System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip g++ cmake libomp-dev
```

**macOS:**
```bash
# Install Homebrew if not already installed (https://brew.sh)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python cmake libomp
```

**Windows:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Install Visual Studio Community Edition with "Desktop development with C++" workload
- Install CMake from [cmake.org](https://cmake.org/download/)

### Hardware Requirements

- **Minimum:** 4 GB RAM, 2 CPU cores
- **Recommended:** 8+ GB RAM, 4+ CPU cores (simulations can be computationally intensive)

## Installation

### Step 1: Get the Code

Clone or download the repository:

```bash
# Using git (recommended)
git clone https://github.com/benjym/HGD.git
cd HGD

# Or download and extract the ZIP file from GitHub
```

### Step 2: Install Python Package

Install HGD and all its dependencies:

```bash
pip install -e .
```

This command will:
- Install all required Python packages (numpy, matplotlib, scipy, etc.)
- Compile the C++ extension modules
- Set up the package in "editable" mode for development

**Note:** The installation may take a few minutes as it compiles C++ code and downloads dependencies.

### Step 3: Verify Installation

Run the validation script to check everything is working:

```bash
python validate_installation.py
```

This script checks:
- ✓ Python version (3.9+)
- ✓ Required packages (numpy, matplotlib, scipy, etc.)
- ✓ HGD package installation
- ✓ C++ extension compilation
- ✓ Optional tools (ffmpeg for videos, CMake)

If all checks pass, you'll see: **✅ SUCCESS! HGD is properly installed and ready to use.**

If any checks fail, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

### Step 4: Set Up Pre-commit Hooks (Optional, for developers)

If you plan to contribute to HGD development:

```bash
pre-commit install
```

## Verify Installation

Let's verify that HGD is installed correctly:

### Quick Test

Run this simple Python command:

```bash
python -c "import HGD; print('HGD installed successfully!')"
```

If you see "HGD installed successfully!" then the installation worked.

### Run a Quick Validation

Try running the minimal test simulation (takes ~10 seconds):

```bash
python HGD/main.py json/minimal_test.json5
```

This should:
- Complete in ~10 seconds
- Create output in `output/minimal_test/`
- Generate PNG images of the simulation

Check the output:
```bash
ls output/minimal_test/
# Should show: nu_000000.png, nu_000010.png, etc.
```

If you see PNG files, congratulations! HGD is working correctly. 🎉

### Run Unit Tests (Optional)

For developers, you can also run the test suite:

```bash
python test/test_operators.py
```

This should complete without errors.

## Your First Simulation

Now let's run your first granular mechanics simulation! We'll simulate a column of granular material collapsing under gravity.

### Step 1: Choose an Example

HGD comes with several example configurations in the `json/` directory. Let's start with a simple hopper example:

```bash
python HGD/main.py json/hopper.json5
```

This simulation will:
- Create a hopper (funnel-shaped container) filled with granular material
- Simulate material flowing out through a central outlet
- Generate visualization videos of the particle density and size distribution

**Expected runtime:** 1-5 minutes depending on your computer

### Step 2: Watch the Progress

You'll see progress bars showing:
- Overall simulation progress
- Individual simulation variants (if there are multiple parameter combinations)

Example output:
```
Sim:  50%|█████     | 1/2 [00:30<00:30, 30.0s/it]
inertia=False: 100%|██████████| 8266/8266 [00:30<00:00, 275.53it/s]
```

### Step 3: Find Your Results

When the simulation completes, results are saved in the `output/` directory:

```
output/
└── hopper/
    ├── repose_angle_0/
    │   ├── nu_0000.png
    │   ├── nu_0100.png
    │   ├── ...
    │   └── nu.mp4
    ├── repose_angle_30/
    └── repose_angle_60/
```

## Understanding the Output

### Output Files

For each simulation, HGD generates:

- **PNG images:** Snapshots at regular intervals showing:
  - `nu_*.png` - Solid volume fraction (particle density)
  - `s_*.png` - Particle size distribution
  - `stress_*.png` - Stress field (if calculated)
  
- **MP4 videos:** Animated visualizations:
  - `nu.mp4` - Time evolution of particle density
  - `s.mp4` - Evolution of particle size distribution

- **Data files:** (if enabled in configuration)
  - `.npz` files containing raw numerical data for further analysis

### Interpreting Results

- **Solid fraction (nu):**
  - White/bright areas = high particle density
  - Dark areas = low particle density (voids)
  - Range: 0 (empty) to ~0.6 (densely packed)

- **Particle size (s):**
  - Different colors represent different particle sizes
  - Helps visualize segregation and mixing

## Next Steps

### Try Other Examples

Explore different scenarios:

```bash
# Granular collapse
python HGD/main.py json/collapse.json5

# Hopper with different friction angles
python HGD/main.py json/hopper.json5

# Slope stability
python HGD/main.py json/test_slope.json5
```

For descriptions of all available examples, see [EXAMPLES.md](EXAMPLES.md).

### Create Your Own Simulation

1. Copy an example configuration:
   ```bash
   cp json/hopper.json5 json/my_simulation.json5
   ```

2. Edit the parameters (see [Parameter Reference](#parameter-reference))

3. Run your simulation:
   ```bash
   python HGD/main.py json/my_simulation.json5
   ```

### Parameter Reference

Key parameters you can modify:

- **Resolution:**
  - `nx`: Horizontal grid cells (higher = more detailed, slower)
  - `ny`: Vertical grid cells
  - `nm`: Number of internal states (parallel simulations)

- **Geometry:**
  - `H`: Physical height of system (meters)
  - `theta`: Gravity angle (0 = vertical, degrees)
  - `boundaries`: Boundary conditions (e.g., "central_outlet")

- **Material Properties:**
  - `repose_angle`: Angle of repose / friction angle (degrees)
  - `s_m`: Minimum particle size (meters)
  - `s_M`: Maximum particle size (meters)
  - `gsd_mode`: Grain size distribution ('mono', 'bi', or 'poly')

- **Simulation:**
  - `t_f`: Final simulation time (seconds)
  - `save_inc`: How often to save outputs (timesteps)

For a complete list with defaults, see `json/defaults.json5`.

## Troubleshooting

### Installation Issues

**Problem:** "No module named 'HGD'"
```
Solution: Make sure you ran `pip install -e .` from the HGD directory
```

**Problem:** "CMake Error" or "C++ compiler not found"
```
Solution: Install CMake and a C++ compiler (see Prerequisites section)
```

**Problem:** "fatal error: omp.h: No such file or directory"
```
Solution: Install OpenMP development libraries
  Ubuntu/Debian: sudo apt-get install libomp-dev
  macOS: brew install libomp
```

### Runtime Issues

**Problem:** `AttributeError: 'dict_to_class' object has no attribute 'defined_time_step_size'`
```
Solution: If using inertia=true, you must add:
  defined_time_step_size: 1e-3  // in your JSON configuration
```

**Problem:** Simulation runs but produces no output
```
Solution: Check that the 'plot' and 'videos' parameters are set in your JSON file
  plot: ['nu', 's']
  videos: ['nu', 's']
```

**Problem:** "Cannot allocate memory" or out of memory errors
```
Solution: Reduce grid resolution (nx, ny, nm) or increase system RAM
```

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Getting Help

- **Documentation:** [https://benjym.github.io/HGD/](https://benjym.github.io/HGD/)
- **Support:** Contact the development team on [Matrix](https://matrix.to/#/!UZnyhaLhQymfFbLJYI:matrix.org?via=matrix.org)
- **Issues:** Report bugs on [GitHub Issues](https://github.com/benjym/HGD/issues)

## What's Next?

- Read [EXAMPLES.md](EXAMPLES.md) to understand available example scenarios
- Explore the [API Reference](https://benjym.github.io/HGD/reference) for advanced usage
- Check out published papers using HGD in the `papers/` directory
- Join the community chat for questions and discussions

Happy simulating! 🎉
