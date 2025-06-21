# 📚 Bookstore API Automation

This repository contains API automation tests for a FastAPI-based Bookstore application using `pytest`, `httpx`, and Allure for reporting.

---

## ✅ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd bookstore
```

### 2. Create Virtual Environment & Install Requirements
```bash
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r bookstore/requirements.txt
```

### 3. Set Up Allure CLI
- Install Java (required by Allure CLI)
- Install Allure CLI:
```bash
choco install allure   # On Windows (using Chocolatey)
```
- Confirm installation:
```bash
allure --version
```

---

## ▶️ Running the Test Suite

### With Allure Reporting:
1. Run all tests and collect raw results:
```bash
pytest tests/ --alluredir=allure-results
```

2. Launch the interactive report:
```bash
allure serve allure-results
```

3. (Optional) Export a static HTML report:
```bash
allure generate allure-results -o allure-report --clean
start allure-report\index.html
```

---

## 🔍 Testing Strategy
- Written using `pytest` with test isolation and schema validation.
- Token-protected routes are tested using real JWT tokens.
- Each test validates HTTP status codes, response body fields, and authorization.
- Modular setup using `conftest.py` for reusability.
- Follows clear Arrange → Act → Assert flow.

### Coverage:
- ✅ User signup and login
- ✅ Auth token flow and protected routes
- ✅ Book creation, retrieval, update, and deletion
- ✅ Invalid payload and negative test cases
- ✅ Health check endpoint

---

## 📁 Project Structure
```
bookstore/
├── bookstore/              # FastAPI app
│   ├── main.py
│   ├── database.py
│   ├── utils.py
│   └── ...
├── tests/                  # API tests using pytest
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_health.py
├── allure-results/         # ⚠️ Temporary test data (auto-generated)
├── allure-report/          # ✅ Permanent HTML report
├── requirements.txt
└── README.md
```

---

## 🧪 Sample Test Report
After test execution, open the Allure report to view:
- Total test runs and results
- Execution timeline
- Failed test tracebacks
- Tagged features and stories

📸 Screenshot Example:
> ![Sample Allure Report]
> !

---

## 💡 Notes
- Use `allure serve` to view results dynamically.
- Use `allure generate` to export static HTML reports.
- Ensure Java is installed and `JAVA_HOME` is set for Allure.
- Report folders can be zipped and shared.

---

Made with ❤️ for API quality assurance.

