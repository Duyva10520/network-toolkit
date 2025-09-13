#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git setup script for Network Toolkit
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} thành công")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} thất bại")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi {description}: {e}")
        return False

def check_git():
    """Kiểm tra git có được cài đặt không"""
    return run_command("git --version", "Kiểm tra Git")

def setup_git_repo():
    """Setup git repository"""
    print("🌐 NETWORK TOOLKIT - GIT SETUP")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git():
        print("❌ Git chưa được cài đặt. Vui lòng cài đặt Git trước.")
        return False
    
    # Initialize git repo if not exists
    if not os.path.exists('.git'):
        if not run_command("git init", "Khởi tạo Git repository"):
            return False
    
    # Add all files
    if not run_command("git add .", "Thêm tất cả files"):
        return False
    
    # Check if there are changes to commit
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️ Không có thay đổi nào để commit")
        return True
    
    # Commit changes
    commit_message = "feat: initial commit - Network Toolkit v1.0.0\n\n- All-in-one network testing tool\n- 14 interactive options\n- CSV and HTML export\n- Cross-platform support\n- Zero dependencies"
    
    if not run_command(f'git commit -m "{commit_message}"', "Commit changes"):
        return False
    
    print("\n🎉 Git repository setup hoàn thành!")
    return True

def push_to_github():
    """Hướng dẫn push lên GitHub"""
    print("\n📋 HƯỚNG DẪN PUSH LÊN GITHUB:")
    print("=" * 50)
    print("1. Tạo repository mới trên GitHub:")
    print("   - Đi đến https://github.com/new")
    print("   - Repository name: network-toolkit")
    print("   - Description: All-in-one network testing tool with beautiful reports")
    print("   - Public repository")
    print("   - KHÔNG tích 'Add README file' (đã có sẵn)")
    print()
    print("2. Sau khi tạo repo, chạy các lệnh sau:")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/YOUR_USERNAME/network-toolkit.git")
    print("   git push -u origin main")
    print()
    print("3. Hoặc nếu đã có remote:")
    print("   git push origin main")
    print()
    print("💡 Thay YOUR_USERNAME bằng username GitHub của bạn")
    print()
    
    # Hỏi có muốn tự động setup remote không
    try:
        username = input("🔗 Nhập GitHub username (Enter để skip): ").strip()
        if username:
            repo_url = f"https://github.com/{username}/network-toolkit.git"
            
            # Check if remote already exists
            result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"ℹ️ Remote origin đã tồn tại: {result.stdout.strip()}")
                update = input("🔄 Cập nhật remote URL? (y/N): ").strip().lower()
                if update in ['y', 'yes']:
                    run_command(f"git remote set-url origin {repo_url}", "Cập nhật remote URL")
            else:
                run_command(f"git remote add origin {repo_url}", "Thêm remote origin")
            
            # Set main branch
            run_command("git branch -M main", "Đặt tên branch chính là main")
            
            print(f"\n🚀 Sẵn sàng push! Chạy lệnh:")
            print(f"   git push -u origin main")
            
            auto_push = input("\n🚀 Tự động push ngay? (y/N): ").strip().lower()
            if auto_push in ['y', 'yes']:
                if run_command("git push -u origin main", "Push lên GitHub"):
                    print(f"\n🎉 Đã push thành công lên GitHub!")
                    print(f"🌐 Repository URL: {repo_url}")
                    print(f"📊 GitHub Pages: https://{username}.github.io/network-toolkit/")
                else:
                    print("\n❌ Push thất bại. Vui lòng kiểm tra:")
                    print("   - GitHub repository đã được tạo chưa?")
                    print("   - Username và repository name có đúng không?")
                    print("   - Có quyền push không?")
    
    except KeyboardInterrupt:
        print("\n👋 Đã hủy setup remote")

def main():
    """Main function"""
    try:
        if setup_git_repo():
            push_to_github()
        else:
            print("❌ Git setup thất bại")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Đã dừng git setup")
        sys.exit(0)

if __name__ == "__main__":
    main()