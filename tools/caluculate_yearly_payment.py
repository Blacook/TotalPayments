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


def 