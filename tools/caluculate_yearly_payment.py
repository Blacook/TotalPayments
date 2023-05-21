##
# @file    :   caluculate_yearly_payment.py
#
# @brief   :   To calculate the yearly payment from the payslip pdf
#
# @author  :   Shuhei Fukami
# @contact :   shu0722@keio.jp
# @date    :   2023/05/21
#
# (C)Copyright 2023, SFukami.


import os
import re
from pytesseract import image_to_string
from pdf2image import convert_from_path
from tools.ocr_payslip import read_text_from_pdf, extract_next_line_amount

def calculate_yearly_payment_from_pdf_dir(dir_path: str, path_tessdata:str='/opt/homebrew/share/tessdata',) -> int:
    """To calculate the yearly payment from the pdf files in the directory.

    Args:
        dir_path (str): the path to the directory containing the pdf files
        path_tessdata (str, optional): the path to the tessdata directory. Defaults to '/opt/homebrew/share/tessdata'.

    Returns:
        int: the yearly payment
    """
    # get the list of pdf files in the directory
    # sort the list by the file name
    pdf_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(".pdf")]
    pdf_files.sort()
    # calculate the yearly payment from the pdf files
    yearly_payment = 0
    for pdf_file in pdf_files:
        
        # read text from pdf
        pdf_path = os.path.join(dir_path, pdf_file)
        text = read_text_from_pdf(pdf_path, path_tessdata)
        # extract the amount of the next line
        amount = extract_next_line_amount(text)
        print(f"{pdf_file.split('.')[0]}: {amount} 円")
        # add the amount to the yearly payment
        yearly_payment += int(amount.replace(",", ""))
    print(f"Total Annual Salary:\n {yearly_payment:,} 円")
    return yearly_payment 