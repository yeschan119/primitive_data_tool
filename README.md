# Pharmacovigilance Analytics Tool
### ADR (Adverse Drug Reaction) Data Processing System

[한국어 🇰🇷](README.ko.md)

Internal pharmacovigilance analytics platform developed for **Daewoong Pharmaceutical PV Team** to automate analysis and reporting of **Adverse Drug Reaction (ADR) datasets**.

The tool processes raw pharmacovigilance data and generates regulatory reporting outputs including **Line Listing** and **Summary Tabulation**.

Designed as a **portable executable application** so pharmaceutical partners can run the tool without installing development environments.

---

# Project Overview

Pharmacovigilance teams regularly analyze large volumes of adverse drug reaction reports to detect potential safety signals.

This project automates the **data processing pipeline**, enabling faster safety analysis and report generation.

Key capabilities:

- ADR raw dataset ingestion
- Automated pharmacovigilance report generation
- GUI based workflow for non-technical users
- Executable distribution for external pharmaceutical clients
- Cloud-based authentication

---

# Key Features

## ADR Data Processing
Automated ingestion and transformation of pharmacovigilance datasets.

Capabilities:

- Data filtering by **product code**
- Date range based reporting
- Data transformation using **Pandas**

---

## Report Generation

Two report types are supported.

### Line Listing
Detailed case-level adverse event records.

Typical usage:
- Regulatory safety reporting
- Individual case analysis

### Summary Tabulation
Aggregated statistical analysis of ADR events.

Typical usage:
- Safety signal detection
- Trend analysis

---

## Desktop GUI Application

Built a GUI application using **Tkinter**.

Features:

- Product code input
- Start / End date selection
- Report generation workflow
- Progress bar monitoring
- Input validation and error handling

This allows **PV analysts without programming knowledge** to operate the tool.

---

## Executable Distribution

The application was packaged into a **standalone executable**.

Implementation steps:

1. Convert Jupyter Notebook code → Python modules
2. Build GUI application
3. Package executable using **PyInstaller**

Example build command:

```
pyinstaller --name PV_ADR_Analyzer \
--onefile guiapp.py \
--noconsole
```

---

## Environment Optimization

Initial environment size:

```
Anaconda environment ~300MB
```

Optimized build:

```
Custom virtualenv ~30MB
```

Result:

- ~90% size reduction
- Faster executable distribution

---

## Cloud Authentication System

User authentication implemented using **AWS RDS (MySQL)**.

Functions:

- User login verification
- Client access control
- Centralized credential management

Example user creation:

```
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON login.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

---

# Technology Stack

| Category | Technology |
|--------|-----------|
| Language | Python |
| Data Processing | Pandas |
| Database | MySQL |
| Cloud | AWS RDS |
| GUI | Tkinter |
| Packaging | PyInstaller |

---

# Project Structure

```
data/
  Sample pharmacovigilance datasets

code/
  Main analysis and reporting logic

sub_code/
  Experimental testing modules

demo/
  Tool demonstration videos
```

Example test dataset

```
Product Code : 201701182
Start Date : 2017-02-13
End Date : Present
```

---

# Security Considerations

Multiple approaches were evaluated for source code protection.

Options considered:

- Python code encryption
- Cython compilation
- PyInstaller packaging

Final approach:

- Compiled executable
- Restricted distribution
- Authentication via cloud database

---

# Cross Platform Testing

External environment testing performed across:

- Mac → Windows
- Windows → Mac
- Windows → Windows

Goal:

Ensure consistent executable behavior across operating systems.

---

# Challenges

## MedDRA Dictionary Licensing

MedDRA dictionaries cannot be distributed freely with the executable.

Proposed solution:

- Host MedDRA dictionary on secure server
- Retrieve data via API

---

## Edge Case Handling

Example case:

```
Product Code : 197000040
```

Result:

- Summary Tabulation generated successfully
- Line Listing returned empty dataset

Solution:

Display message:

```
"No ADR reports exist for the selected product"
```

---

# Project Outcome

- Built pharmacovigilance ADR analysis tool
- Automated safety report generation
- Delivered executable application for PV teams
- Integrated cloud authentication system
- Reduced runtime environment size by ~90%

---

# Team

Eungchan Kang — Pharmacovigilance Team  
Jisun Jang — IT Operations Team
