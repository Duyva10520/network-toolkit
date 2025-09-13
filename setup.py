#!/usr/bin/env python3
"""
Setup script for Network Toolkit
"""

import sys
import platform

def check_requirements():
    """Kiểm tra requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {python_version.major}.{python_version.minor}")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check OS
    os_name = platform.system()
    print(f"✅ Operating System: {os_name} {platform.release()}")
    
    # Check required modules (all standard library)
    required_modules = [
        'socket', 'subprocess', 'platform', 'time', 
        'threading', 'concurrent.futures', 'json', 
        'sys', 'os', 'datetime', 'typing', 'webbrowser'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module: {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ Module: {module}")
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        return False
    
    print("\n🎉 All requirements satisfied!")
    return True

def main():
    """Main setup function"""
    print("🌐 NETWORK TOOLKIT SETUP")
    print("=" * 40)
    
    if not check_requirements():
        print("\n❌ Setup failed. Please fix requirements.")
        sys.exit(1)
    
    print("\n🚀 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run: python network_toolkit.py")
    print("   2. Choose from 14 available options")
    print("   3. Export results to CSV/HTML")
    print("\n💡 Tips:")
    print("   • Start with Quick Test (option 1)")
    print("   • Use HTML reports for presentations")
    print("   • Check CSV Help (option 14) for analysis")
    print("\n🎯 Enjoy using Network Toolkit!")

if __name__ == "__main__":
    main()