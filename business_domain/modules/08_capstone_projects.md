# Module 8: Enterprise Domain Capstone Projects

This module outlines the requirements, stakeholders, and business value metrics for the six enterprise domain projects.

---

## Project 1: Insurance Claims Copilot

### Overview
Design and build an AI claims processing copilot that automates document ingestion, parses damage receipts, and flags suspicious claims for audit.

### Key Requirements
*   **Ingestion**: Parse pdf invoice files and damage photos.
*   **Validation**: Cross-reference receipts against policy coverage terms.
*   **Audit**: Flag claims with mismatched names, dates, or values for review.

### Business Value Metrics
*   **Cycle Time**: Reduce average days to settle claims from 5 days to under 2 hours.
*   **Operating Cost Savings**: Minimize manual auditor review hours.

---

## Project 2: Banking Loan Processing Assistant

### Overview
Build a loan application processor that parses tax returns and bank statements, calculates debt-to-income ratios, and flags risk profiles.

### Key Requirements
*   **Data Extraction**: Extract data from tax returns and bank statement PDFs.
*   **Metrics Calculation**: Calculate debt-to-income (DTI) ratio metrics.
*   **Audit**: Verify signatures and check for missing documents.

### Business Value Metrics
*   **Loan Growth**: Increase loan approval speed to capture new customers.
*   **Defect Reduction**: Minimize document omissions and manual review errors.

---

## Project 3: Healthcare Knowledge Assistant

### Overview
Build a RAG-based hospital knowledge assistant that allows clinicians to search care guidelines and medical databases.

### Key Requirements
*   **Search**: Query internal medical guideline documents.
*   **Groundedness**: Return responses with page citations to prevent hallucinations.
*   **Compliance**: Ensure strict user roles and block access to PHI.

### Business Value Metrics
*   **Search Time**: Reduce clinician search time for care guidelines.
*   **Compliance Score**: Enforce audit logging compliance.

---

## Project 4: Retail Demand Forecasting Platform

### Overview
Deploy a demand forecasting pipeline that predicts inventory requirements based on transaction history and seasonal variables.

### Key Requirements
*   **Forecasting**: Predict sales volumes for retail SKU inventory.
*   **Inventory Tuning**: Adjust safety stock thresholds to minimize stockouts and overstocks.

### Business Value Metrics
*   **Stockout Incidents**: Minimize lost sales from out-of-stock items.
*   **Storage Cost Savings**: Optimize inventory carrying costs.

---

## Project 5: Manufacturing Predictive Maintenance Platform

### Overview
Design an anomaly detection pipeline that monitors machine sensor telemetry to predict component failures.

### Key Requirements
*   **Ingestion**: Aggregate temperature and vibration sensor feeds from SCADA systems.
*   **Alerting**: Trigger maintenance repair orders before machinery breakdowns occur.

### Business Value Metrics
*   **Machine Downtime**: Reduce unscheduled machine outages.
*   **OEE Improvement**: Optimize overall equipment effectiveness.

---

## Project 6: Supply Chain Control Tower

### Overview
Build a real-time logistics control tower that aggregates WMS and TMS logs to track shipments and predict delivery delays.

### Key Requirements
*   **Telemetry**: Stream tracking updates from delivery trucks.
*   **Alerting**: Predict delivery delays in transit and reschedule shipments.

### Business Value Metrics
*   **OTIF Metric**: Improve on-time, in-full delivery rates.
*   **Transit Cost Savings**: Optimize carrier routing and reduce fuel costs.
