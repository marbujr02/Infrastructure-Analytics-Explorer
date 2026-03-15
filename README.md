# Infrastructure Analytics Explorer

A Python command-line application that analyzes global data center infrastructure and generates statistical insights and visualizations.

---

## Overview

This project explores global data center infrastructure using Python data analysis tools.  
Users can load a dataset, perform statistical analysis, search infrastructure data, generate visualizations, and produce AI-generated insights.

Data centers serve as the **physical backbone of cloud computing platforms such as AWS**, which motivated this project while studying cloud infrastructure. :contentReference[oaicite:0]{index=0}

---

## Features

- Dataset loading and preprocessing
- Summary statistics and numerical analysis
- Search by country or cloud provider
- Data visualization with charts
- AI-generated insights using OpenAI API
- Menu-driven CLI interface

---

## Technologies Used

| Technology | Purpose |
|------------|--------|
| Python | Core programming language |
| Pandas | Data loading and cleaning |
| NumPy | Numerical analysis |
| Matplotlib | Data visualization |
| Regex | Input validation |
| OpenAI API | AI insight generation |

---

## Example Menu

```
What would you like to do today?

1. Load Dataset
2. Display Summary Statistics
3. Search Dataset
4. Perform Data Analysis
5. Create Visualization
6. API Data Lookup
7. Exit
```

---

## Project Structure

```
Infrastructure-Analytics-Explorer
│
├── main.py
├── dataset.csv
├── README.md
└── requirements.txt
```

---

## Challenges Solved

One challenge involved file path inconsistencies between Desktop, OneDrive, and the VS Code working environment.  
This was resolved by implementing a **path-agnostic loading method using Python’s `os.path` module** so the dataset can automatically be located relative to the script. :contentReference[oaicite:1]{index=1}

---

## Future Improvements

- Interactive dashboard
- Cloud provider infrastructure comparisons
- Additional statistical analysis
- Web interface

---

## Author

**Franklin Neal Jr.**  
University of Colorado Denver  
Information Systems
