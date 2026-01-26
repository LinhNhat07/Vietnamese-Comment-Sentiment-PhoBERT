# Vietnamese-News-Sentiment-Classification  
Phân loại cảm xúc tin tức tiếng Việt sử dụng PhoBERT

**Vietnamese News Sentiment Classification Using PhoBERT**

### Mục tiêu dự án
Xây dựng một hệ thống xử lý ngôn ngữ tự nhiên (NLP) tiếng Việt tiên tiến nhằm **phân loại cảm xúc** (Tiêu cực - Negative, Trung lập - Neutral, Tích cực - Positive) từ các bài báo trực tuyến. Hệ thống hỗ trợ phân tích dư luận, giám sát truyền thông, theo dõi xu hướng báo chí và ứng dụng trong các lĩnh vực như tài chính, quản lý khủng hoảng truyền thông, nghiên cứu truyền thông số.

### Công nghệ chính
- **Mô hình cốt lõi**: Fine-tune **PhoBERT** (mô hình ngôn ngữ tiền huấn luyện dành riêng cho tiếng Việt, dựa trên RoBERTa) sử dụng framework **PyTorch** và thư viện **Hugging Face Transformers**.
- **Dữ liệu**: Xây dựng bộ dữ liệu tùy chỉnh gồm **18.900 mẫu tin tức** thu thập từ **VnExpress** – một trong những cổng thông tin điện tử uy tín và có lượng truy cập lớn nhất Việt Nam.
- **Quy trình xử lý**:
  - Tokenization chuyên biệt cho tiếng Việt (word segmentation tích hợp trong PhoBERT).
  - Kỹ thuật cân bằng lớp (class balancing) để xử lý dữ liệu mất cân bằng tự nhiên trong tin tức.
  - Đánh giá đa lớp (multi-class classification) với các chỉ số chuẩn: Accuracy, F1-score (Macro & Weighted), Confusion Matrix.

### Triển khai
- Thu thập và gắn nhãn dữ liệu tin tức tiếng Việt từ VnExpress (tiêu đề + nội dung bài báo).
- Fine-tune PhoBERT qua nhiều epoch với các kỹ thuật tối ưu hóa hiện đại (learning rate scheduler, early stopping, gradient accumulation...).
- Đánh giá mô hình trên tập validation độc lập, phân tích Confusion Matrix chi tiết để xác định hiệu suất theo từng lớp cảm xúc và các trường hợp khó (imbalanced classes).

### Kết quả đạt được
Mô hình đạt hiệu suất phân loại mạnh mẽ trên dữ liệu thực tế tiếng Việt:

- **Accuracy**: **78.25%**  
- **F1-weighted**: **0.78**  
- **F1-macro**: **0.69**

Mô hình thể hiện **độ chính xác cao** ở lớp Tiêu cực và Tích cực, chứng minh khả năng phát hiện cảm xúc đáng tin cậy trên văn bản báo chí tiếng Việt thực tế. Kết quả này khẳng định hiệu quả của PhoBERT trong việc xử lý ngôn ngữ tiếng Việt – ngôn ngữ đơn âm tiết, giàu dấu thanh, ngữ cảnh phức tạp và từ vựng chuyên ngành.

### Ứng dụng thực tiễn & Tiềm năng phát triển
Dự án không chỉ dừng ở mô hình học thuật mà mang tính ứng dụng cao trong môi trường thực tế tại Việt Nam:

- **Giám sát truyền thông & dư luận**: Phát hiện sớm các làn sóng tiêu cực trên báo chí (ví dụ: khủng hoảng thương hiệu, sự kiện xã hội).
- **Phân tích tài chính & đầu tư**: Dự báo tác động của tin tức đến thị trường chứng khoán, tiền tệ hoặc bất động sản.
- **Nghiên cứu truyền thông**: Phân tích thiên kiến báo chí, xu hướng cảm xúc theo thời gian hoặc theo chủ đề (chính trị, kinh tế, y tế...).
- **Tích hợp hệ thống lớn**: Có thể triển khai vào dashboard thời gian thực, API cho doanh nghiệp, hoặc kết hợp với các công cụ social listening.

**Tiềm năng phát triển tiếp theo**:
- Mở rộng dữ liệu từ nhiều nguồn (Tuổi Trẻ, Thanh Niên, Dân Trí...) để tăng độ tổng quát.
- Thử nghiệm các mô hình mới hơn (PhoBERT-large, ViT5, hoặc multilingual models như XLM-R với fine-tuning).
- Thêm tính năng aspect-based sentiment analysis (phân tích cảm xúc theo khía cạnh cụ thể trong bài báo).
- Phát triển phiên bản demo web (Streamlit/Gradio) để người dùng thử nghiệm trực tiếp.
