import os
import fitz  # PyMuPDF
import pandas as pd


def extract_toc_from_pdf(pdf_path):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Extract the table of contents
    toc = pdf_document.get_toc()

    # Convert the TOC to a pandas DataFrame
    toc_data = []
    for entry in toc:
        toc_data.append({"Title": entry[1], "Level": entry[0], "Page": entry[2]})

    # Create a DataFrame
    df = pd.DataFrame(toc_data)
    
    return df

def get_page_count(pdf_path):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    return pdf_document.page_count

def save_toc_to_csv(pdf_path, csv_path):
    # Extract table of contents from PDF
    toc_df = extract_toc_from_pdf(pdf_path)

    # Save to CSV
    toc_df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # Example usage
    pdf_file = (
        "/home/mike/Documents/tunes/Beatles/Beatles/The Beatles Complete - Vol 1 A-I.pdf"
    )
    output_dir = "/usr/local/dev/MuApi/SheetMusicIndices/origindex"
    csv_file = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0] + ".csv")
    
    save_toc_to_csv(pdf_file, csv_file)
