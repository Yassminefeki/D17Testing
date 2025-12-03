#!/usr/bin/env python3
"""
Master script to generate all acceptance criteria and create a comprehensive report.
Run this script to generate/update acceptance criteria for all test folders.
"""

import os
import sys
from pathlib import Path

def main():
    """Main execution."""
    print("=" * 80)
    print("ANDROID TEST SUITE — User Story & Acceptance Criteria Generator")
    print("=" * 80)
    
    base_path = Path(__file__).parent
    
    test_folders = [
        "Android/test_de_securite",
        "Android/test_de_performance",
        "Android/test_d_utilisabilite",
        "Android/test_de_compatibilite",
        "Android/test_de_connectivite",
        "Android/test_d_integration",
    ]
    
    print("\n📋 Generating acceptance criteria...\n")
    
    generated_count = 0
    for folder in test_folders:
        folder_path = base_path / folder
        script_path = folder_path / "generate_acceptance_criteria.py"
        
        if script_path.exists():
            try:
                # Import and execute the generation script
                import importlib.util
                spec = importlib.util.spec_from_file_location("gen_criteria", script_path)
                module = importlib.util.module_from_spec(spec)
                
                # Change to folder directory before running
                original_cwd = os.getcwd()
                os.chdir(str(folder_path))
                
                spec.loader.exec_module(module)
                
                os.chdir(original_cwd)
                generated_count += 1
                print(f"  ✓ {folder}")
            except Exception as e:
                print(f"  ✗ {folder} — Error: {e}")
        else:
            print(f"  ⊘ {folder} — Script not found")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nGenerated: {generated_count}/{len(test_folders)} acceptance criteria files\n")
    
    # List all generated files
    print("Generated files:")
    for folder in test_folders:
        criteria_file = base_path / folder / "acceptance_criteria.md"
        if criteria_file.exists():
            size = criteria_file.stat().st_size
            print(f"  ✓ {folder}/acceptance_criteria.md ({size} bytes)")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. **Review User Stories**: Check each user_stories.md file
   - Ensure stories follow "As a ... I want ... so that ..." format
   - Refine and add more stories as needed

2. **Review Acceptance Criteria**: Check each acceptance_criteria.md file
   - Verify Given/When/Then format
   - Adjust metrics and thresholds based on requirements
   - Add more criteria if needed

3. **Create Jira Tickets**: Use the user stories and criteria
   - Copy stories to ticket descriptions
   - Add acceptance criteria as task checklist
   - Set priorities and story points

4. **Automate Tests**: Implement test cases for each criterion
   - Security tests: pytest with security assertions
   - Performance tests: load testing with JMeter/Locust
   - Usability tests: manual or Selenium tests
   - Compatibility tests: Android emulator/device matrix
   - Connectivity tests: network simulation tools
   - Integration tests: API mocking and test fixtures

5. **Fine-tune**: Iterate on stories and criteria based on feedback
   - Re-run this generator after updates
   - Maintain version control for story changes
    """)
    print("=" * 80)

if __name__ == "__main__":
    main()
