# 📱 Automated & Performance Testing of D17 Mobile App

This project focuses on the comprehensive Quality Assurance (QA) and testing transformation of the **D17 Mobile Application** (Tunisian Post). It demonstrates a shift from manual verification to a high-performance, automated pipeline using AI-driven strategies and industry-standard tools.

## 🌟 Key Highlights

- **Mobile Test Automation:** Developed a robust framework using **Appium & Python** for core financial transaction flows.
- **AI-Driven QA:** Leveraged the **Gemini API** to automatically generate executable test cases from user stories, optimizing the testing lifecycle.
- **Performance Engineering:** Conducted stress testing with **Apache JMeter**, simulating up to **1,000 concurrent users**.
- **Critical Insights:** Identified a backend performance bottleneck at **60 Transactions Per Second (TPS)**, providing actionable data for infrastructure scaling.
- **Security Validation:** Audited the application against **OWASP Mobile Top 10** standards (Certificate Pinning, HTTPS, etc.).

## 🛠 Tech Stack

* **Automation:** Appium, Python, PyTest, Android Debug Bridge (ADB).
* **Performance:** Apache JMeter.
* **Artificial Intelligence:** Gemini API (Google AI).
* **Management & DevOps:** Jira (Agile/Scrum), GitHub.
* **Network Analysis:** PCAPdroid, HTTP Toolkit.

## 📊 Project Architecture

The project follows a multi-layered approach:
1.  **Requirement Analysis:** Agile task management via Jira.
2.  **Test Design:** AI-generated test scenarios.
3.  **Execution:** Automated functional scripts (Appium) and Load testing (JMeter).
4.  **Security Audit:** Verification of data encryption and system integrity.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- Appium Server
- Android SDK (ADB)
- Apache JMeter

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Yassminefeki/D17Testing.git](https://github.com/Yassminefeki/D17Testing.git)
2. Install Python dependencies:
   pip install -r requirements.txt
3. Run the Appium server and connect your Android device
