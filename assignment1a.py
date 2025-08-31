import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the Data from Excel
df = pd.read_excel("student.xlsx")

# 2. Vectorized Computations
df["Total"] = df[["Math", "Physics", "Chemistry", "Biology"]].sum(axis=1)
df["Average"] = df["Total"] / 4

# Grade assignment (vectorized with np.select)
conditions = [
    (df["Average"] >= 90),
    (df["Average"] >= 75) & (df["Average"] < 90),
    (df["Average"] >= 60) & (df["Average"] < 75),
    (df["Average"] < 60)
]
grades = ["A", "B", "C", "F"]
df["Grade"] = np.select(conditions, grades)

# 3. Top performers per subject
top_performers = {}
for subject in ["Math", "Physics", "Chemistry", "Biology"]:
    top3 = df.nlargest(3, subject)[["StudentID", "Name", subject]]
    top_performers[subject] = top3

# 5. Save Results Back to Excel
with pd.ExcelWriter("results.xlsx", engine="xlsxwriter") as writer:
    summary_cols = ["StudentID", "Name", "Total", "Average", "Grade"]
    df[summary_cols].to_excel(writer, sheet_name="Summary", index=False)

    workbook  = writer.book
    worksheet_tp = workbook.add_worksheet("Top Performers")
    writer.sheets["Top Performers"] = worksheet_tp

    startrow = 0
    for subject, top3 in top_performers.items():
        worksheet_tp.write(startrow, 0, f"Top 3 in {subject}")
        top3.to_excel(writer, sheet_name="Top Performers", index=False, startrow=startrow+1)
        startrow += len(top3) + 3

    avg_per_subject = df[["Math", "Physics", "Chemistry", "Biology"]].mean()
    plt.figure(figsize=(6,4))
    avg_per_subject.plot(kind='bar', title="Average Marks per Subject")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig("subject_avg.png")

    worksheet_summary = writer.sheets["Summary"]
    worksheet_summary.insert_image("H2", "subject_avg.png")
