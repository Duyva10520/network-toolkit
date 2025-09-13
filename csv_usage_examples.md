# CSV Export Usage Examples

## 📊 Cách sử dụng CSV files từ Network Toolkit v1.0.0

Network Toolkit cung cấp 5 loại CSV export với khả năng filtering mạnh mẽ.

### 🎯 Mục đích
CSV files giúp bạn:
- Phân tích logs bằng Excel, Google Sheets
- Tạo charts và graphs
- Monitor performance theo thời gian
- Tìm patterns và trends
- Tạo báo cáo chuyên nghiệp

### 📋 Các loại CSV Export

#### 1. Basic Export
```csv
timestamp,action,status,message
2025-09-13T20:26:22.223690,advanced_test,start,Bắt đầu kiểm tra mạng nâng cao
2025-09-13T20:26:22.224337,test_execution,info,Đang chạy: Network LAN Scan
2025-09-13T20:26:22.225093,network_scan,start,Quét 10 IPs trong range 192.168.1.1-10
```

**Sử dụng cho:**
- Báo cáo tổng quan
- Timeline của các tests
- Quick overview

#### 2. Detailed Export
```csv
timestamp,action,status,message,details
2025-09-13T20:26:22.223690,ping_test,success,Ping 8.8.8.8 thành công,"{'host': '8.8.8.8', 'execution_time': 0.45}"
```

**Sử dụng cho:**
- Technical analysis
- Debugging
- Performance tuning

#### 3. Summary Export
```csv
metric,value
session_id,20250913_202616
total_logs,18
success_count,5
error_count,1
success_rate,27.78
```

**Sử dụng cho:**
- KPI tracking
- Dashboard metrics
- Executive reports

#### 4. Performance Export
```csv
action,status,timestamp,execution_time,details
ping_test,success,2025-09-13T20:26:22.223690,0.45,{'host': '8.8.8.8'}
dns_resolve,success,2025-09-13T20:26:23.123456,23.45,{'domain': 'google.com'}
```

**Sử dụng cho:**
- Performance monitoring
- Speed analysis
- Optimization

### 💡 Excel/Google Sheets Tips

#### Tạo Charts từ Performance Data:
1. Import CSV vào Excel
2. Select columns: timestamp, execution_time
3. Insert → Line Chart
4. Analyze trends theo thời gian

#### Pivot Tables cho Analysis:
1. Select all data
2. Insert → Pivot Table
3. Rows: action
4. Values: Count of status
5. Filter: status = "success"

#### Conditional Formatting:
1. Select status column
2. Home → Conditional Formatting
3. Red cho "error"
4. Green cho "success"
5. Yellow cho "warning"

### 🔍 Custom Filter Examples

#### Chỉ export errors:
- Filter by status: `error`
- Export type: `detailed`
- Để debug các vấn đề

#### Chỉ export ping tests:
- Filter by action: `ping_test`
- Export type: `performance`
- Để monitor ping performance

#### Chỉ export successful operations:
- Filter by status: `success`
- Export type: `basic`
- Để báo cáo thành công

### 📈 Analysis Examples

#### 1. Network Performance Over Time
```sql
-- Nếu import vào database
SELECT 
    DATE(timestamp) as date,
    AVG(CAST(execution_time AS FLOAT)) as avg_time
FROM network_logs 
WHERE action = 'ping_test' AND status = 'success'
GROUP BY DATE(timestamp)
ORDER BY date;
```

#### 2. Success Rate by Test Type
```excel
=COUNTIFS(action,"ping_test",status,"success")/COUNTIF(action,"ping_test")
```

#### 3. Error Frequency
```excel
=COUNTIF(status,"error")
```

### 🚀 Advanced Usage

#### Power BI Integration:
1. Export detailed CSV
2. Import vào Power BI
3. Tạo dashboard với:
   - Success rate gauge
   - Performance trends
   - Error distribution

#### Python Analysis:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('network_toolkit_export.csv')

# Plot performance over time
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.plot(x='timestamp', y='execution_time', kind='line')
plt.show()
```

### 📊 Best Practices

1. **Regular Exports**: Export logs định kỳ để tracking
2. **Naming Convention**: Dùng tên file có timestamp
3. **Filter Wisely**: Chỉ export data cần thiết
4. **Backup**: Lưu trữ CSV files quan trọng
5. **Automation**: Script để auto-export và analysis

### 🎯 Use Cases

#### IT Administrator:
- Daily network health reports
- Performance trending
- Issue tracking

#### Network Engineer:
- Troubleshooting analysis
- Capacity planning
- SLA monitoring

#### DevOps:
- CI/CD pipeline monitoring
- Infrastructure health checks
- Alerting thresholds

#### Management:
- Executive dashboards
- KPI reporting
- Budget planning (based on performance data)