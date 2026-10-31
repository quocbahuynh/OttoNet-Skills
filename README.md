# Ottonet

**Universal ASP.NET Codebase Intelligence — Engineered for 100% Accuracy & Blazing-Fast Navigation**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Accuracy](https://img.shields.io/badge/Focus-100%25%20Accuracy%20%26%20Speed-orange)](skills/ottonet-skill/SKILL.md)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## Triết Lý: Chính Xác 100% & Tốc Độ Nhanh Nhất

Trong các codebase C# ASP.NET lớn (50.000 đến 500.000+ dòng code), vấn đề lớn nhất của AI không phải là thiếu chỗ chứa token, mà là **đọc lướt (skimming) dẫn đến hiểu sai logic nghiệp vụ**, đoán mò kiến trúc (IoC, MediatR, Controller inheritance), và tốn quá nhiều lượt gọi công cụ vòng vo.

**Ottonet** cắt bỏ toàn bộ thủ tục rườm rà, tập trung tuyệt đối vào:
1. **Tìm đúng điểm nóng trong 1 bước (Blazing-Fast Traversal):** Dò thẳng từ Route/Method đến đúng implementation mà không đoán mò.
2. **Thấu đáo 100% logic (Zero-Skimming Rigor):** Đọc trọn vẹn method mục tiêu trong 1 lượt gọi, soi kỹ toàn bộ rẽ nhánh `if-else`, toán tử biên (`<` vs `<=`), nullability, và EF Core change tracking.
3. **Workflow đa API vững chắc:** Neo theo vòng đời trạng thái (`Status Lifecycle`), đảm bảo sửa 1 API không làm gãy các bước kế tiếp trong chuỗi nghiệp vụ.

---

## Khả Năng Thích Ứng Toàn Diện (Universal Architecture)

Ottonet không hardcode theo bất kỳ thư viện nào mà hỗ trợ toàn diện mọi kiến trúc ASP.NET:
- **N-Tier / Layered:** Controller &rarr; `IService` &rarr; `Service` &rarr; `IRepository` &rarr; `DbContext`.
- **FastEndpoints / REPR:** `Endpoint<TRequest, TResponse>` với `HandleAsync`.
- **Minimal APIs & Carter:** `app.MapGet`/`MapPost`, Route Groups, `ICarterModule`.
- **Vertical Slice Architecture:** Co-located `Features/Orders/CreateOrder/`.
- **Dapper & Micro-ORMs:** Direct SQL strings, `IDbConnection`, and stored procedure mappings.
- **Modular Monolith & DDD:** Bounded contexts and in-memory event handlers.
- **Legacy Web API 2 / MVC:** `ApiController` actions and EF6.

---

## Cài Đặt (1 Lệnh Duy Nhất)

Cài đặt trực tiếp vào AI Agent hoặc workspace của bạn qua [skills.sh](https://skills.sh):

```bash
# Cài đặt cho workspace hiện tại (tự động nhận diện Cursor, Antigravity, Claude, Copilot, etc.)
npx skills add quocbahuynh/OttoNet-Skills --skill '*'

# Cài đặt toàn cục (global trên toàn máy tính)
npx skills add quocbahuynh/OttoNet-Skills -g --skill '*'

# Cài đặt cho từng agent cụ thể
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent cursor
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent claude-code
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent copilot
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent windsurf cline
```

---

## Zero Dependencies

Không dùng Python, không thêm project C# phụ, không sinh binary rác vào repository. Ottonet hoạt động thuần túy như một bộ não định hướng và kỷ luật tư duy cho AI Agent.

---

## License

Licensed under the [MIT License](LICENSE).
