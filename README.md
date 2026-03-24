 <h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   Hệ thống quản lý nhân sự, khách hàng và công việc trên nền tảng Odoo 15
</h2>
<div align="center">
    <p align="center">
        <img src="images/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="images/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="images/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
</div>

# HỆ THỐNG ERP QUẢN LÝ KHÁCH HÀNG VÀ CÔNG VIỆC TÍCH HỢP HRM

## 1. Tổng quan về hệ thống

Hệ thống được xây dựng trên nền tảng **Odoo 15** nhằm hỗ trợ doanh nghiệp quản lý tập trung các nghiệp vụ cốt lõi, bao gồm **quản lý nhân sự, quản lý khách hàng và quản lý công việc**. Hệ thống được thiết kế theo mô hình ERP module hóa, cho phép các chức năng liên kết chặt chẽ với nhau, đồng thời đảm bảo tính linh hoạt, dễ mở rộng và phù hợp với nhu cầu quản lý thực tế của doanh nghiệp.

Trong hệ thống, mỗi nghiệp vụ được triển khai dưới dạng một module độc lập nhưng có khả năng tích hợp và chia sẻ dữ liệu. Nhờ đó, thông tin về nhân sự, khách hàng, người liên hệ và công việc được quản lý đồng bộ, giúp nâng cao hiệu quả vận hành, giảm thao tác thủ công và hỗ trợ nhà quản lý trong quá trình theo dõi, đánh giá và ra quyết định.

Điểm cốt lõi của hệ thống là lấy **HRM làm dữ liệu gốc**, từ đó liên kết sang **khách hàng**, và từ khách hàng phát sinh **công việc chăm sóc, tư vấn, báo giá**. Ngoài các chức năng quản lý cơ bản, hệ thống còn tích hợp **tự động hóa quy trình nghiệp vụ mức 2** và **Telegram Bot API ở mức 3** để gửi thông báo ra ngoài hệ thống.

---

## 2. Các chức năng chính

Hệ thống cung cấp các chức năng quản lý nghiệp vụ cốt lõi của doanh nghiệp, được triển khai dưới dạng các module độc lập nhưng có khả năng liên kết và chia sẻ dữ liệu với nhau.

### 2.1. Quản lý nhân sự
- Mở rộng hồ sơ nhân viên từ `hr.employee`.
- Quản lý thông tin bổ sung như quê quán, CCCD, ngày cấp, nơi cấp, số điện thoại khẩn cấp.
- Quản lý **thân nhân** của nhân viên.
- Quản lý **quá trình công tác**.
- Dashboard nhân sự hỗ trợ theo dõi nhanh tình trạng dữ liệu.
- Liên kết nhân viên với khách hàng và công việc phụ trách.

### 2.2. Quản lý khách hàng
- Quản lý thông tin khách hàng, loại khách hàng, hạng khách hàng, trạng thái.
- Gắn **nhân viên phụ trách** cho từng khách hàng.
- Quản lý **người liên hệ** của khách hàng doanh nghiệp.
- Theo dõi **lần chăm sóc gần nhất** và **ngày chăm sóc tiếp theo**.
- Hỗ trợ danh sách **Khách hàng cần chăm sóc**.
- Dashboard khách hàng hỗ trợ theo dõi khách VIP và khách hàng cần chăm sóc.

### 2.3. Quản lý công việc
- Tạo và theo dõi công việc theo từng giai đoạn xử lý.
- Gắn công việc với khách hàng, người liên hệ, nhân viên phụ trách và phòng ban.
- Quản lý công việc theo dạng danh sách, form và kanban.
- Quản lý **follow-up** phát sinh từ công việc trước đó.
- Quản lý **nhật ký nhắc việc**.
- Theo dõi **công việc quá hạn**.
- Dashboard công việc hỗ trợ giám sát nhanh tiến độ xử lý.

### 2.4. Tự động hóa mức 2
- Tự động điền thông tin công việc khi chọn khách hàng.
- Tự động gán người liên hệ chính và nhân viên phụ trách.
- Tự động tăng độ ưu tiên đối với khách hàng VIP.
- Tự động sinh công việc follow-up khi hoàn thành báo giá hoặc tư vấn lần 1.
- Cron kiểm tra công việc quá hạn và tạo nhắc việc định kỳ.

### 2.5. Tích hợp Telegram Bot API mức 3
- Cấu hình Telegram Bot Token và Chat ID trong hệ thống.
- Gửi thông báo Telegram thủ công từ form công việc.
- Gửi thông báo Telegram tự động khi phát sinh follow-up.
- Gửi thông báo Telegram khi công việc quá hạn.


## 3. Công nghệ sử dụng

![OS](https://img.shields.io/badge/OS-Ubuntu-orange?logo=ubuntu&logoColor=white)
![ERP](https://img.shields.io/badge/ERP-Odoo%2015-purple)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql&logoColor=white)
![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=white)
![Repository](https://img.shields.io/badge/Repository-GitHub-black?logo=github&logoColor=white)

Hệ thống được triển khai trên hệ điều hành Ubuntu, sử dụng nền tảng Odoo 15 làm lõi ERP.  
Python 3.10 được sử dụng để phát triển các module nghiệp vụ, kết hợp với PostgreSQL để lưu trữ dữ liệu.  
Docker hỗ trợ triển khai cơ sở dữ liệu, trong khi GitHub được dùng để quản lý mã nguồn.  
Ngoài ra, hệ thống tích hợp Google Calendar API và Groq API để mở rộng chức năng.


# 4. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 4.1. Clone project.
git clone https://gitlab.com/anhlta/odoo-fitdnu.git
git checkout 

## 4.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 4.3. khởi tạo môi trường ảo.

`python3.10 -m venv ./venv`
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

# 4.4. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`docker-compose up -d`

# 4.5. Setup tham số chạy cho hệ thống

## 4.5.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5432
xmlrpc_port = 8069
```
Có thể kế thừa từ **odoo.conf.template**

Ngoài ra có thể thêm mổ số parameters như:

```
-c _<đường dẫn đến tệp odoo.conf>_
-u _<tên addons>_ giúp cập nhật addons đó trước khi khởi chạy
-d _<tên database>_ giúp chỉ rõ tên database được sử dụng
--dev=all giúp bật chế độ nhà phát triển 
```

# 4.6. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất


## 📞 5. Liên hệ
- 👨‍🎓 **Sinh viên thực hiện**: Phạm Đình Tuấn Anh
- 🎓 **Khoa**: Công nghệ thông tin – Đại học Đại Nam
- 📧 **Email**: phamdinhtuananh05@gmail.com
