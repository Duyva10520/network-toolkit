#!/usr/bin/env python3
"""
Network Toolkit - Công cụ kiểm tra mạng toàn diện
Hợp nhất tất cả các tính năng thành một tool duy nhất với menu tùy chọn
"""

import socket
import subprocess
import platform
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# ============================================================================
# NETWORK LOGGER CLASS
# ============================================================================

class NetworkLogger:
    def __init__(self, log_file=None):
        self.logs = []
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = log_file or f"network_toolkit_logs_{self.session_id}.json"
        
    def log(self, action: str, status: str, details: Dict[str, Any] = None, message: str = ""):
        """Ghi log cho một action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'action': action,
            'status': status,
            'message': message,
            'details': details or {}
        }
        
        self.logs.append(log_entry)
        
        # In ra console với format đẹp
        status_icon = {
            'success': '✅',
            'error': '❌', 
            'warning': '⚠️',
            'info': 'ℹ️',
            'start': '🔍',
            'complete': '✅'
        }.get(status, '📝')
        
        print(f"{status_icon} [{action}] {message}")
        
        # Lưu vào file ngay lập tức
        self.save_to_file()
        
        return log_entry
    
    def log_start(self, action: str, message: str = ""):
        return self.log(action, 'start', message=message or f"Bắt đầu {action}")
    
    def log_success(self, action: str, details: Dict[str, Any] = None, message: str = ""):
        return self.log(action, 'success', details, message or f"{action} thành công")
    
    def log_error(self, action: str, error: str, details: Dict[str, Any] = None):
        return self.log(action, 'error', details, f"{action} thất bại: {error}")
    
    def log_warning(self, action: str, warning: str, details: Dict[str, Any] = None):
        return self.log(action, 'warning', details, f"{action} cảnh báo: {warning}")
    
    def log_info(self, action: str, info: str, details: Dict[str, Any] = None):
        return self.log(action, 'info', details, info)
    
    def get_summary(self) -> Dict[str, Any]:
        total_logs = len(self.logs)
        success_count = len([log for log in self.logs if log['status'] == 'success'])
        error_count = len([log for log in self.logs if log['status'] == 'error'])
        warning_count = len([log for log in self.logs if log['status'] == 'warning'])
        
        actions = list(set(log['action'] for log in self.logs))
        
        return {
            'session_id': self.session_id,
            'total_logs': total_logs,
            'success_count': success_count,
            'error_count': error_count,
            'warning_count': warning_count,
            'actions_performed': actions,
            'success_rate': round((success_count / total_logs * 100), 2) if total_logs > 0 else 0
        }
    
    def print_summary(self):
        summary = self.get_summary()
        
        print("\n" + "=" * 50)
        print("📊 TÓM TẮT LOGS SESSION")
        print("=" * 50)
        print(f"🆔 Session ID: {summary['session_id']}")
        print(f"📝 Tổng logs: {summary['total_logs']}")
        print(f"✅ Thành công: {summary['success_count']}")
        print(f"❌ Lỗi: {summary['error_count']}")
        print(f"⚠️ Cảnh báo: {summary['warning_count']}")
        print(f"📈 Tỷ lệ thành công: {summary['success_rate']}%")
        print(f"🎯 Actions: {', '.join(summary['actions_performed'])}")
        print("=" * 50)
    
    def save_to_file(self):
        try:
            log_data = {
                'session_info': {
                    'session_id': self.session_id,
                    'created_at': datetime.now().isoformat(),
                    'total_logs': len(self.logs)
                },
                'summary': self.get_summary(),
                'logs': self.logs
            }
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Lỗi lưu log file: {e}")
    
    def export_csv(self, csv_file=None, export_type="basic", filter_status=None, filter_action=None):
        """Export logs ra CSV với nhiều tùy chọn"""
        import csv
        
        csv_file = csv_file or f"network_toolkit_logs_{self.session_id}.csv"
        
        try:
            # Filter logs theo yêu cầu
            filtered_logs = self.logs
            
            if filter_status:
                filtered_logs = [log for log in filtered_logs if log['status'] == filter_status]
            
            if filter_action:
                filtered_logs = [log for log in filtered_logs if log['action'] == filter_action]
            
            if not filtered_logs:
                print("❌ Không có logs nào phù hợp với filter")
                return False
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if export_type == "basic":
                    fieldnames = ['timestamp', 'action', 'status', 'message']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for log in filtered_logs:
                        writer.writerow({
                            'timestamp': log['timestamp'],
                            'action': log['action'],
                            'status': log['status'],
                            'message': log['message']
                        })
                
                elif export_type == "detailed":
                    fieldnames = ['timestamp', 'action', 'status', 'message', 'details']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for log in filtered_logs:
                        writer.writerow({
                            'timestamp': log['timestamp'],
                            'action': log['action'],
                            'status': log['status'],
                            'message': log['message'],
                            'details': str(log.get('details', {}))
                        })
                
                elif export_type == "summary":
                    # Export summary statistics
                    fieldnames = ['metric', 'value']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    summary = self.get_summary()
                    for key, value in summary.items():
                        writer.writerow({
                            'metric': key,
                            'value': str(value)
                        })
                
                elif export_type == "performance":
                    # Export performance data
                    fieldnames = ['action', 'status', 'timestamp', 'execution_time', 'details']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for log in filtered_logs:
                        details = log.get('details', {})
                        execution_time = ""
                        
                        # Tìm execution time trong details
                        for key in ['execution_time_seconds', 'scan_duration_seconds', 'connect_time_ms', 'resolve_time_ms']:
                            if key in details:
                                execution_time = str(details[key])
                                break
                        
                        writer.writerow({
                            'action': log['action'],
                            'status': log['status'],
                            'timestamp': log['timestamp'],
                            'execution_time': execution_time,
                            'details': str(details)
                        })
                    
            print(f"📄 Đã export CSV ({export_type}): {csv_file}")
            print(f"📊 Số records: {len(filtered_logs)}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi export CSV: {e}")
            return False
    
    def interactive_csv_export(self):
        """Interactive CSV export với menu tùy chọn"""
        print("\n📊 CSV EXPORT - TÙY CHỌN NÂNG CAO")
        print("=" * 50)
        
        if not self.logs:
            print("❌ Không có logs để export")
            print("💡 Tip: Chạy một vài tests trước để có logs")
            return False
        
        # Hiển thị thống kê hiện tại
        summary = self.get_summary()
        print(f"📝 Tổng logs: {summary['total_logs']}")
        print(f"✅ Thành công: {summary['success_count']}")
        print(f"❌ Lỗi: {summary['error_count']}")
        print(f"⚠️ Cảnh báo: {summary['warning_count']}")
        print(f"🎯 Actions: {', '.join(summary['actions_performed'])}")
        
        print("\n📋 CHỌN LOẠI EXPORT:")
        print("1. Basic Export      - Timestamp, Action, Status, Message")
        print("2. Detailed Export   - Bao gồm cả Details")
        print("3. Summary Export    - Chỉ thống kê tổng hợp")
        print("4. Performance Export - Focus vào thời gian thực hiện")
        print("5. Custom Filter     - Tùy chọn filter")
        print("0. Hủy")
        
        try:
            choice = int(input("\n👉 Chọn loại export (0-5): ").strip())
            
            if choice == 0:
                print("❌ Đã hủy export")
                return False
            
            # Tên file
            default_name = f"network_toolkit_export_{self.session_id}.csv"
            csv_file = input(f"\n📁 Tên file CSV (Enter = {default_name}): ").strip()
            if not csv_file:
                csv_file = default_name
            
            if choice == 1:
                return self.export_csv(csv_file, "basic")
            
            elif choice == 2:
                return self.export_csv(csv_file, "detailed")
            
            elif choice == 3:
                return self.export_csv(csv_file, "summary")
            
            elif choice == 4:
                return self.export_csv(csv_file, "performance")
            
            elif choice == 5:
                # Custom filter
                print("\n🔍 CUSTOM FILTER OPTIONS:")
                
                # Filter by status
                print(f"📊 Available statuses: success, error, warning, info, start")
                filter_status = input("Filter by status (Enter = all): ").strip()
                if not filter_status:
                    filter_status = None
                
                # Filter by action
                print(f"🎯 Available actions: {', '.join(summary['actions_performed'])}")
                filter_action = input("Filter by action (Enter = all): ").strip()
                if not filter_action:
                    filter_action = None
                
                # Export type
                print("\n📋 Export format:")
                print("1. Basic   2. Detailed")
                format_choice = input("Chọn format (1-2, Enter = 1): ").strip()
                export_type = "detailed" if format_choice == "2" else "basic"
                
                return self.export_csv(csv_file, export_type, filter_status, filter_action)
            
            else:
                print("❌ Lựa chọn không hợp lệ")
                return False
                
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")
            return False
        except KeyboardInterrupt:
            print("\n❌ Đã hủy export")
            return False
    
    def export_html(self, html_file=None, report_type="comprehensive"):
        """Export logs ra HTML report đẹp mắt"""
        html_file = html_file or f"network_toolkit_report_{self.session_id}.html"
        
        try:
            summary = self.get_summary()
            
            # HTML Template
            html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Toolkit Report - {summary['session_id']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .summary-card.success {{
            border-left-color: #28a745;
        }}
        
        .summary-card.error {{
            border-left-color: #dc3545;
        }}
        
        .summary-card.warning {{
            border-left-color: #ffc107;
        }}
        
        .summary-card.info {{
            border-left-color: #17a2b8;
        }}
        
        .summary-card h3 {{
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #495057;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .logs-section {{
            margin-top: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .logs-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .logs-table th {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .logs-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .logs-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-success {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .status-error {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .status-warning {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .status-info {{
            background-color: #d1ecf1;
            color: #0c5460;
        }}
        
        .status-start {{
            background-color: #e2e3e5;
            color: #383d41;
        }}
        
        .timestamp {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .action-tag {{
            background-color: #e9ecef;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.85em;
            color: #495057;
        }}
        
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            transition: width 0.3s ease;
        }}
        
        .chart-container {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        @media (max-width: 768px) {{
            .summary-grid {{
                grid-template-columns: 1fr;
            }}
            
            .logs-table {{
                font-size: 0.9em;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Network Toolkit Report</h1>
            <div class="subtitle">Session: {summary['session_id']} | Generated: {self._format_timestamp()}</div>
        </div>
        
        <div class="content">
            <!-- Summary Cards -->
            <div class="summary-grid">
                <div class="summary-card success">
                    <h3>✅ Successful Operations</h3>
                    <div class="value">{summary['success_count']}</div>
                </div>
                
                <div class="summary-card error">
                    <h3>❌ Failed Operations</h3>
                    <div class="value">{summary['error_count']}</div>
                </div>
                
                <div class="summary-card warning">
                    <h3>⚠️ Warnings</h3>
                    <div class="value">{summary['warning_count']}</div>
                </div>
                
                <div class="summary-card info">
                    <h3>📊 Total Logs</h3>
                    <div class="value">{summary['total_logs']}</div>
                </div>
            </div>
            
            <!-- Success Rate -->
            <div class="chart-container">
                <h3>📈 Success Rate: {summary['success_rate']}%</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {summary['success_rate']}%"></div>
                </div>
            </div>
            
            <!-- Actions Performed -->
            <div class="chart-container">
                <h3>🎯 Actions Performed</h3>
                <div style="margin-top: 15px;">
                    {self._generate_action_tags(summary['actions_performed'])}
                </div>
            </div>
"""
            
            if report_type == "comprehensive":
                html_content += self._generate_logs_table()
            
            html_content += f"""
        </div>
        
        <div class="footer">
            <p>Generated by Network Toolkit | {self._format_timestamp()}</p>
            <p>📧 For support: <a href="mailto:support@networktoolkit.com">support@networktoolkit.com</a></p>
        </div>
    </div>
    
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            // Animate progress bar
            const progressBar = document.querySelector('.progress-fill');
            if (progressBar) {{
                setTimeout(() => {{
                    progressBar.style.width = '{summary['success_rate']}%';
                }}, 500);
            }}
            
            // Add click handlers for summary cards
            const cards = document.querySelectorAll('.summary-card');
            cards.forEach(card => {{
                card.addEventListener('click', function() {{
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {{
                        this.style.transform = 'translateY(-5px)';
                    }}, 150);
                }});
            }});
        }});
    </script>
</body>
</html>
"""
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"🌐 Đã tạo HTML report: {html_file}")
            print(f"📊 Mở file trong browser để xem báo cáo đẹp mắt!")
            
            # Hỏi có muốn mở file không
            try:
                open_file = input("🌐 Mở file trong browser ngay? (y/N): ").strip().lower()
                if open_file in ['y', 'yes']:
                    self._open_html_file(html_file)
            except KeyboardInterrupt:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo HTML report: {e}")
            return False
    
    def _format_timestamp(self):
        """Format timestamp cho HTML"""
        from datetime import datetime
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    def _generate_action_tags(self, actions):
        """Tạo action tags cho HTML"""
        tags_html = ""
        for action in actions:
            tags_html += f'<span class="action-tag">{action}</span> '
        return tags_html
    
    def _generate_logs_table(self):
        """Tạo bảng logs cho HTML"""
        if not self.logs:
            return "<p>Không có logs để hiển thị.</p>"
        
        table_html = """
            <div class="logs-section">
                <h2 class="section-title">📋 Detailed Logs</h2>
                <table class="logs-table">
                    <thead>
                        <tr>
                            <th>⏰ Timestamp</th>
                            <th>🎯 Action</th>
                            <th>📊 Status</th>
                            <th>💬 Message</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Chỉ hiển thị 50 logs gần nhất để tránh file quá lớn
        recent_logs = self.logs[-50:] if len(self.logs) > 50 else self.logs
        
        for log in recent_logs:
            timestamp = log['timestamp'].split('T')[1].split('.')[0]  # Chỉ lấy time
            status_class = f"status-{log['status']}"
            
            table_html += f"""
                        <tr>
                            <td class="timestamp">{timestamp}</td>
                            <td><span class="action-tag">{log['action']}</span></td>
                            <td><span class="status-badge {status_class}">{log['status']}</span></td>
                            <td>{log['message']}</td>
                        </tr>
            """
        
        table_html += """
                    </tbody>
                </table>
            </div>
        """
        
        if len(self.logs) > 50:
            table_html += f"<p style='text-align: center; margin-top: 15px; color: #6c757d;'>Hiển thị 50 logs gần nhất (tổng: {len(self.logs)} logs)</p>"
        
        return table_html
    
    def interactive_html_export(self):
        """Interactive HTML export với menu tùy chọn"""
        print("\n🌐 HTML REPORT EXPORT")
        print("=" * 50)
        
        if not self.logs:
            print("❌ Không có logs để tạo report")
            print("💡 Tip: Chạy một vài tests trước để có logs")
            return False
        
        # Hiển thị thống kê hiện tại
        summary = self.get_summary()
        print(f"📝 Tổng logs: {summary['total_logs']}")
        print(f"✅ Thành công: {summary['success_count']}")
        print(f"❌ Lỗi: {summary['error_count']}")
        print(f"📈 Success rate: {summary['success_rate']}%")
        
        print("\n📋 CHỌN LOẠI REPORT:")
        print("1. Comprehensive Report - Bao gồm summary + detailed logs")
        print("2. Summary Only        - Chỉ thống kê tổng hợp")
        print("0. Hủy")
        
        try:
            choice = int(input("\n👉 Chọn loại report (0-2): ").strip())
            
            if choice == 0:
                print("❌ Đã hủy tạo report")
                return False
            
            # Tên file
            default_name = f"network_toolkit_report_{self.session_id}.html"
            html_file = input(f"\n📁 Tên file HTML (Enter = {default_name}): ").strip()
            if not html_file:
                html_file = default_name
            
            if choice == 1:
                return self.export_html(html_file, "comprehensive")
            elif choice == 2:
                return self.export_html(html_file, "summary")
            else:
                print("❌ Lựa chọn không hợp lệ")
                return False
                
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")
            return False
        except KeyboardInterrupt:
            print("\n❌ Đã hủy tạo report")
            return False
    
    def _open_html_file(self, html_file):
        """Mở HTML file trong browser"""
        import webbrowser
        import os
        
        try:
            # Lấy absolute path
            abs_path = os.path.abspath(html_file)
            file_url = f"file://{abs_path}"
            
            # Mở trong browser
            webbrowser.open(file_url)
            print(f"🌐 Đã mở {html_file} trong browser")
        except Exception as e:
            print(f"❌ Không thể mở file trong browser: {e}")
            print(f"💡 Bạn có thể mở file thủ công: {html_file}")

# ============================================================================
# NETWORK TOOLKIT CLASS
# ============================================================================

class NetworkToolkit:
    def __init__(self):
        self.results = {}
        self.logger = NetworkLogger()
        
    # ========================================================================
    # BASIC NETWORK FUNCTIONS
    # ========================================================================
    
    def ping_test(self, host="8.8.8.8", count=2):
        """Kiểm tra ping đến host"""
        self.logger.log_start("ping_test", f"Ping {host} với {count} packets")
        
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, str(count), host]
        
        try:
            start_time = time.time()
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            execution_time = time.time() - start_time
            
            ping_details = {
                'host': host,
                'count': count,
                'command': ' '.join(command),
                'return_code': result.returncode,
                'execution_time_seconds': round(execution_time, 2),
                'output_length': len(result.stdout) if result.stdout else 0
            }
            
            success = result.returncode == 0
            self.results[f'ping_{host}'] = {
                'host': host,
                'success': success,
                'execution_time': execution_time,
                'details': ping_details
            }
            
            if success:
                self.logger.log_success("ping_test", ping_details, 
                                      f"Ping {host} thành công ({execution_time:.2f}s)")
                return True
            else:
                self.logger.log_error("ping_test", f"Ping {host} thất bại", ping_details)
                return False
                
        except subprocess.TimeoutExpired:
            error_details = {'host': host, 'timeout': 15, 'error_type': 'timeout'}
            self.logger.log_error("ping_test", f"Ping {host} timeout", error_details)
            self.results[f'ping_{host}'] = {'host': host, 'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            error_details = {'host': host, 'error_type': 'exception', 'exception': str(e)}
            self.logger.log_error("ping_test", str(e), error_details)
            self.results[f'ping_{host}'] = {'host': host, 'success': False, 'error': str(e)}
            return False
    
    def check_dns(self, domains=None):
        """Kiểm tra DNS resolution"""
        if domains is None:
            domains = ["google.com", "github.com", "cloudflare.com"]
        
        self.logger.log_start("dns_check", f"Kiểm tra DNS cho {len(domains)} domains")
        
        dns_results = []
        success_count = 0
        
        for domain in domains:
            try:
                start_time = time.time()
                ip = socket.gethostbyname(domain)
                resolve_time = (time.time() - start_time) * 1000
                
                dns_result = {
                    'domain': domain, 
                    'ip': ip, 
                    'success': True, 
                    'resolve_time_ms': round(resolve_time, 2)
                }
                dns_results.append(dns_result)
                success_count += 1
                
                self.logger.log_success("dns_resolve", dns_result,
                                      f"DNS {domain} -> {ip} ({resolve_time:.2f}ms)")
                
            except socket.gaierror as e:
                dns_result = {'domain': domain, 'success': False, 'error': str(e), 'error_type': 'gaierror'}
                dns_results.append(dns_result)
                self.logger.log_error("dns_resolve", str(e), dns_result)
            except Exception as e:
                dns_result = {'domain': domain, 'success': False, 'error': str(e), 'error_type': 'exception'}
                dns_results.append(dns_result)
                self.logger.log_error("dns_resolve", str(e), dns_result)
        
        self.results['dns'] = dns_results
        
        summary = {
            'total_domains': len(domains), 
            'success_count': success_count, 
            'success_rate': success_count/len(domains)*100
        }
        
        self.logger.log_success("dns_check", summary,
                              f"DNS check hoàn thành: {success_count}/{len(domains)} thành công")
        
        return success_count == len(domains)
    
    def check_connectivity(self, hosts=None):
        """Kiểm tra kết nối socket"""
        if hosts is None:
            hosts = [("google.com", 80), ("github.com", 443), ("1.1.1.1", 53)]
        
        self.logger.log_start("connectivity_check", f"Kiểm tra kết nối đến {len(hosts)} hosts")
        
        connectivity_results = []
        success_count = 0
        
        for host, port in hosts:
            try:
                start_time = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                connect_time = (time.time() - start_time) * 1000
                
                if result == 0:
                    conn_result = {
                        'host': host,
                        'port': port,
                        'success': True,
                        'connect_time_ms': round(connect_time, 2)
                    }
                    connectivity_results.append(conn_result)
                    success_count += 1
                    
                    self.logger.log_success("connectivity_test", conn_result,
                                          f"{host}:{port} kết nối OK ({connect_time:.2f}ms)")
                else:
                    conn_result = {
                        'host': host,
                        'port': port,
                        'success': False,
                        'error': f'Connection failed (code: {result})'
                    }
                    connectivity_results.append(conn_result)
                    self.logger.log_error("connectivity_test", f"Kết nối thất bại", conn_result)
                    
            except Exception as e:
                conn_result = {
                    'host': host,
                    'port': port,
                    'success': False,
                    'error': str(e)
                }
                connectivity_results.append(conn_result)
                self.logger.log_error("connectivity_test", str(e), conn_result)
        
        self.results['connectivity'] = connectivity_results
        
        summary = {
            'total_hosts': len(hosts),
            'success_count': success_count,
            'success_rate': success_count/len(hosts)*100
        }
        
        self.logger.log_success("connectivity_check", summary,
                              f"Connectivity check hoàn thành: {success_count}/{len(hosts)} thành công")
        
        return success_count == len(hosts)
    
    def get_local_info(self):
        """Lấy thông tin mạng local"""
        self.logger.log_start("local_info", "Lấy thông tin mạng local")
        
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            local_details = {
                'hostname': hostname,
                'local_ip': local_ip,
                'platform': platform.system(),
                'platform_release': platform.release()
            }
            
            self.results['local_info'] = local_details
            
            self.logger.log_success("local_info", local_details,
                                  f"Local info: {hostname} ({local_ip})")
            
            return True
            
        except Exception as e:
            error_details = {'error': str(e), 'error_type': 'exception'}
            self.logger.log_error("local_info", str(e), error_details)
            self.results['local_info'] = {'success': False, 'error': str(e)}
            return False
    
    # ========================================================================
    # ADVANCED NETWORK FUNCTIONS
    # ========================================================================
    
    def port_scan(self, host="127.0.0.1", ports=None, port_range=None):
        """Scan các port"""
        if ports is None and port_range is None:
            ports = [22, 23, 25, 53, 80, 443, 3389, 5432, 3306]
        elif port_range:
            start_port, end_port = port_range
            ports = list(range(start_port, end_port + 1))
        
        self.logger.log_start("port_scan", f"Scanning {len(ports)} ports trên {host}")
        
        def check_port(port):
            try:
                start_time = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()
                connect_time = (time.time() - start_time) * 1000
                
                if result == 0:
                    self.logger.log_success("port_check", 
                                          {'host': host, 'port': port, 'connect_time_ms': connect_time},
                                          f"Port {port} mở ({connect_time:.2f}ms)")
                    return {'port': port, 'status': 'open', 'connect_time_ms': round(connect_time, 2)}
                else:
                    return {'port': port, 'status': 'closed'}
            except Exception as e:
                self.logger.log_error("port_check", str(e), {'host': host, 'port': port})
                return {'port': port, 'status': 'error', 'error': str(e)}
        
        start_scan_time = time.time()
        with ThreadPoolExecutor(max_workers=50) as executor:
            port_results = list(executor.map(check_port, ports))
        scan_duration = time.time() - start_scan_time
        
        # Phân tích kết quả
        open_ports = [p for p in port_results if p['status'] == 'open']
        closed_ports = [p for p in port_results if p['status'] == 'closed']
        error_ports = [p for p in port_results if p['status'] == 'error']
        
        scan_summary = {
            'host': host,
            'total_ports': len(ports),
            'open_count': len(open_ports),
            'closed_count': len(closed_ports),
            'error_count': len(error_ports),
            'scan_duration_seconds': round(scan_duration, 2),
            'open_ports': [p['port'] for p in open_ports]
        }
        
        self.results['port_scan'] = {
            'host': host,
            'results': port_results,
            'open_ports': [p['port'] for p in open_ports],
            'summary': scan_summary
        }
        
        # Log kết quả tổng
        if open_ports:
            self.logger.log_success("port_scan", scan_summary, 
                                  f"Port scan hoàn thành: {len(open_ports)} ports mở")
            print(f"✅ Tìm thấy {len(open_ports)} port mở: {[p['port'] for p in open_ports]}")
        else:
            self.logger.log_warning("port_scan", "Không tìm thấy port nào mở", scan_summary)
            print("❌ Không tìm thấy port nào mở")
        
        return len(open_ports) > 0
    
    def network_scan(self, network="192.168.1", start=1, end=10):
        """Quét các thiết bị trong mạng LAN"""
        ip_range = f"{network}.{start}-{end}"
        total_ips = end - start + 1
        self.logger.log_start("network_scan", f"Quét {total_ips} IPs trong range {ip_range}")
        
        active_hosts = []
        
        def ping_host(ip):
            try:
                if platform.system().lower() == "windows":
                    cmd = ["ping", "-n", "1", "-w", "500", ip]
                else:
                    cmd = ["ping", "-c", "1", "-W", "1", ip]
                
                start_ping = time.time()
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                ping_time = time.time() - start_ping
                
                if result.returncode == 0:
                    self.logger.log_success("host_ping", 
                                          {'ip': ip, 'ping_time_ms': round(ping_time * 1000, 2)},
                                          f"Tìm thấy thiết bị: {ip}")
                    return ip
                    
            except Exception as e:
                self.logger.log_error("host_ping", str(e), {'ip': ip})
            return None
        
        ips = [f"{network}.{i}" for i in range(start, end + 1)]
        
        scan_start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(ping_host, ips)
            active_hosts = [ip for ip in results if ip is not None]
        scan_duration = time.time() - scan_start_time
        
        scan_summary = {
            'network_range': ip_range,
            'total_ips_scanned': total_ips,
            'active_hosts_found': len(active_hosts),
            'scan_duration_seconds': round(scan_duration, 2),
            'active_hosts': active_hosts,
            'discovery_rate': len(active_hosts) / total_ips * 100 if total_ips > 0 else 0
        }
        
        if active_hosts:
            self.logger.log_success("network_scan", scan_summary,
                                  f"Network scan hoàn thành: {len(active_hosts)} thiết bị tìm thấy")
            print(f"✅ Tìm thấy {len(active_hosts)} thiết bị:")
            for host in active_hosts:
                print(f"   📱 {host}")
        else:
            self.logger.log_warning("network_scan", "Không tìm thấy thiết bị nào", scan_summary)
            print("❌ Không tìm thấy thiết bị nào")
            
        self.results['network_scan'] = scan_summary
        return len(active_hosts) > 0
    
    def bandwidth_test(self, host="google.com", port=80, duration=5):
        """Kiểm tra băng thông đơn giản"""
        self.logger.log_start("bandwidth_test", f"Kiểm tra băng thông đến {host}:{port} trong {duration}s")
        
        try:
            start_time = time.time()
            total_bytes = 0
            connections_made = 0
            
            while time.time() - start_time < duration:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                try:
                    sock.connect((host, port))
                    connections_made += 1
                    request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                    sock.send(request.encode())
                    
                    while True:
                        data = sock.recv(4096)
                        if not data:
                            break
                        total_bytes += len(data)
                        
                except socket.timeout:
                    break
                except Exception:
                    break
                finally:
                    sock.close()
            
            elapsed = time.time() - start_time
            if elapsed > 0 and total_bytes > 0:
                speed_bps = total_bytes / elapsed
                speed_kbps = speed_bps / 1024
                speed_mbps = speed_kbps / 1024
                
                bandwidth_details = {
                    'host': host,
                    'port': port,
                    'duration_seconds': round(elapsed, 2),
                    'total_bytes': total_bytes,
                    'connections_made': connections_made,
                    'speed_bps': round(speed_bps, 2),
                    'speed_kbps': round(speed_kbps, 2),
                    'speed_mbps': round(speed_mbps, 2)
                }
                
                self.logger.log_success("bandwidth_test", bandwidth_details,
                                      f"Băng thông: {speed_mbps:.2f} Mbps ({total_bytes} bytes)")
                
                print(f"✅ Tốc độ ước tính: {speed_mbps:.2f} Mbps ({speed_kbps:.2f} Kbps)")
                
                self.results['bandwidth_test'] = bandwidth_details
                return True
            else:
                error_details = {'host': host, 'port': port, 'total_bytes': total_bytes, 'elapsed': elapsed}
                self.logger.log_error("bandwidth_test", "Không thể đo được tốc độ", error_details)
                print("❌ Không thể đo được tốc độ")
                return False
                
        except Exception as e:
            error_details = {'host': host, 'port': port, 'error_type': 'exception', 'exception': str(e)}
            self.logger.log_error("bandwidth_test", str(e), error_details)
            print(f"❌ Lỗi kiểm tra băng thông: {e}")
            return False
    
    def traceroute(self, target="8.8.8.8", max_hops=15):
        """Thực hiện traceroute đến target"""
        self.logger.log_start("traceroute", f"Traceroute đến {target} với max {max_hops} hops")
        
        try:
            os_type = platform.system().lower()
            if os_type == "windows":
                cmd = ["tracert", "-h", str(max_hops), "-w", "3000", target]
            else:
                cmd = ["traceroute", "-m", str(max_hops), "-w", "3", target]
            
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            execution_time = time.time() - start_time
            
            traceroute_details = {
                'target': target,
                'max_hops': max_hops,
                'os_type': os_type,
                'command': ' '.join(cmd),
                'execution_time_seconds': round(execution_time, 2),
                'return_code': result.returncode,
                'output_lines': len(result.stdout.split('\n')) if result.stdout else 0
            }
            
            if result.returncode == 0:
                self.logger.log_success("traceroute", traceroute_details,
                                      f"Traceroute đến {target} hoàn thành ({execution_time:.2f}s)")
                print("✅ Traceroute hoàn thành:")
                print(result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout)
                
                self.results['traceroute'] = traceroute_details
                return True
            else:
                self.logger.log_error("traceroute", f"Command failed: {result.stderr}", traceroute_details)
                print(f"❌ Traceroute thất bại: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            timeout_details = {'target': target, 'timeout_seconds': 45}
            self.logger.log_error("traceroute", "Command timeout after 45 seconds", timeout_details)
            print("❌ Traceroute timeout")
            return False
        except Exception as e:
            error_details = {'target': target, 'error_type': 'exception', 'exception': str(e)}
            self.logger.log_error("traceroute", str(e), error_details)
            print(f"❌ Lỗi traceroute: {e}")
            return False
    
    def get_network_stats(self):
        """Lấy thống kê mạng chi tiết"""
        self.logger.log_start("network_stats", "Lấy thống kê mạng và kết nối")
        
        try:
            os_type = platform.system().lower()
            
            if os_type == "windows":
                stats_cmd = ["netstat", "-e"]
                connections_cmd = ["netstat", "-an"]
            else:
                stats_cmd = ["netstat", "-i"]
                connections_cmd = ["netstat", "-tuln"]
            
            # Lấy interface statistics
            start_time = time.time()
            result = subprocess.run(stats_cmd, capture_output=True, text=True, timeout=10)
            stats_time = time.time() - start_time
            
            if result.returncode != 0:
                raise Exception(f"Stats command failed: {result.stderr}")
            
            stats_output = result.stdout
            
            # Lấy connections
            start_time = time.time()
            connections = subprocess.run(connections_cmd, capture_output=True, text=True, timeout=10)
            connections_time = time.time() - start_time
            
            if connections.returncode != 0:
                raise Exception(f"Connections command failed: {connections.stderr}")
            
            connections_output = connections.stdout
            
            # Phân tích kết quả
            stats_lines = len(stats_output.split('\n'))
            connections_lines = len(connections_output.split('\n'))
            
            network_stats_details = {
                'os_type': os_type,
                'stats_command': ' '.join(stats_cmd),
                'connections_command': ' '.join(connections_cmd),
                'stats_execution_time_seconds': round(stats_time, 2),
                'connections_execution_time_seconds': round(connections_time, 2),
                'stats_output_lines': stats_lines,
                'connections_output_lines': connections_lines,
                'total_output_size': len(stats_output) + len(connections_output)
            }
            
            self.logger.log_success("network_stats", network_stats_details,
                                  f"Network stats hoàn thành ({stats_lines + connections_lines} lines)")
            
            print("✅ Thống kê mạng:")
            print("Interface Statistics:")
            print(stats_output[:500] + "..." if len(stats_output) > 500 else stats_output)
            print("\nActive Connections:")
            print(connections_output[:500] + "..." if len(connections_output) > 500 else connections_output)
            
            self.results['network_stats'] = network_stats_details
            return True
            
        except subprocess.TimeoutExpired:
            timeout_details = {'commands': [' '.join(stats_cmd), ' '.join(connections_cmd)]}
            self.logger.log_error("network_stats", "Command timeout", timeout_details)
            print("❌ Lỗi: Command timeout")
            return False
        except Exception as e:
            error_details = {'error_type': 'exception', 'exception': str(e)}
            self.logger.log_error("network_stats", str(e), error_details)
            print(f"❌ Lỗi lấy thống kê: {e}")
            return False
    
    # ========================================================================
    # TEST SUITES
    # ========================================================================
    
    def run_quick_test(self):
        """Chạy kiểm tra nhanh"""
        self.logger.log_start("quick_test", "Bắt đầu kiểm tra mạng nhanh")
        
        print("🚀 KIỂM TRA MẠNG NHANH")
        print("=" * 50)
        print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = datetime.now()
        
        tests = [
            ("Local Info", self.get_local_info),
            ("DNS Check", self.check_dns),
            ("Connectivity Check", self.check_connectivity),
            ("Ping Google DNS", lambda: self.ping_test("8.8.8.8", 2)),
            ("Ping Cloudflare DNS", lambda: self.ping_test("1.1.1.1", 2))
        ]
        
        completed_tests = 0
        failed_tests = 0
        
        for i, (test_name, test_func) in enumerate(tests, 1):
            try:
                print(f"\n{i}. {test_name}...")
                self.logger.log_info("test_execution", f"Đang chạy: {test_name}")
                
                success = test_func()
                
                if success:
                    completed_tests += 1
                    print(f"   ✅ {test_name} thành công")
                else:
                    failed_tests += 1
                    print(f"   ❌ {test_name} thất bại")
                    
            except Exception as e:
                failed_tests += 1
                self.logger.log_error("test_execution", f"Lỗi trong {test_name}: {str(e)}")
                print(f"   ❌ {test_name} lỗi: {e}")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.generate_report("Quick Test", completed_tests, failed_tests, duration)
        
        return {
            'total_tests': len(tests),
            'completed_tests': completed_tests,
            'failed_tests': failed_tests,
            'duration_seconds': round(duration, 2),
            'success_rate': completed_tests / len(tests) * 100
        }
    
    def run_full_test(self):
        """Chạy kiểm tra đầy đủ"""
        self.logger.log_start("full_test", "Bắt đầu kiểm tra mạng đầy đủ")
        
        print("🚀 KIỂM TRA MẠNG ĐẦY ĐỦ")
        print("=" * 50)
        print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = datetime.now()
        
        tests = [
            ("Local Info", self.get_local_info),
            ("DNS Check", self.check_dns),
            ("Connectivity Check", self.check_connectivity),
            ("Ping Google DNS", lambda: self.ping_test("8.8.8.8", 3)),
            ("Ping Cloudflare DNS", lambda: self.ping_test("1.1.1.1", 3)),
            ("Port Scan", lambda: self.port_scan("127.0.0.1")),
            ("Network Stats", self.get_network_stats)
        ]
        
        completed_tests = 0
        failed_tests = 0
        
        for i, (test_name, test_func) in enumerate(tests, 1):
            try:
                print(f"\n{i}. {test_name}...")
                self.logger.log_info("test_execution", f"Đang chạy: {test_name}")
                
                success = test_func()
                
                if success:
                    completed_tests += 1
                    print(f"   ✅ {test_name} thành công")
                else:
                    failed_tests += 1
                    print(f"   ❌ {test_name} thất bại")
                    
            except Exception as e:
                failed_tests += 1
                self.logger.log_error("test_execution", f"Lỗi trong {test_name}: {str(e)}")
                print(f"   ❌ {test_name} lỗi: {e}")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.generate_report("Full Test", completed_tests, failed_tests, duration)
        
        return {
            'total_tests': len(tests),
            'completed_tests': completed_tests,
            'failed_tests': failed_tests,
            'duration_seconds': round(duration, 2),
            'success_rate': completed_tests / len(tests) * 100
        }
    
    def run_advanced_test(self):
        """Chạy kiểm tra nâng cao"""
        self.logger.log_start("advanced_test", "Bắt đầu kiểm tra mạng nâng cao")
        
        print("🚀 KIỂM TRA MẠNG NÂNG CAO")
        print("=" * 50)
        print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = datetime.now()
        
        tests = [
            ("Network LAN Scan", lambda: self.network_scan("192.168.1", 1, 10)),
            ("Port Range Scan", lambda: self.port_scan("127.0.0.1", port_range=(20, 100))),
            ("Bandwidth Test", lambda: self.bandwidth_test("google.com")),
            ("Network Statistics", self.get_network_stats),
            ("Traceroute Test", lambda: self.traceroute("8.8.8.8"))
        ]
        
        completed_tests = 0
        failed_tests = 0
        
        for i, (test_name, test_func) in enumerate(tests, 1):
            try:
                print(f"\n{i}. {test_name}...")
                self.logger.log_info("test_execution", f"Đang chạy: {test_name}")
                
                success = test_func()
                
                if success:
                    completed_tests += 1
                    print(f"   ✅ {test_name} thành công")
                else:
                    failed_tests += 1
                    print(f"   ❌ {test_name} thất bại")
                    
            except Exception as e:
                failed_tests += 1
                self.logger.log_error("test_execution", f"Lỗi trong {test_name}: {str(e)}")
                print(f"   ❌ {test_name} lỗi: {e}")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.generate_report("Advanced Test", completed_tests, failed_tests, duration)
        
        return {
            'total_tests': len(tests),
            'completed_tests': completed_tests,
            'failed_tests': failed_tests,
            'duration_seconds': round(duration, 2),
            'success_rate': completed_tests / len(tests) * 100
        }
    
    def generate_report(self, test_type, completed_tests, failed_tests, duration):
        """Tạo báo cáo kết quả"""
        print(f"\n" + "=" * 60)
        print(f"📊 BÁO CÁO KẾT QUÁ - {test_type.upper()}")
        print("=" * 60)
        
        # DNS Status
        dns_results = self.results.get('dns', [])
        if dns_results:
            dns_success = sum(1 for r in dns_results if r.get('success'))
            print(f"🌐 DNS: {dns_success}/{len(dns_results)} domains thành công")
        
        # Connectivity Status
        conn_results = self.results.get('connectivity', [])
        if conn_results:
            conn_success = sum(1 for r in conn_results if r.get('success'))
            print(f"🔗 Connectivity: {conn_success}/{len(conn_results)} hosts thành công")
        
        # Ping Status
        ping_results = {k: v for k, v in self.results.items() if k.startswith('ping_')}
        if ping_results:
            ping_success = sum(1 for r in ping_results.values() if r.get('success'))
            print(f"🏓 Ping: {ping_success}/{len(ping_results)} hosts thành công")
        
        # Port Scan Status
        port_scan = self.results.get('port_scan', {})
        if port_scan:
            summary = port_scan.get('summary', {})
            open_count = summary.get('open_count', 0)
            total_ports = summary.get('total_ports', 0)
            print(f"🔌 Port Scan: {open_count}/{total_ports} ports mở")
        
        # Network Scan Status
        network_scan = self.results.get('network_scan', {})
        if network_scan:
            hosts_found = network_scan.get('active_hosts_found', 0)
            total_ips = network_scan.get('total_ips_scanned', 0)
            print(f"🔍 Network Scan: {hosts_found}/{total_ips} hosts tìm thấy")
        
        # Bandwidth Test Status
        bandwidth_test = self.results.get('bandwidth_test', {})
        if bandwidth_test:
            speed_mbps = bandwidth_test.get('speed_mbps', 0)
            print(f"📊 Bandwidth: {speed_mbps:.2f} Mbps")
        
        # Local Info
        local_info = self.results.get('local_info', {})
        if local_info and 'hostname' in local_info:
            print(f"🏠 Local: {local_info['hostname']} ({local_info.get('local_ip', 'N/A')})")
        
        # Tổng kết
        total_tests = completed_tests + failed_tests
        success_rate = (completed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 TỔNG KẾT:")
        print(f"   ✅ Thành công: {completed_tests}/{total_tests} tests ({success_rate:.1f}%)")
        print(f"   ⏱️ Thời gian: {duration:.2f} giây")
        print(f"   📁 Log file: {self.logger.log_file}")
        
        print("=" * 60)
        
        # Lưu kết quả
        self.save_results()
        
        # In summary logs
        self.logger.print_summary()
    
    def save_results(self):
        """Lưu kết quả vào file JSON"""
        filename = f"network_toolkit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Kết quả đã được lưu vào: {filename}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu file: {e}")

# ============================================================================
# MAIN MENU INTERFACE
# ============================================================================

def show_main_menu():
    """Hiển thị menu chính"""
    print("\n" + "=" * 70)
    print("🌐 NETWORK TOOLKIT - CÔNG CỤ KIỂM TRA MẠNG TOÀN DIỆN")
    print("=" * 70)
    print("📋 MENU CHÍNH:")
    print()
    print("   🚀 KIỂM TRA NHANH:")
    print("   1. Quick Test        - Kiểm tra nhanh (5 tests, ~30s)")
    print("   2. Full Test         - Kiểm tra đầy đủ (7 tests, ~2 phút)")
    print("   3. Advanced Test     - Kiểm tra nâng cao (5 tests, ~5 phút)")
    print()
    print("   🔧 KIỂM TRA RIÊNG LẺ:")
    print("   4. DNS Test          - Kiểm tra DNS resolution")
    print("   5. Ping Test         - Ping đến host tùy chọn")
    print("   6. Port Scan         - Quét port trên host")
    print("   7. Network Scan      - Quét thiết bị trong LAN")
    print("   8. Bandwidth Test    - Kiểm tra băng thông")
    print("   9. Traceroute        - Theo dõi đường đi gói tin")
    print("   10. Network Stats    - Thống kê mạng chi tiết")
    print()
    print("   📊 TIỆN ÍCH:")
    print("   11. Export CSV       - Export logs với nhiều tùy chọn")
    print("   12. Export HTML      - Tạo báo cáo HTML đẹp mắt")
    print("   13. View Summary     - Xem tóm tắt logs")
    print("   14. CSV Help         - Hướng dẫn sử dụng CSV")
    print("   0. Thoát")
    print("=" * 70)

def show_csv_help():
    """Hiển thị hướng dẫn sử dụng CSV"""
    print("\n📊 HƯỚNG DẪN SỬ DỤNG CSV EXPORT")
    print("=" * 60)
    print()
    print("🎯 MỤC ĐÍCH:")
    print("   CSV files giúp bạn phân tích logs bằng Excel, Google Sheets,")
    print("   hoặc các công cụ data analysis khác.")
    print()
    print("📋 CÁC LOẠI EXPORT:")
    print()
    print("   1️⃣ BASIC EXPORT:")
    print("      - Columns: Timestamp, Action, Status, Message")
    print("      - Dùng để: Xem tổng quan logs")
    print("      - Phù hợp: Báo cáo đơn giản")
    print()
    print("   2️⃣ DETAILED EXPORT:")
    print("      - Columns: + Details (thông tin chi tiết)")
    print("      - Dùng để: Phân tích sâu, debug")
    print("      - Phù hợp: Technical analysis")
    print()
    print("   3️⃣ SUMMARY EXPORT:")
    print("      - Columns: Metric, Value")
    print("      - Dùng để: Thống kê tổng hợp")
    print("      - Phù hợp: Dashboard, KPI tracking")
    print()
    print("   4️⃣ PERFORMANCE EXPORT:")
    print("      - Columns: Action, Status, Timestamp, Execution_Time")
    print("      - Dùng để: Phân tích hiệu suất")
    print("      - Phù hợp: Performance monitoring")
    print()
    print("   5️⃣ CUSTOM FILTER:")
    print("      - Filter theo: Status (success/error/warning)")
    print("      - Filter theo: Action (ping_test/dns_check/...)")
    print("      - Dùng để: Tập trung vào vấn đề cụ thể")
    print()
    print("💡 TIPS SỬ DỤNG:")
    print("   • Dùng Basic cho báo cáo hàng ngày")
    print("   • Dùng Performance để monitor tốc độ mạng")
    print("   • Dùng Custom Filter để tìm lỗi cụ thể")
    print("   • Import vào Excel để tạo charts")
    print("   • Dùng pivot tables để phân tích trends")
    print()
    print("📈 VÍ DỤ PHÂN TÍCH:")
    print("   • So sánh ping time theo thời gian")
    print("   • Đếm số lỗi DNS theo ngày")
    print("   • Tracking bandwidth qua các lần test")
    print("   • Monitoring port scan results")
    print("=" * 60)

def get_user_input(prompt, input_type=str, default=None):
    """Lấy input từ user với validation"""
    while True:
        try:
            user_input = input(f"{prompt}")
            if user_input.strip() == "" and default is not None:
                return default
            return input_type(user_input.strip())
        except ValueError:
            print(f"❌ Vui lòng nhập {input_type.__name__} hợp lệ")
        except KeyboardInterrupt:
            print("\n👋 Đã hủy")
            return None

def main():
    """Main function"""
    toolkit = NetworkToolkit()
    
    print("🎉 Chào mừng đến với Network Toolkit!")
    print("💡 Tip: Bạn có thể nhấn Ctrl+C bất kỳ lúc nào để dừng")
    
    while True:
        try:
            show_main_menu()
            
            choice = get_user_input("\n👉 Chọn chức năng (0-14): ", int)
            
            if choice is None:  # Ctrl+C
                break
            elif choice == 0:
                print("👋 Tạm biệt!")
                break
            elif choice == 1:
                toolkit.run_quick_test()
            elif choice == 2:
                toolkit.run_full_test()
            elif choice == 3:
                toolkit.run_advanced_test()
            elif choice == 4:
                domains = get_user_input("Nhập domains (cách nhau bởi dấu phẩy, Enter = mặc định): ", str, "")
                if domains:
                    domain_list = [d.strip() for d in domains.split(",")]
                    toolkit.check_dns(domain_list)
                else:
                    toolkit.check_dns()
            elif choice == 5:
                host = get_user_input("Nhập host để ping (Enter = 8.8.8.8): ", str, "8.8.8.8")
                count = get_user_input("Số lần ping (Enter = 4): ", int, 4)
                toolkit.ping_test(host, count)
            elif choice == 6:
                host = get_user_input("Nhập host để scan (Enter = 127.0.0.1): ", str, "127.0.0.1")
                port_range_input = get_user_input("Nhập port range (vd: 20-100, Enter = ports mặc định): ", str, "")
                if port_range_input and "-" in port_range_input:
                    start, end = map(int, port_range_input.split("-"))
                    toolkit.port_scan(host, port_range=(start, end))
                else:
                    toolkit.port_scan(host)
            elif choice == 7:
                network = get_user_input("Nhập network (Enter = 192.168.1): ", str, "192.168.1")
                start = get_user_input("IP bắt đầu (Enter = 1): ", int, 1)
                end = get_user_input("IP kết thúc (Enter = 10): ", int, 10)
                toolkit.network_scan(network, start, end)
            elif choice == 8:
                host = get_user_input("Nhập host (Enter = google.com): ", str, "google.com")
                port = get_user_input("Nhập port (Enter = 80): ", int, 80)
                duration = get_user_input("Thời gian test (giây, Enter = 5): ", int, 5)
                toolkit.bandwidth_test(host, port, duration)
            elif choice == 9:
                target = get_user_input("Nhập target (Enter = 8.8.8.8): ", str, "8.8.8.8")
                max_hops = get_user_input("Max hops (Enter = 15): ", int, 15)
                toolkit.traceroute(target, max_hops)
            elif choice == 10:
                toolkit.get_network_stats()
            elif choice == 11:
                toolkit.logger.interactive_csv_export()
            elif choice == 12:
                toolkit.logger.interactive_html_export()
            elif choice == 13:
                toolkit.logger.print_summary()
            elif choice == 14:
                show_csv_help()
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 0-14.")
            
            if choice != 0:
                input("\n⏸️  Nhấn Enter để tiếp tục...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Đã dừng chương trình.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi không mong muốn: {e}")
            input("⏸️  Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()