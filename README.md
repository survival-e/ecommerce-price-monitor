# Advanced Production E-Commerce Price Monitor

A high-performance Python web scraping tool built with **Selenium**, **Object-Oriented Programming (OOP)**, and **Explicit Waits (`WebDriverWait`)**. Designed for scalable product tracking, dynamic pagination handling, and clean data export.

## Features
- **Headless Browser Execution**: Runs silently in CLI or CI/CD pipelines using custom Chrome options.
- **Robust Exception Handling**: Employs dynamic DOM polling (`WebDriverWait`) to handle asynchronous rendering cleanly without lag.
- **Object-Oriented Design**: Encapsulated within a modular `PriceMonitor` class for easy extensibility.
- **Data Normalization & Export**: Sanitizes scraped currencies into floats and generates standardized UTF-8 encoded CSVs.
- **Structured Logging**: Provides full real-time terminal execution logs for monitoring.

## Requirements & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ecommerce-price-monitor.git](https://github.com/YOUR_USERNAME/ecommerce-price-monitor.git)
   cd ecommerce-price-monitor