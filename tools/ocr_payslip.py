##
# @file    :   ocr_payslip.py
#
# @brief   :   To read text from pdf and extract the amount of the next line
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

def preprocess_image_for_ocr(img) -> str:
    # ノイズ除去
    img = cv2.medianBlur(img, 5)

    # 二値化
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 膨張と収縮
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    return img
    
def read_text_from_pdf(pdf_path: str, path_tessdata:str='/opt/homebrew/share/tessdata',) -> str:
    """To read text from pdf.

    Args:
        pdf_path (str): the path to the payslip pdf file
        path_tessdata (str, optional): the path to the tessdata directory. Defaults to '/opt/homebrew/share/tessdata'.
                                       "brew install tesseract-lang" to install the tessdata directory
                                       check the path by "brew info tesseract-lang"

    Returns:
        str: _description_
    """
    # designate the path to the tessdata directory
    os.environ['TESSDATA_PREFIX'] = path_tessdata
    # convert the pdf to images
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        # extract the text from the image
        text = image_to_string(image, lang="jpn", config="--psm 6")
    return text
    
def extract_next_line_amount(text: str, keyword:str="総支給", pattern_amount:str =r'(\d{1,3}(?:,\d{3})*)',)-> str:
    """To extract the amount of the next line from the text.

    Args:
        text (str): the payslip text to extract the amount from
        keyword (str, optional): the keyword to find the amount. Defaults to "総支給".
        pattern_amount (str, optional): the pattern to find the amount. Defaults to '\b\d{1,3}(?:,\d{3})*\b'.

    Returns:
        str : the amount of the next line
    """
    # extract the amount of the line and the next line from the text
    pattern_line = re.escape(keyword) + r'.*?\n.*?\n'
    match = re.search(pattern_line, text, re.DOTALL)
    if match:
        # print(match.group())
        #match.group()の二行目を抽出
        next_line = match.group().split('\n')[1].replace(' ', '')
        # print(next_line)
        # extract the amount from the matched text
        amount_match = re.search(pattern_amount, next_line)
        if amount_match:
            return amount_match.group().replace(' ', '')
    
    # if not found
    return "0"