# Heterarchical Granular Dynamics (HGD)

**Disclaimer: This code is under development and is likely to have significant breaking changes in the near future. Many features are incomplete or redundant. Please contact the development team if you would like a tour.**

A Python package for simulating the motion of granular materials as a result of the motion of voids. HGD models non-inertial problems and segregation particularly well for several systems.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Quick Start

**New to HGD?** Follow our comprehensive [Getting Started Guide](GETTING_STARTED.md) for step-by-step installation and your first simulation.

**Already installed?** Try running an example:
```bash
python HGD/main.py json/hopper.json5
```

## 📋 Prerequisites

Before installing HGD, ensure you have:

- **Python 3.9 or newer** (Python 3.11+ recommended)
- **C++ compiler** (g++, Clang, or MSVC)
- **CMake 3.15+**
- **OpenMP** (for parallel execution)

<details>
<summary>📦 <b>Quick install commands for dependencies</b></summary>

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip g++ cmake libomp-dev
```

**macOS:**
```bash
brew install python cmake libomp
```

**Windows:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Install Visual Studio with C++ support
- Install CMake from [cmake.org](https://cmake.org/download/)

</details>

## 🔧 Installation

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/benjym/HGD.git
   cd HGD
   ```

2. **Install HGD and dependencies:**
   ```bash
   pip install -e .
   ```
   
   This command installs all required Python packages and compiles the C++ extension modules.

3. **Verify installation:**
   ```bash
   python -c "import HGD; print('HGD installed successfully!')"
   ```

4. **(Optional) Set up pre-commit hooks for development:**
   ```bash
   pre-commit install
   ```

## 🎯 Running Simulations

Run a simulation using a JSON5 configuration file:

```bash
python HGD/main.py json/<config_file>.json5
```

**Example:**
```bash
python HGD/main.py json/hopper.json5
```

The simulation parameters are stored in the JSON5 file. Default parameters are available in `json/defaults.json5`.

## 📚 Documentation & Resources

- **[Getting Started Guide](GETTING_STARTED.md)** - Complete installation and first simulation walkthrough
- **[Examples Guide](EXAMPLES.md)** - Detailed description of all example scenarios
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solutions to common problems
- **[API Documentation](https://benjym.github.io/HGD/)** - Comprehensive code reference
- **[Default Parameters](json/defaults.json5)** - All configurable parameters with defaults

## 💡 Example Simulations

HGD includes several example configurations:

| Example | Description | Runtime |
|---------|-------------|---------|
| `hopper.json5` | Material flowing through a hopper | ~2 min |
| `collapse.json5` | Column collapse under gravity | ~1 min |
| `footing.json5` | Load bearing capacity test | ~3 min |
| `temperature.json5` | Thermal effects in flow | ~5 min |

See [EXAMPLES.md](EXAMPLES.md) for complete descriptions and usage instructions.

## 🔍 Viewing Results

After running a simulation, results are saved in the `output/` directory:

```
output/
└── <simulation_name>/
    ├── <parameter_set>/
    │   ├── nu_*.png      # Density snapshots
    │   ├── s_*.png       # Particle size snapshots
    │   ├── nu.mp4        # Density video
    │   └── s.mp4         # Particle size video
    └── ...
```

## 🛠️ Configuration

Simulations are configured using JSON5 files. Key parameters include:

```json5
{
    // Grid resolution
    nx: 50,              // Horizontal cells
    ny: 50,              // Vertical cells
    nm: 20,              // Internal states
    
    // Physical properties
    H: 1.0,              // System height (m)
    repose_angle: 30,    // Friction angle (degrees)
    s_m: 0.001,          // Min particle size (m)
    gsd_mode: 'bi',      // Grain size distribution
    
    // Simulation
    t_f: 5.0,            // Final time (s)
    save_inc: 1,         // Save frequency
    plot: ['nu', 's'],   // Variables to plot
}
```

See `json/defaults.json5` for all available parameters.

## ❓ Troubleshooting

**Installation fails?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues:
- C++ compiler not found
- CMake errors
- OpenMP missing
- Memory errors
- And more...

**Need help?** See the [Support](#-support) section below.

# Documentation

You can [read the docs here](https://benjym.github.io/HGD/).

# Support

You can contact the development team [here](https://matrix.to/#/!UZnyhaLhQymfFbLJYI:matrix.org?via=matrix.org).

# Authors

- [Benjy Marks](mailto:benjy.marks@sydney.edu.au)
- [Shivakumar Athani](mailto:shivakumar.athani@sydney.edu.au)
- [Jiahuan Li](mailto:jiahuan.li@sydney.edu.au)
