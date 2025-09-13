# Network Connection Checker

Công cụ kiểm tra toàn bộ kết nối mạng của máy tính được viết bằng Python.

## 📁 Cấu trúc Project

```
network-toolkit/
├── 🌟 Core Files
│   ├── network_toolkit.py       # Main tool - All-in-one network checker
│   ├── requirements.txt         # Dependencies info (100% standard library)
│   └── sample_report.html       # HTML report example
├── 📚 Documentation
│   ├── README.md               # Main documentation
│   ├── FEATURES.md             # Detailed feature list
│   ├── QUICK_START.md          # 30-second setup guide
│   ├── PROJECT_OVERVIEW.md     # Comprehensive overview
│   ├── CHANGELOG.md            # Version history
│   ├── CONTRIBUTING.md         # Contribution guidelines
│   ├── CONTRIBUTORS.md         # Contributors list
│   └── SECURITY.md             # Security policy
├── ⚙️ Setup & Build
│   ├── setup.py               # Setup script
│   ├── git_setup.py           # Git repository setup
│   ├── build_executable.py    # Build executable
│   ├── VERSION                # Version tracking
│   ├── COMMIT_MESSAGE.md      # Commit templates
│   └── LICENSE                # MIT License
├── 🔧 Development
│   ├── .gitignore             # Git ignore rules
│   ├── .github/workflows/     # GitHub Actions CI/CD
│   └── csv_usage_examples.md  # CSV usage guide
└── 📊 Generated Files (auto-created)
    ├── network_toolkit_logs_*.json     # Session logs
    ├── network_toolkit_results_*.json  # Test results
    ├── network_toolkit_export_*.csv    # CSV exports
    └── network_toolkit_report_*.html   # HTML reports
```

**Professional project structure với CI/CD, documentation và build system!**

## 🚀 Cách sử dụng

### 🌟 TOOL CHÍNH (Khuyến nghị):
```bash
python network_toolkit.py
```
**Tool duy nhất hợp nhất tất cả tính năng với menu tương tác đầy đủ**

### 🎯 Chỉ cần một lệnh duy nhất:
```bash
python network_toolkit.py
```

**Không cần cài đặt gì thêm - 100% Python standard library!**

### 📦 Installation Options:

#### Option 1: Direct Run (Khuyến nghị)
```bash
# Clone repository
git clone https://github.com/yourusername/network-toolkit.git
cd network-toolkit

# Run setup (optional)
python setup.py

# Run tool
python network_toolkit.py
```

#### Option 2: Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_executable.py

# Run executable
./dist/network-toolkit  # Linux/Mac
# hoặc
dist\network-toolkit.exe  # Windows
```

#### Option 3: Git Setup
```bash
# Setup git repository
python git_setup.py

# Push to GitHub (follow instructions)
```

## ✨ Tính năng Network Toolkit

### 🚀 KIỂM TRA NHANH (3 chế độ):
1. **Quick Test** (5 tests, ~30s):
   - ✅ Local Info, DNS, Connectivity, Ping tests
   
2. **Full Test** (7 tests, ~2 phút):
   - ✅ Tất cả Quick Test + Port Scan + Network Stats
   
3. **Advanced Test** (5 tests, ~7 phút):
   - ✅ LAN Scan, Port Range Scan, Bandwidth, Stats, Traceroute (2-min timeout)

### 🔧 KIỂM TRA RIÊNG LẺ:
- 🌐 **DNS Test**: Kiểm tra phân giải tên miền (tùy chọn domains)
- 🏓 **Ping Test**: Ping đến host tùy chọn (tùy chọn số lần)
- 🔌 **Port Scan**: Quét port trên host (tùy chọn range)
- 🔍 **Network Scan**: Quét thiết bị trong LAN (tùy chọn range IP)
- 📊 **Bandwidth Test**: Kiểm tra băng thông (tùy chọn host/port/duration)
- 🛣️ **Traceroute**: Theo dõi đường đi gói tin (tùy chọn target/hops)
- 📈 **Network Stats**: Thống kê mạng chi tiết

### 📊 TIỆN ÍCH:
- 💾 **Smart CSV Export**: 5 loại export (Basic, Detailed, Summary, Performance, Custom Filter)
- 🌐 **Beautiful HTML Reports**: Báo cáo HTML đẹp mắt với dashboard và charts
- 📋 **View Summary**: Xem tóm tắt logs session
- 🔍 **Interactive Menu**: Menu tương tác thân thiện
- ⚙️ **Customizable**: Tùy chỉnh parameters cho mọi test
- 📈 **CSV Help**: Hướng dẫn chi tiết cách sử dụng CSV cho analysis

### 📝 LOGGING SYSTEM:
- 📋 **Real-time Logging**: Log chi tiết từng bước
- 📊 **Session Summary**: Thống kê tổng hợp
- 💾 **Auto-save**: Tự động lưu JSON + CSV
- ⏱️ **Performance Tracking**: Đo thời gian execution
- 🔍 **Error Handling**: Chi tiết lỗi và troubleshooting

## 💡 Hướng dẫn sử dụng Network Toolkit

### 🌟 Khuyến nghị cho người dùng mới:
```bash
python network_toolkit.py
```

### 📋 Menu chính sẽ hiển thị:
```
🌐 NETWORK TOOLKIT - CÔNG CỤ KIỂM TRA MẠNG TOÀN DIỆN
====================================================================
📋 MENU CHÍNH:

   🚀 KIỂM TRA NHANH:
   1. Quick Test        - Kiểm tra nhanh (5 tests, ~30s)
   2. Full Test         - Kiểm tra đầy đủ (7 tests, ~2 phút)
   3. Advanced Test     - Kiểm tra nâng cao (5 tests, ~5 phút)

   🔧 KIỂM TRA RIÊNG LẺ:
   4. DNS Test          - Kiểm tra DNS resolution
   5. Ping Test         - Ping đến host tùy chọn
   6. Port Scan         - Quét port trên host
   7. Network Scan      - Quét thiết bị trong LAN
   8. Bandwidth Test    - Kiểm tra băng thông
   9. Traceroute        - Theo dõi đường đi gói tin
   10. Network Stats    - Thống kê mạng chi tiết

   📊 TIỆN ÍCH:
   11. Export Logs      - Export logs ra CSV
   12. View Summary     - Xem tóm tắt logs
   0. Thoát
```

### 🎯 Khuyến nghị sử dụng:
1. **Lần đầu**: Chọn `1. Quick Test` để kiểm tra nhanh
2. **Kiểm tra định kỳ**: Chọn `2. Full Test`
3. **Troubleshooting**: Chọn `3. Advanced Test`
4. **Kiểm tra cụ thể**: Sử dụng các option 4-10
5. **Phân tích**: Sử dụng option 11-12 để export và xem logs

## 🔧 Yêu cầu hệ thống

- Python 3.7+
- Windows/Linux/macOS
- Không cần cài đặt thêm package (100% standard library)

## 🧹 Project đã được tối ưu hóa

✅ **Đã hợp nhất tất cả tính năng** vào một file duy nhất  
✅ **Đã xóa các file thừa** và deprecated  
✅ **Đã tối ưu hóa cấu trúc** project  
✅ **Chỉ còn 3 files** cần thiết  
✅ **Không dependencies** bên ngoài  

## 📊 Ví dụ Output

### 🌐 HTML Report (MỚI):
Chọn option 12 để tạo báo cáo HTML đẹp mắt với:
- 📊 Dashboard với summary cards
- 📈 Progress bars và success rate
- 🎨 Giao diện responsive, modern
- 📱 Xem được trên mọi thiết bị
- 🔍 Color-coded logs table
- 💾 Tự động mở trong browser

### Quick Test:
```
🌐 KIỂM TRA MẠNG NHANH
========================================
⏰ Thời gian: 2024-12-13 14:30:22
💻 Hệ điều hành: Windows 10

1️⃣ Kiểm tra DNS...
   ✅ google.com -> 142.250.190.14
   ✅ github.com -> 140.82.112.3
   ✅ cloudflare.com -> 104.16.132.229

2️⃣ Kiểm tra kết nối...
   ✅ google.com:80 - 45ms
   ✅ github.com:443 - 67ms
   ✅ 1.1.1.1:53 - 23ms

📊 TÓM TẮT KẾT QUÁ:
🌐 DNS: 3/3 thành công
🔗 Kết nối: 3/3 thành công
🏠 Thông tin local: MyPC (192.168.1.100)
🌍 Internet: Có
```

## 🛠️ Troubleshooting

- **Lỗi permission**: Chạy với quyền admin (một số lệnh mạng cần quyền cao)
- **Timeout**: Kiểm tra firewall hoặc antivirus
- **DNS lỗi**: Thử đổi DNS sang 8.8.8.8 hoặc 1.1.1.1
- **Gateway không tìm thấy**: Kiểm tra kết nối WiFi/Ethernet

## 📝 Logging System

### Các loại logs:
- ✅ **Success**: Các action thành công
- ❌ **Error**: Lỗi và exception
- ⚠️ **Warning**: Cảnh báo
- ℹ️ **Info**: Thông tin bổ sung
- 🔍 **Start**: Bắt đầu action

### Files được tạo:
- `network_logs_YYYYMMDD_HHMMSS.json` - Logs chính
- `quick_test_logs.json` - Logs của quick test
- `demo_logs.json` - Logs demo
- `*.csv` - Export CSV (tùy chọn)

### Ví dụ log entry:
```json
{
  "timestamp": "2024-12-13T14:30:22.123456",
  "session_id": "20241213_143022",
  "action": "ping_test",
  "status": "success",
  "message": "Ping 8.8.8.8 thành công",
  "details": {
    "host": "8.8.8.8",
    "count": 4,
    "return_code": 0
  }
}
```

## 📝 Lưu ý

- Các test nâng cao có thể mất nhiều thời gian
- Port scanning chỉ test localhost để tránh vi phạm bảo mật
- Traceroute có thể bị chặn bởi một số router
- Tất cả kết quả và logs được lưu với timestamp
- Logs được lưu real-time, không mất dữ liệu khi interrupt

## 🛠️ Fixes và Improvements

### Các lỗi đã được sửa:
- ✅ **Traceroute timeout**: Giảm từ 60s xuống 45s, max_hops từ 30 xuống 15
- ✅ **Missing logs**: Thêm logging cho tất cả static methods
- ✅ **Error handling**: Cải thiện exception handling và timeout
- ✅ **Performance**: Tối ưu hóa ThreadPool workers và timeouts
- ✅ **Success counting**: Sửa logic đếm success/failure không chính xác

### Phiên bản tối ưu (`network_checker_optimized.py`):
- 🚀 **Nhanh hơn**: Chỉ chạy các test ổn định và nhanh
- 🛡️ **Ổn định hơn**: Timeout ngắn hơn, error handling tốt hơn
- 📊 **Logging đầy đủ**: Mỗi action đều có log chi tiết
- 🎯 **Focused**: Tập trung vào các test quan trọng nhất

### Tool phân tích lỗi (`fix_and_test.py`):
- 🔍 **Phân tích log files**: Tự động tìm lỗi trong logs
- 🧪 **Test individual functions**: Test từng function riêng lẻ
- 🛠️ **Auto-fix**: Tự động áp dụng các fixes
- 📊 **Report**: Báo cáo chi tiết về lỗi và fixes