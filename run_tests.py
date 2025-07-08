#!/usr/bin/env python3
"""
Run automated tests against the ZER OpenAPI specification
"""
import subprocess
import sys

def run_schemathesis():
    """Run Schemathesis property-based tests"""
    print("=" * 60)
    print("Running Schemathesis Tests (Property-based fuzzing)")
    print("=" * 60)
    
    cmd = [
        "schemathesis", "run",
        "zer_search_openapi.yaml",
        "--url=https://zer.bzst.de/api/v1",
        "--checks", "all",
        "--max-examples", "50"
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode

def install_dredd():
    """Check if Dredd is installed"""
    try:
        subprocess.run(["dredd", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\nDredd is not installed. To install it, run:")
        print("  npm install -g dredd")
        print("  or")
        print("  npx dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1")
        return False

def run_dredd():
    """Run Dredd contract tests"""
    print("\n" + "=" * 60)
    print("Running Dredd Tests (Contract validation)")
    print("=" * 60)
    
    if not install_dredd():
        return 1
    
    cmd = [
        "dredd",
        "zer_search_openapi.yaml",
        "https://zer.bzst.de/api/v1",
        "--sorted",
        "--details"
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode

def main():
    """Run all tests"""
    print("OpenAPI Testing Suite for ZER API")
    print("=" * 60)
    
    # Run Schemathesis
    schemathesis_result = run_schemathesis()
    
    # Run Dredd
    dredd_result = run_dredd()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    print(f"Schemathesis: {'PASSED' if schemathesis_result == 0 else 'FAILED'}")
    print(f"Dredd: {'PASSED' if dredd_result == 0 else 'FAILED'}")
    
    # Exit with failure if any test failed
    sys.exit(max(schemathesis_result, dredd_result))

if __name__ == "__main__":
    main()