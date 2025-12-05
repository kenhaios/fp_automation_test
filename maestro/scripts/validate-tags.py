#!/usr/bin/env python3
"""
Maestro Test Tag Validation Script
Validates that all test files have required tags and follow naming conventions
"""

import os
import yaml
import sys
from pathlib import Path

# Required tags for different file types
REQUIRED_TAGS_TESTS = ['feature', 'test-type', 'priority', 'platform']
REQUIRED_TAGS_SHARED = ['platform']  # Shared components have minimal requirements
REQUIRED_TAGS_QUALITY_GATES = ['platform']  # Quality gates have minimal requirements
REQUIRED_TAGS_TEST_SUITES = ['platform']  # Test suites have minimal requirements

# Valid values for specific tags
VALID_PLATFORMS = ['ios', 'android']
VALID_TEST_TYPES = ['happy-path', 'negative', 'edge-case']
VALID_PRIORITIES = ['p0', 'p1', 'p2', 'p3']

# Colors for output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    """Print colored message"""
    print(f"{color}{message}{Colors.END}")

def extract_tags_from_content(content):
    """Extract tags from YAML content"""
    try:
        # Split by '---' to get the header section
        parts = content.split('---')
        if len(parts) < 2:
            return []
        
        header = parts[0]
        data = yaml.safe_load(header)
        
        if not data or 'tags' not in data:
            return []
            
        return data.get('tags', [])
    except yaml.YAMLError as e:
        print_colored(f"YAML parsing error: {e}", Colors.RED)
        return []

def get_file_type(filepath):
    """Determine the file type based on path"""
    path_str = str(filepath)
    
    if 'shared-components' in path_str:
        return 'shared'
    elif 'quality-gates' in path_str:
        return 'quality-gate'
    elif 'test-suites' in path_str:
        return 'test-suite'
    else:
        return 'test'

def get_required_tags(file_type):
    """Get required tags based on file type"""
    if file_type == 'shared':
        return REQUIRED_TAGS_SHARED
    elif file_type == 'quality-gate':
        return REQUIRED_TAGS_QUALITY_GATES
    elif file_type == 'test-suite':
        return REQUIRED_TAGS_TEST_SUITES
    else:
        return REQUIRED_TAGS_TESTS

def validate_file(filepath):
    """Validate a single test file"""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"], []
    
    # Extract tags
    tags = extract_tags_from_content(content)
    
    if not tags:
        errors.append("No tags found")
        return errors, warnings
    
    # Convert tags to dict for easier processing
    tag_dict = {}
    for tag in tags:
        if ':' in tag:
            key, value = tag.split(':', 1)
            if key not in tag_dict:
                tag_dict[key] = []
            tag_dict[key].append(value)
        else:
            # Handle tags without values (like 'shared')
            tag_dict[tag] = True
    
    # Determine file type and get required tags
    file_type = get_file_type(filepath)
    required_tags = get_required_tags(file_type)
    
    # Check required tags
    for required_tag in required_tags:
        if required_tag not in tag_dict:
            errors.append(f"Missing required tag: {required_tag}")
    
    # Validate platform tags
    if 'platform' in tag_dict:
        platforms = tag_dict['platform']
        for platform in platforms:
            if platform not in VALID_PLATFORMS:
                warnings.append(f"Unknown platform: {platform}")
    
    # Validate test-type
    if 'test-type' in tag_dict:
        test_types = tag_dict['test-type']
        for test_type in test_types:
            if test_type not in VALID_TEST_TYPES:
                warnings.append(f"Unknown test-type: {test_type}")
    
    # Validate priority
    if 'priority' in tag_dict:
        priorities = tag_dict['priority']
        for priority in priorities:
            if priority not in VALID_PRIORITIES:
                warnings.append(f"Unknown priority: {priority}")
    
    # Check file naming convention
    filename = os.path.basename(filepath)
    if filename.endswith('-ios.yaml'):
        if 'platform' in tag_dict and 'ios' not in tag_dict['platform']:
            errors.append("iOS file suffix but no ios platform tag")
    elif filename.endswith('-android.yaml'):
        if 'platform' in tag_dict and 'android' not in tag_dict['platform']:
            errors.append("Android file suffix but no android platform tag")
    else:
        # Cross-platform file should have both platform tags
        if 'platform' in tag_dict:
            platforms = tag_dict['platform']
            if len(platforms) == 1:
                warnings.append(f"Cross-platform file has only {platforms[0]} tag")
    
    return errors, warnings

def find_test_files(directory):
    """Find all YAML test files"""
    test_files = []
    flows_dir = Path(directory) / 'flows'
    
    if not flows_dir.exists():
        print_colored(f"Flows directory not found: {flows_dir}", Colors.RED)
        return []
    
    # Find all .yaml files in flows directory
    for yaml_file in flows_dir.rglob('*.yaml'):
        # Skip hidden files and directories
        if not any(part.startswith('.') for part in yaml_file.parts):
            test_files.append(yaml_file)
    
    return test_files

def main():
    """Main validation function"""
    print_colored("Maestro Test Tag Validation", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)
    
    # Get maestro directory (current directory)
    maestro_dir = Path.cwd()
    
    # Find test files
    test_files = find_test_files(maestro_dir)
    
    if not test_files:
        print_colored("No test files found!", Colors.RED)
        sys.exit(1)
    
    print_colored(f"Found {len(test_files)} test files", Colors.BLUE)
    print()
    
    total_errors = 0
    total_warnings = 0
    files_with_errors = 0
    files_with_warnings = 0
    
    for test_file in sorted(test_files):
        relative_path = test_file.relative_to(maestro_dir)
        errors, warnings = validate_file(test_file)
        
        if errors or warnings:
            print_colored(f"File: {relative_path}", Colors.BOLD)
            
            if errors:
                files_with_errors += 1
                total_errors += len(errors)
                for error in errors:
                    print_colored(f"  ❌ ERROR: {error}", Colors.RED)
            
            if warnings:
                files_with_warnings += 1
                total_warnings += len(warnings)
                for warning in warnings:
                    print_colored(f"  ⚠️  WARNING: {warning}", Colors.YELLOW)
            
            print()
    
    # Summary
    print_colored("Validation Summary", Colors.BOLD + Colors.BLUE)
    print_colored("-" * 30, Colors.BLUE)
    print_colored(f"Total files checked: {len(test_files)}", Colors.BLUE)
    print_colored(f"Files with errors: {files_with_errors}", Colors.RED if files_with_errors > 0 else Colors.GREEN)
    print_colored(f"Files with warnings: {files_with_warnings}", Colors.YELLOW if files_with_warnings > 0 else Colors.GREEN)
    print_colored(f"Total errors: {total_errors}", Colors.RED if total_errors > 0 else Colors.GREEN)
    print_colored(f"Total warnings: {total_warnings}", Colors.YELLOW if total_warnings > 0 else Colors.GREEN)
    
    if total_errors == 0 and total_warnings == 0:
        print_colored("✅ All tests passed validation!", Colors.GREEN)
    elif total_errors == 0:
        print_colored("✅ No errors found, but there are warnings to review", Colors.YELLOW)
    else:
        print_colored("❌ Validation failed - errors found", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()