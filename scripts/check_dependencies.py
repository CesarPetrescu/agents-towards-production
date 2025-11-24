#!/usr/bin/env python3
"""
Script to check for dependency conflicts across all tutorials in the repository.
"""
import os
from pathlib import Path


def check_dependency_conflicts():
    """Check for dependency conflicts across all tutorials"""
    tutorials_dir = Path("/workspace/tutorials")
    requirements_files = list(tutorials_dir.rglob("requirements.txt"))
    
    all_deps = {}
    conflicts = []
    
    print(f"Found {len(requirements_files)} requirements.txt files to analyze...")
    
    for req_file in requirements_files:
        print(f"Analyzing: {req_file}")
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('http'):
                    # Handle different version specifiers
                    if '==' in line:
                        pkg, version = line.split('==', 1)
                        pkg_key = pkg.lower().strip()  # Normalize package name
                        if pkg_key in all_deps and all_deps[pkg_key] != version:
                            conflicts.append({
                                'package': pkg,
                                'version1': all_deps[pkg_key],
                                'version2': version,
                                'files': [all_deps[f"{pkg_key}_file"], str(req_file)]
                            })
                        else:
                            all_deps[pkg_key] = version
                            all_deps[f"{pkg_key}_file"] = str(req_file)
                    elif '>=' in line or '<=' in line or '>' in line or '<' in line or '~=' in line:
                        # Handle other version specifiers
                        pkg = line.split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('~=')[0].split('!=')[0].strip()
                        pkg_key = pkg.lower().strip()
                        if pkg_key not in all_deps:
                            all_deps[pkg_key] = line
                            all_deps[f"{pkg_key}_file"] = str(req_file)
    
    print(f"\nAnalyzing {len(all_deps)} unique packages...")
    
    if conflicts:
        print("\nDependency conflicts found:")
        for conflict in conflicts:
            print(f"  {conflict['package']}: {conflict['version1']} vs {conflict['version2']}")
            print(f"    Files: {', '.join(conflict['files'])}")
        print(f"\nTotal conflicts: {len(conflicts)}")
        return conflicts
    else:
        print("\nNo dependency conflicts found!")
        return []


def main():
    conflicts = check_dependency_conflicts()
    if conflicts:
        print("\nRecommendation: Consider creating a centralized dependency management system.")
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())