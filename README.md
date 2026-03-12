# Python Pharmacovigilance Analytics Tool

[한국어 🇰🇷](README.ko.md)

### Python-based ADR (Adverse Drug Reaction) Data Processing System

A **Python-based data analysis tool** developed for the Pharmacovigilance (PV) team to process and analyze **Adverse Drug Reaction (ADR) raw datasets**.

The system uses **Python data processing pipelines (Pandas)** to automatically generate regulatory reporting outputs including:

- **Line Listing**
- **Summary Tabulation**

The application was implemented as a **Python desktop GUI tool** so that non-technical PV analysts can run safety data analysis without a development environment.

---

## Key Features

- Python-based ADR data processing
- Pandas data transformation pipeline
- Automated Line Listing / Summary Tabulation reports
- Tkinter-based desktop GUI
- PyInstaller executable distribution
- AWS RDS-based user authentication

---

## Python-Centric Tech Stack

| Category | Technology |
|--------|-----------|
| Language | **Python** |
| Data Processing | **Pandas** |
| GUI | **Tkinter** |
| Packaging | **PyInstaller** |
| Database | MySQL |
| Cloud | AWS RDS |

---

## Project Structure

```
data/       ADR test datasets
code/       Python data processing logic
sub_code/   experimental / testing scripts
demo/       demonstration videos
```

---

<details>
<summary>Python Implementation Details</summary>

## Python Data Processing Pipeline

ADR raw datasets are processed using a Python-based data pipeline.

Processing steps:

- Product code filtering
- Date range filtering
- Data transformation using Pandas
- Report-ready dataset generation

---

## Automated ADR Reporting

The Python system generates two pharmacovigilance reports.

### Line Listing

Case-level adverse event data.

Typical usage:

- Regulatory reporting
- Individual case safety analysis

---

### Summary Tabulation

Aggregated statistical view of adverse events.

Typical usage:

- Safety signal detection
- ADR trend monitoring

---

## Python GUI Application

A desktop GUI application built using **Tkinter**.

Features:

- Product code input
- Start / End date selection
- Progress bar monitoring
- Input validation and error handling

This allows **PV analysts without programming knowledge** to use the system.

---

## Python Executable Distribution

The Python application was distributed as a **standalone executable** using PyInstaller.

Example build command:

```
pyinstaller --name PV_ADR_Analyzer \
--onefile guiapp.py \
--noconsole
```

---

## Python Environment Optimization

Initial environment:

```
Anaconda environment ~300MB
```

Optimized runtime:

```
Python virtualenv ~30MB
```

Result:

- ~90% environment size reduction
- Easier executable distribution

---

## Authentication System

Python application connected to **AWS RDS (MySQL)** for user authentication.

Example SQL:

```
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON login.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

</details>

---

## Team

Eungchan Kang — Pharmacovigilance Team  
Jisun Jang — IT Operations Team
