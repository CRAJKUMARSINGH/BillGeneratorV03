#!/usr/bin/env python3
"""
Multi-Project BillGenerator Synchronization Script
Applies optimizations and synchronizes all BillGenerator projects

Author: RAJKUMAR SINGH CHAUHAN
Email: crajkumarsingh@hotmail.com
Version: 1.0
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiBillGeneratorManager:
    """Manages optimization and synchronization across all BillGenerator projects"""
    
    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Detect user directory
            self.base_path = Path.home()
        
        self.projects = self.discover_billgenerator_projects()
        self.results = {}
        
    def discover_billgenerator_projects(self) -> List[Path]:
        """Discover all BillGenerator projects"""
        projects = []
        
        # Look for BillGenerator* directories
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name.startswith('BillGenerator'):
                projects.append(item)
                logger.info(f"Discovered project: {item.name}")
        
        return sorted(projects)
    
    def check_git_repositories(self):
        """Check Git status for all projects"""
        git_status = {}
        
        for project in self.projects:
            project_status = {
                "has_git": False,
                "is_repo": False,
                "remote_configured": False,
                "remote_url": None,
                "current_branch": None,
                "status_clean": False
            }
            
            try:
                # Check if .git directory exists
                git_dir = project / ".git"
                project_status["has_git"] = git_dir.exists()
                
                if project_status["has_git"]:
                    project_status["is_repo"] = True
                    
                    # Get remote URL
                    try:
                        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                              cwd=project, capture_output=True, text=True)
                        if result.returncode == 0:
                            project_status["remote_configured"] = True
                            project_status["remote_url"] = result.stdout.strip()
                    except:
                        pass
                    
                    # Get current branch
                    try:
                        result = subprocess.run(['git', 'branch', '--show-current'], 
                                              cwd=project, capture_output=True, text=True)
                        if result.returncode == 0:
                            project_status["current_branch"] = result.stdout.strip()
                    except:
                        pass
                    
                    # Check if status is clean
                    try:
                        result = subprocess.run(['git', 'status', '--porcelain'], 
                                              cwd=project, capture_output=True, text=True)
                        if result.returncode == 0:
                            project_status["status_clean"] = len(result.stdout.strip()) == 0
                    except:
                        pass
                        
            except Exception as e:
                logger.warning(f"Error checking Git status for {project.name}: {e}")
            
            git_status[project.name] = project_status
        
        return git_status
    
    def configure_git_for_all_projects(self):
        """Configure Git for all projects"""
        configured_projects = []
        
        for project in self.projects:
            try:
                # Configure user
                subprocess.run(['git', 'config', 'user.email', 'crajkumarsingh@hotmail.com'], 
                             cwd=project, check=True)
                subprocess.run(['git', 'config', 'user.name', 'RAJKUMAR SINGH CHAUHAN'], 
                             cwd=project, check=True)
                
                configured_projects.append(project.name)
                logger.info(f"Git configured for {project.name}")
                
            except Exception as e:
                logger.error(f"Failed to configure Git for {project.name}: {e}")
        
        return configured_projects
    
    def copy_optimization_files(self):
        """Copy optimization files to all projects"""
        source_project = None
        
        # Find the most complete project (likely V03)
        for project in self.projects:
            if 'V03' in project.name or 'v03' in project.name:
                source_project = project
                break
        
        if not source_project:
            source_project = self.projects[-1]  # Use the last one
        
        optimization_files = [
            "comprehensive_optimizer.py",
            "README_RAJKUMAR.md",
            "bug removal prompt GENERAL.md",
            "requirements.txt"
        ]
        
        copied_files = {}
        
        for target_project in self.projects:
            if target_project == source_project:
                continue
                
            copied_files[target_project.name] = []
            
            for filename in optimization_files:
                source_file = source_project / filename
                target_file = target_project / filename
                
                if source_file.exists():
                    try:
                        # Read source content
                        with open(source_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Adapt content for target project
                        content = content.replace(source_project.name, target_project.name)
                        
                        # Write to target
                        with open(target_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        copied_files[target_project.name].append(filename)
                        logger.info(f"Copied {filename} to {target_project.name}")
                        
                    except Exception as e:
                        logger.error(f"Failed to copy {filename} to {target_project.name}: {e}")
        
        return copied_files
    
    def run_optimization_for_all(self):
        """Run optimization for all projects"""
        optimization_results = {}
        
        for project in self.projects:
            logger.info(f"Running optimization for {project.name}")
            
            try:
                # Import and run the optimizer
                sys.path.insert(0, str(project))
                
                optimizer_script = project / "comprehensive_optimizer.py"
                if optimizer_script.exists():
                    # Run the optimizer
                    result = subprocess.run([sys.executable, str(optimizer_script)], 
                                          cwd=project, 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=300)
                    
                    optimization_results[project.name] = {
                        "success": result.returncode == 0,
                        "output": result.stdout,
                        "error": result.stderr
                    }
                else:
                    logger.warning(f"Optimizer script not found for {project.name}")
                    optimization_results[project.name] = {
                        "success": False,
                        "error": "Optimizer script not found"
                    }
                    
            except Exception as e:
                logger.error(f"Failed to run optimization for {project.name}: {e}")
                optimization_results[project.name] = {
                    "success": False,
                    "error": str(e)
                }
        
        return optimization_results
    
    def synchronize_repositories(self):
        """Synchronize all repositories with their remotes"""
        sync_results = {}
        
        for project in self.projects:
            logger.info(f"Synchronizing repository: {project.name}")
            
            sync_result = {
                "pulled": False,
                "committed": False, 
                "pushed": False,
                "errors": []
            }
            
            try:
                # Add all changes
                subprocess.run(['git', 'add', '.'], cwd=project, check=True)
                
                # Commit if there are changes
                commit_message = f"Applied comprehensive optimizations to {project.name}"
                result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                      cwd=project, capture_output=True)
                if result.returncode == 0:
                    sync_result["committed"] = True
                
                # Pull latest changes
                try:
                    subprocess.run(['git', 'pull', 'origin', 'main'], 
                                 cwd=project, check=True, capture_output=True)
                    sync_result["pulled"] = True
                except subprocess.CalledProcessError:
                    # Try master branch
                    try:
                        subprocess.run(['git', 'pull', 'origin', 'master'], 
                                     cwd=project, check=True, capture_output=True)
                        sync_result["pulled"] = True
                    except:
                        sync_result["errors"].append("Failed to pull from remote")
                
                # Push changes
                try:
                    subprocess.run(['git', 'push', 'origin', 'main'], 
                                 cwd=project, check=True, capture_output=True)
                    sync_result["pushed"] = True
                except subprocess.CalledProcessError:
                    # Try master branch
                    try:
                        subprocess.run(['git', 'push', 'origin', 'master'], 
                                     cwd=project, check=True, capture_output=True)
                        sync_result["pushed"] = True
                    except:
                        sync_result["errors"].append("Failed to push to remote")
                
            except Exception as e:
                sync_result["errors"].append(str(e))
            
            sync_results[project.name] = sync_result
        
        return sync_results
    
    def generate_comprehensive_report(self):
        """Generate comprehensive optimization and synchronization report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "developer": {
                "name": "RAJKUMAR SINGH CHAUHAN",
                "email": "crajkumarsingh@hotmail.com"
            },
            "projects_discovered": [p.name for p in self.projects],
            "total_projects": len(self.projects),
            "git_status": self.check_git_repositories(),
            "results": self.results
        }
        
        # Save report
        report_file = self.base_path / "BillGenerator_Optimization_Report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Comprehensive report saved to {report_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
        
        return report
    
    def run_complete_process(self):
        """Run the complete optimization and synchronization process"""
        logger.info("Starting complete BillGenerator optimization and synchronization process")
        
        # Step 1: Check Git repositories
        logger.info("Step 1: Checking Git repositories")
        git_status = self.check_git_repositories()
        self.results["git_status"] = git_status
        
        # Step 2: Configure Git for all projects
        logger.info("Step 2: Configuring Git for all projects")
        configured_projects = self.configure_git_for_all_projects()
        self.results["configured_projects"] = configured_projects
        
        # Step 3: Copy optimization files
        logger.info("Step 3: Copying optimization files")
        copied_files = self.copy_optimization_files()
        self.results["copied_files"] = copied_files
        
        # Step 4: Run optimization for all projects
        logger.info("Step 4: Running optimization for all projects")
        optimization_results = self.run_optimization_for_all()
        self.results["optimization_results"] = optimization_results
        
        # Step 5: Synchronize repositories
        logger.info("Step 5: Synchronizing repositories")
        sync_results = self.synchronize_repositories()
        self.results["sync_results"] = sync_results
        
        # Step 6: Generate comprehensive report
        logger.info("Step 6: Generating comprehensive report")
        report = self.generate_comprehensive_report()
        
        return report

def main():
    """Main function"""
    print("🏗️ Multi-Project BillGenerator Optimization & Synchronization")
    print("=" * 60)
    
    # Get base path from command line or use default
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = str(Path.home())
    
    manager = MultiBillGeneratorManager(base_path)
    
    if not manager.projects:
        print("❌ No BillGenerator projects found!")
        print(f"Searched in: {base_path}")
        sys.exit(1)
    
    print(f"📁 Found {len(manager.projects)} BillGenerator projects:")
    for project in manager.projects:
        print(f"  • {project.name}")
    
    print("\n🚀 Starting optimization process...")
    
    try:
        report = manager.run_complete_process()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 OPTIMIZATION & SYNCHRONIZATION SUMMARY")
        print("="*60)
        
        print(f"✅ Projects processed: {report['total_projects']}")
        print(f"✅ Git configured for: {len(report['results']['configured_projects'])} projects")
        
        # Optimization results
        optimization_results = report['results']['optimization_results']
        successful_optimizations = sum(1 for r in optimization_results.values() if r['success'])
        print(f"✅ Successful optimizations: {successful_optimizations}/{len(optimization_results)}")
        
        # Sync results  
        sync_results = report['results']['sync_results']
        successful_syncs = sum(1 for r in sync_results.values() 
                             if r['committed'] and r['pushed'])
        print(f"✅ Successful synchronizations: {successful_syncs}/{len(sync_results)}")
        
        print(f"\n📄 Detailed report saved to: BillGenerator_Optimization_Report.json")
        print("\n🎉 Process completed successfully!")
        
        # Print project-specific results
        print("\n📋 Project Details:")
        for project_name in manager.projects:
            project_name = project_name.name
            print(f"\n  🏗️ {project_name}:")
            
            if project_name in optimization_results:
                if optimization_results[project_name]['success']:
                    print(f"    ✅ Optimization: Success")
                else:
                    print(f"    ❌ Optimization: Failed")
            
            if project_name in sync_results:
                sync = sync_results[project_name]
                print(f"    📤 Committed: {'✅' if sync['committed'] else '❌'}")
                print(f"    🔄 Synced: {'✅' if sync['pushed'] else '❌'}")
        
    except Exception as e:
        logger.error(f"Process failed: {e}")
        print(f"\n❌ Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()