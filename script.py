# Declaring dependencies
import pandas as pd
import sys
from fpdf import FPDF
from datetime import date
import os

# Parsing Inputs
def generateReport(dataset1, dataset2):

    df1 = pd.read_excel(dataset1)
    df2 = pd.read_excel(dataset2)

    # Metric 1: Difference in Number of Rows
    numRows1 = df1.shape[0]
    numRows2 = df2.shape[0]
    diffRows = numRows1 - numRows2
    percentChangeRows = (diffRows/numRows1)*100

    # Metric 2: Change in Storage
    totalStorage1 = df1['TotalFileSizeMB'].sum()
    totalStorage2 = df2['TotalFileSizeMB'].sum()

    storageDifference = totalStorage1 - totalStorage2
    changeStorage = (storageDifference/totalStorage1)*100

    url = df1.at[2, 'FileURL']
    teamName = url.split('/')[2]

    userName  = os.getlogin().split(".")
    name = " ".join(userName)


    # Writing to Report
    # Report Fields - Date and Timestamp, Generated by a
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"{teamName} Archive Summary", ln=True, align='C')
    
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Team Name: {teamName}", ln=True)
    pdf.cell(200, 10, txt=f"Generation Date: {date.today()}", ln=True)
    pdf.cell(200, 10, txt=f"Generated by: {name}", ln=True)

    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Total files before Archive: {numRows1}", ln=True)
    pdf.cell(200, 10, txt=f"Total files after Archive: {numRows2}", ln=True)
    pdf.cell(200, 10, txt=f"Reduction in files after archive: {diffRows}", ln=True)
    pdf.cell(200, 10, txt=f"Percent change in files: {round(percentChangeRows, 2)}%", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Storage used before archive (MB): {round(totalStorage1, 2)}", ln=True)
    pdf.cell(200, 10, txt=f"Total Storage used after archive (MB): {round(totalStorage2, 2)}", ln=True)
    pdf.cell(200, 10, txt=f"Difference in storage (MB): {round(storageDifference, 2)}", ln=True)
    pdf.cell(200, 10, txt=f"Percent change in Storage: {round(changeStorage, 2)}%", ln=True)

    pdf.output(f"{teamName}_archive_summary.pdf")

if __name__ == "__main__":

    # Checking input format
    if (len(sys.argv) != 3):
        print ("Input format should be `python script.py <inputfile1.xlsx> <inputfile2.xlsx>`")
        sys.exit(1)
    
    dataset1 = sys.argv[1]
    dataset2 = sys.argv[2]

    generateReport(dataset1, dataset2)
