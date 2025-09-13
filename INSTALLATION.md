# Installation Guide - Network Toolkit

## 🎯 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, Linux, macOS 10.14+
- **Memory**: 50MB RAM
- **Storage**: 10MB free space
- **Network**: Internet connection for testing

### Recommended Requirements
- **Python**: 3.9 or higher
- **Memory**: 100MB RAM
- **Storage**: 50MB free space (for logs and reports)

## 🚀 Installation Methods

### Method 1: Direct Download (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/network-toolkit.git
cd network-toolkit

# Verify Python version
python --version  # Should be 3.8+

# Run setup check
python setup.py

# Start using
python network_toolkit.py
```

### Method 2: Download ZIP
1. Go to GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desired folder
4. Open terminal in extracted folder
5. Run `python network_toolkit.py`

### Method 3: Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_executable.py

# Run executable
./dist/network-toolkit  # Linux/Mac
# or
dist\network-toolkit.exe  # Windows
```

## 🔧 Platform-Specific Instructions

### Windows Installation

#### Prerequisites Check
```cmd
# Check Python version
python --version

# If Python not found, download from python.org
# Make sure to check "Add Python to PATH"
```

#### Installation Steps
```cmd
# Method 1: Git (if Git is installed)
git clone https://github.com/yourusername/network-toolkit.git
cd network-toolkit
python setup.py
python network_toolkit.py

# Method 2: Direct download
# Download ZIP from GitHub
# Extract to C:\Tools\network-toolkit\
# Open Command Prompt in that folder
python network_toolkit.py
```

#### Windows-Specific Features
- Uses `tracert` instead of `traceroute`
- Uses `ipconfig` for network info
- Uses `netstat` for statistics
- Supports Windows firewall detection

### Linux Installation

#### Prerequisites (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.7+ if not available
sudo apt install python3.7 python3-pip

# Verify installation
python3 --version
```

#### Prerequisites (CentOS/RHEL)
```bash
# Install Python 3.7+
sudo yum install python3 python3-pip
# or for newer versions
sudo dnf install python3 python3-pip
```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/yourusername/network-toolkit.git
cd network-toolkit

# Make executable (optional)
chmod +x network_toolkit.py

# Run setup check
python3 setup.py

# Start using
python3 network_toolkit.py
```

#### Linux-Specific Features
- Uses native `traceroute` command
- Uses `ifconfig` or `ip` commands
- Supports `netstat` and modern `ss` command
- Better performance on Linux systems

### macOS Installation

#### Prerequisites
```bash
# Check if Python 3.7+ is installed
python3 --version

# If not, install via Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.9

# Or download from python.org
```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/yourusername/network-toolkit.git
cd network-toolkit

# Run setup check
python3 setup.py

# Start using
python3 network_toolkit.py
```

#### macOS-Specific Features
- Uses BSD-style network commands
- Compatible with macOS network stack
- Supports both Intel and Apple Silicon Macs

## 🔍 Verification Steps

### 1. Python Version Check
```bash
python --version
# Should output: Python 3.8.x or higher
```

### 2. Dependencies Check
```bash
python setup.py
# Should show all green checkmarks
```

### 3. Basic Functionality Test
```bash
python network_toolkit.py
# Choose option 1 (Quick Test)
# Should complete in ~30 seconds
```

### 4. Export Test
```bash
# After running a test:
# Choose option 12 (Export HTML)
# Should create HTML file and offer to open in browser
```

## 🛠️ Troubleshooting

### Common Issues

#### "Python not found"
**Solution:**
- Windows: Reinstall Python with "Add to PATH" checked
- Linux: Install python3 package
- macOS: Install via Homebrew or python.org

#### "Permission denied"
**Solution:**
```bash
# Linux/macOS: Add execute permission
chmod +x network_toolkit.py

# Windows: Run as Administrator if needed
```

#### "Module not found"
**Solution:**
- All modules are standard library
- Check Python version (must be 3.8+)
- Try: `python -c "import socket, subprocess, platform"`

#### Network tests fail
**Solution:**
- Check internet connection
- Disable VPN temporarily
- Check firewall settings
- Try different DNS servers

#### Traceroute timeout
**Solution:**
- Normal behavior for some networks
- Try reducing hop count
- Check if traceroute is blocked by firewall

### Performance Issues

#### Slow execution
**Causes & Solutions:**
- **Slow network**: Normal, tests depend on network speed
- **Firewall blocking**: Configure firewall to allow Python
- **Antivirus interference**: Add exception for Python/toolkit
- **Limited resources**: Close other applications

#### High memory usage
**Solutions:**
- Normal usage is <50MB
- Clear old log files if many sessions
- Restart if memory keeps growing

## 📦 Distribution Options

### For End Users
1. **Portable**: Single Python file, no installation needed
2. **Executable**: Pre-built binary for each platform
3. **Installer**: Automated installation with shortcuts

### For Developers
1. **Source Code**: Full access to modify and extend
2. **Git Repository**: Version control and collaboration
3. **Build System**: Create custom distributions

## 🔄 Updates and Maintenance

### Checking for Updates
```bash
# Check current version
python -c "from network_toolkit import __version__; print(__version__)"

# Check GitHub for latest release
# Compare with VERSION file in repository
```

### Updating
```bash
# Git method
git pull origin main

# Manual method
# Download latest ZIP and replace files
```

### Backup
```bash
# Backup your logs and reports
cp network_toolkit_*.* backup/

# Backup custom configurations (if any)
```

## 📞 Support

### Getting Help
- **Documentation**: Read README.md and FEATURES.md
- **Quick Start**: Follow QUICK_START.md
- **Issues**: GitHub Issues for bug reports
- **Email**: support@networktoolkit.com

### Before Reporting Issues
1. Check Python version (3.7+)
2. Run `python setup.py` to verify setup
3. Try Quick Test to isolate issues
4. Check firewall/antivirus settings
5. Include error messages and system info

---

**Ready to start?** Follow the installation method that works best for your system! 🚀