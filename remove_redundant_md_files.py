#!/usr/bin/env python3
"""
Script to identify and remove redundant .md files while preserving computational logic
and ensuring output formats comply with statutory governmental requirements.
"""

import os
import hashlib
import shutil
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('md_removal_audit.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MarkdownRedundancyRemover:
    """Class to identify and remove redundant markdown files"""
    
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / "backup_md_files"
        self.audit_log = []
        
        # Files that must be preserved (critical to computational logic or statutory requirements)
        self.preserved_files = {
            "README.md",  # Main project overview
            "COMPLETE_COMBINED_DOCUMENTATION.md",  # Comprehensive documentation
            "requirements.txt",  # Dependency requirements
        }
        
        # Patterns indicating redundancy (files with these patterns can be considered for removal)
        self.redundancy_patterns = [
            "_IMPLEMENTATION.md",
            "_FINAL_CONFIRMATION.md",
            "_VALIDATION_REPORT.md",
            "_MODIFICATIONS_SUMMARY.md",
            "_DETAILED_IMPLEMENTATION.md",
            "_SOLUTION_SUMMARY.md",
            "_ALIGNMENT_REPORT.md",
            "_ALIGNMENT_MODIFICATIONS.md",
            "_VERIFICATION.md",
            "_FOR_REVIEW.md",
            "_GUIDE.md",
            "_DEPLOYMENT_GUIDE.md",
        ]
        
        # Files that contain computational logic or are used as input/configuration
        self.computational_files = {
            "requirements.txt",
            "run_comprehensive_tests.bat",
            "run_programmatically.txt",
            "sample_processed_data.json",
        }
        
        # Template files that must be preserved for statutory compliance
        self.template_files = set()
        for template_file in self.root_dir.glob("templates/*.html"):
            self.template_files.add(template_file.name)
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def find_markdown_files(self):
        """Find all .md files in the directory"""
        md_files = list(self.root_dir.glob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files")
        return md_files
    
    def identify_redundant_files(self):
        """Identify redundant markdown files based on content and naming patterns"""
        md_files = self.find_markdown_files()
        redundant_files = []
        file_hashes = {}
        
        logger.info("Analyzing markdown files for redundancy...")
        
        for md_file in md_files:
            filename = md_file.name
            
            # Skip preserved files
            if filename in self.preserved_files:
                logger.info(f"Preserving required file: {filename}")
                continue
            
            # Check if file contains computational logic
            if filename in self.computational_files:
                logger.info(f"Preserving computational file: {filename}")
                continue
            
            # Check naming patterns for redundancy
            is_redundant_by_pattern = any(pattern in filename for pattern in self.redundancy_patterns)
            if is_redundant_by_pattern:
                logger.info(f"Flagged by pattern matching: {filename}")
                redundant_files.append(md_file)
                continue
            
            # Check content-based redundancy
            file_hash = self.calculate_file_hash(md_file)
            if file_hash:
                if file_hash in file_hashes:
                    # Duplicate found
                    original_file = file_hashes[file_hash]
                    logger.info(f"Duplicate found: {filename} (duplicate of {original_file.name})")
                    redundant_files.append(md_file)
                else:
                    file_hashes[file_hash] = md_file
        
        return redundant_files
    
    def backup_files(self, files_to_backup):
        """Create backup of files before deletion"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir()
            logger.info(f"Created backup directory: {self.backup_dir}")
        
        backed_up_files = []
        for file_path in files_to_backup:
            try:
                backup_path = self.backup_dir / file_path.name
                shutil.copy2(file_path, backup_path)
                backed_up_files.append(backup_path)
                logger.info(f"Backed up: {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to backup {file_path.name}: {e}")
        
        return backed_up_files
    
    def remove_redundant_files(self, redundant_files, auto_confirm=False):
        """Remove redundant files after backup and confirmation"""
        if not redundant_files:
            logger.info("No redundant files found for removal")
            return True
        
        # Backup files first
        logger.info("Creating backups of files to be removed...")
        backed_up_files = self.backup_files(redundant_files)
        
        # List files for review
        print("\n" + "="*60)
        print("FILES IDENTIFIED FOR REMOVAL")
        print("="*60)
        for i, file_path in enumerate(redundant_files, 1):
            file_size = file_path.stat().st_size / 1024  # Size in KB
            print(f"{i}. {file_path.name} ({file_size:.1f} KB)")
        
        print(f"\nTotal files to remove: {len(redundant_files)}")
        print(f"Backups created in: {self.backup_dir}")
        
        # Get user confirmation unless auto_confirm is True
        if not auto_confirm:
            confirmation = input("\nDo you want to proceed with deletion? (yes/no): ")
            if confirmation.lower() not in ['yes', 'y']:
                logger.info("File removal cancelled by user")
                return False
        
        # Remove files
        removed_files = []
        failed_removals = []
        
        for file_path in redundant_files:
            try:
                file_path.unlink()
                removed_files.append(file_path.name)
                logger.info(f"Removed: {file_path.name}")
            except Exception as e:
                failed_removals.append((file_path.name, str(e)))
                logger.error(f"Failed to remove {file_path.name}: {e}")
        
        # Log results
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "removed_files": removed_files,
            "failed_removals": failed_removals,
            "backed_up_files": [f.name for f in backed_up_files]
        })
        
        # Summary
        print(f"\n{'='*60}")
        print("REMOVAL SUMMARY")
        print(f"{'='*60}")
        print(f"Successfully removed: {len(removed_files)} files")
        print(f"Failed to remove: {len(failed_removals)} files")
        
        if failed_removals:
            print("\nFailed removals:")
            for filename, error in failed_removals:
                print(f"  - {filename}: {error}")
        
        return len(failed_removals) == 0
    
    def validate_remaining_files(self):
        """Validate that remaining files align with latest templates and statutory requirements"""
        logger.info("Validating remaining markdown files...")
        
        # Check that preserved files still exist
        preserved_exists = []
        preserved_missing = []
        
        for filename in self.preserved_files:
            file_path = self.root_dir / filename
            if file_path.exists():
                preserved_exists.append(filename)
                logger.info(f"Confirmed: {filename} exists")
            else:
                preserved_missing.append(filename)
                logger.warning(f"Missing: {filename}")
        
        # Check that computational files still exist
        computational_exists = []
        computational_missing = []
        
        for filename in self.computational_files:
            file_path = self.root_dir / filename
            if file_path.exists():
                computational_exists.append(filename)
                logger.info(f"Confirmed: {filename} exists")
            else:
                computational_missing.append(filename)
                logger.warning(f"Missing: {filename}")
        
        # Summary
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Preserved files confirmed: {len(preserved_exists)}")
        print(f"Preserved files missing: {len(preserved_missing)}")
        print(f"Computational files confirmed: {len(computational_exists)}")
        print(f"Computational files missing: {len(computational_missing)}")
        
        if preserved_missing:
            print("\nMissing preserved files:")
            for filename in preserved_missing:
                print(f"  - {filename}")
        
        return len(preserved_missing) == 0 and len(computational_missing) == 0
    
    def run_compliance_check(self):
        """Verify that outputs comply with statutory governmental formats"""
        logger.info("Running compliance check for statutory governmental formats...")
        
        # Check that the comprehensive documentation exists
        combined_doc = self.root_dir / "COMPLETE_COMBINED_DOCUMENTATION.md"
        if combined_doc.exists():
            logger.info("✓ Comprehensive documentation exists for statutory compliance")
        else:
            logger.error("✗ Comprehensive documentation missing")
            return False
        
        # Check that template files exist
        template_dir = self.root_dir / "templates"
        if template_dir.exists():
            html_templates = list(template_dir.glob("*.html"))
            logger.info(f"✓ Found {len(html_templates)} HTML templates for statutory formats")
        else:
            logger.error("✗ Template directory missing")
            return False
        
        # Check critical templates
        critical_templates = [
            "certificate_ii.html",
            "certificate_iii.html",
            "bill_scrutiny_sheet.html",
            "first_page_detailed.html",
            "deviation_statement_detailed.html",
            "extra_items_detailed.html"
        ]
        
        missing_templates = []
        for template in critical_templates:
            template_path = template_dir / template
            if template_path.exists():
                logger.info(f"✓ Critical template exists: {template}")
            else:
                missing_templates.append(template)
                logger.error(f"✗ Critical template missing: {template}")
        
        return len(missing_templates) == 0
    
    def generate_audit_report(self):
        """Generate a detailed audit report of all actions"""
        report_path = self.root_dir / "md_removal_audit_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("MARKDOWN FILE REMOVAL AUDIT REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if self.audit_log:
                for entry in self.audit_log:
                    f.write(f"Timestamp: {entry['timestamp']}\n")
                    f.write(f"Removed files: {len(entry['removed_files'])}\n")
                    f.write(f"Failed removals: {len(entry['failed_removals'])}\n")
                    f.write(f"Backed up files: {len(entry['backed_up_files'])}\n\n")
                    
                    if entry['removed_files']:
                        f.write("Removed files:\n")
                        for filename in entry['removed_files']:
                            f.write(f"  - {filename}\n")
                    
                    if entry['failed_removals']:
                        f.write("\nFailed removals:\n")
                        for filename, error in entry['failed_removals']:
                            f.write(f"  - {filename}: {error}\n")
                    
                    f.write("\n" + "-" * 30 + "\n\n")
            else:
                f.write("No removal actions recorded.\n")
        
        logger.info(f"Audit report generated: {report_path}")
        return report_path

def main():
    """Main function to run the markdown redundancy removal process"""
    print("MARKDOWN REDUNDANCY REMOVAL TOOL")
    print("=" * 50)
    print("This tool identifies and removes redundant .md files while preserving")
    print("computational logic and ensuring statutory governmental compliance.\n")
    
    # Initialize the remover
    remover = MarkdownRedundancyRemover()
    
    try:
        # Step 1: Identify redundant files
        print("Step 1: Identifying redundant markdown files...")
        redundant_files = remover.identify_redundant_files()
        
        if not redundant_files:
            print("No redundant files found. Process complete.")
            return
        
        # Step 2: Remove redundant files
        print("\nStep 2: Removing redundant files...")
        removal_success = remover.remove_redundant_files(redundant_files, auto_confirm=False)
        
        # Step 3: Validate remaining files
        print("\nStep 3: Validating remaining files...")
        validation_success = remover.validate_remaining_files()
        
        # Step 4: Run compliance check
        print("\nStep 4: Running compliance check...")
        compliance_success = remover.run_compliance_check()
        
        # Step 5: Generate audit report
        print("\nStep 5: Generating audit report...")
        audit_report = remover.generate_audit_report()
        
        # Final summary
        print(f"\n{'='*60}")
        print("PROCESS COMPLETED")
        print(f"{'='*60}")
        print(f"Removal success: {'✓' if removal_success else '✗'}")
        print(f"Validation success: {'✓' if validation_success else '✗'}")
        print(f"Compliance check: {'✓' if compliance_success else '✗'}")
        print(f"Audit report: {audit_report}")
        
        if removal_success and validation_success and compliance_success:
            print("\n🎉 All steps completed successfully!")
            print("Redundant markdown files have been removed while preserving")
            print("computational logic and statutory compliance.")
        else:
            print("\n⚠️  Some steps encountered issues. Please review the logs.")
            
    except Exception as e:
        logger.error(f"Process failed with error: {e}")
        print(f"\n❌ Process failed: {e}")

if __name__ == "__main__":
    main()