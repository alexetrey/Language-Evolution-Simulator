#!/usr/bin/env python3

import subprocess
import sys
import os

def install_requirements():
    print("Installing Language Evolution Simulator...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    return True

def main():
    print("Language Evolution Simulator - Installation Script")
    print("=" * 50)
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    if install_requirements():
        print("\n🎉 Installation complete!")
        print("\nTo run the simulator:")
        print("  python language_evolution_simulator.py")
        print("\nTo run tests:")
        print("  python test_simulator.py")
        print("\nTo try different scenarios:")
        print("  python example_scenarios.py")
    else:
        print("\n❌ Installation failed!")

if __name__ == "__main__":
    main()
