#pip install dicom
#pip install pydicom


import matplotlib.pyplot as plt
import pydicom
import pydicom.data
import os
from os import listdir
import cv2
import pytesseract
from numpy.core.fromnumeric import shape, size
import numpy as np
import logging
import pandas as pd
from pytesseract.pytesseract import image_to_data
# from skimage import exposure
import sys

from pytesseract.pytesseract import image_to_data

# config
custom_config = r'--psm 12 outputbase digits '
# pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
# pytesseract.pytesseract.tesseract_cmd = 'D:/Tesseract-OCR/tesseract.exe'
logging.basicConfig(filename='app2.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

column_name = ["HN",
"S_MaxPerfusion", "S_Intervals", "S_ED", "S_ES", "S_EF",
"SM_LADPerfusion", "SSD_LADPerfusion",
"SM_LCXPerfusion", "SSD_LCXPerfusion",
"SM_RCAPerfusion", "SSD_RCAPerfusion",
"SM_TOTPerfusion", "SSD_TOTPerfusion",
"SM_LADWallThickening", "SSD_LADWallThickening",
"SM_LCXWallThickening", "SSD_LCXWallThickening",
"SM_RCAWallThickening", "SSD_RCAWallThickening",
"SM_TOTWallThickening", "SSD_TOTWallThickening",
"SM_LADWallMotion", "SSD_LADWallMotion",
"SM_LCXWallMotion", "SSD_LCXWallMotion",
"SM_RCAWallMotion", "SSD_RCAWallMotion",
"SM_TOTWallMotion", "SSD_TOTWallMotion",
"SE_LADPerfusion", "SE_LCXPerfusion", "SE_RCAPerfusion", "SE_TOTPerfusion",
"SE_LADWallThickening", "SE_LCXWallThickening", "SE_RCAWallThickening", "SE_TOTWallThickening",
"SE_LADWallMotion", "SE_LCXWallMotion", "SE_RCAWallMotion", "SE_TOTWallMotion",
"SSEV_LADPerfusion", "SSEV_LCXPerfusion", "SSEV_RCAPerfusion", "SSEV_TOTPerfusion",
"SSEV_LADWallThickening", "SSEV_LCXWallThickening", "SSEV_RCAWallThickening", "SSEV_TOTWallThickening",
"SSEV_LADWallMotion", "SSEV_LCXWallMotion", "SSEV_RCAWallMotion", "SSEV_TOTWallMotion",
"R_MaxPerfusion", "R_Intervals", "R_ED", "R_ES", "R_EF",
"RM_LADPerfusion", "RSD_LADPerfusion",
"RM_LCXPerfusion", "RSD_LCXPerfusion",
"RM_RCAPerfusion", "RSD_RCAPerfusion",
"RM_TOTPerfusion", "RSD_TOTPerfusion",
"RM_LADWallThickening", "RSD_LADWallThickening",
"RM_LCXWallThickening", "RSD_LCXWallThickening",
"RM_RCAWallThickening", "RSD_RCAWallThickening",
"RM_TOTWallThickening", "RSD_TOTWallThickening",
"RM_LADWallMotion", "RSD_LADWallMotion",
"RM_LCXWallMotion", "RSD_LCXWallMotion",
"RM_RCAWallMotion", "RSD_RCAWallMotion",
"RM_TOTWallMotion", "RSD_TOTWallMotion",
"RE_LADPerfusion", "RE_LCXPerfusion", "RE_RCAPerfusion", "RE_TOTPerfusion",
"RE_LADWallThickening", "RE_LCXWallThickening", "RE_RCAWallThickening", "RE_TOTWallThickening",
"RE_LADWallMotion", "RE_LCXWallMotion", "RE_RCAWallMotion", "RE_TOTWallMotion",
"RSEV_LADPerfusion", "RSEV_LCXPerfusion", "RSEV_RCAPerfusion", "RSEV_TOTPerfusion",
"RSEV_LADWallThickening", "RSEV_LCXWallThickening", "RSEV_RCAWallThickening", "RSEV_TOTWallThickening",
"RSEV_LADWallMotion", "RSEV_LCXWallMotion", "RSEV_RCAWallMotion", "RSEV_TOTWallMotion",
"SSS", "S_STS", "S_SMS",
"SRS", "R_STS", "R_SMS", "Date_MPI"]

# df = pd.DataFrame(columns=column_name)
# df_conf = pd.DataFrame(columns=column_name)

def dilate(img):
    # dilate
    kernel = np.ones((3,3), np.uint8)
    # conv_img = np.array(img)
    new_im = cv2.dilate(img, kernel, iterations=1)
    return new_im

def erode(img):
    # dilate
    kernel = np.ones((2,2), np.uint8)
    new_im = cv2.erode(img, kernel, iterations=1)
    return new_im

def invert_img(img):
    return cv2.bitwise_not(img)

def convert_to_string(img):
    return pytesseract.image_to_string(img, config=custom_config)

def im_to_bw(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def resize_img(img):
    return cv2.resize(img, (img.shape[1]*3, img.shape[0]*3))

def extract_text_confidence(img, type_output):
    # print(type_output)
    if(type_output == "number"):
        type = False
    else:
        type = True
    text = convert_to_string(img).split("\n")[0]

    # print(text)
    # print(text.replace('.','',1))
    # print(text.replace('.','',1).replace('-','',1).isdigit())

    try:
        # text เป็นตัวหนังสือแต่ type เป็นตัวเลข
        if((text.replace('.','',1).replace('-','',1).isdigit() == False) & (type == False) | (text == "")):
            text = "-"
            conf_value = 0
            confidence_value = 0
        else:
            img_to_data = image_to_data(img, output_type='data.frame')
            img_data = img_to_data[img_to_data.conf > 10]
            if(img_data.shape[0] == 0):
                if(img_to_data[img_to_data.conf < 10].shape[0] == 1):
                    conf_value = 0
                    confidence_value = 0
                else:
                    text = "-"
                    conf_value = 0
                    confidence_value = 0
            else:
                # print(img_data)
                conf_value = img_data['conf'].values[0]
                # print("conf:", conf_value)
                #confidence value
                # 100-90 = 2 = green
                # 70-89 = 1 = orange
                # 0-69 = 0 = red
                if((conf_value >= 90) & (conf_value <= 100)):
                    confidence_value = 2
                elif((conf_value >= 70) & (conf_value < 90)):
                    confidence_value = 1
                elif((conf_value >= 0) & (conf_value < 70)):
                    confidence_value = 0
            # print(confidence_value)
        print("text:", text, "conf:",conf_value, "conf_level:", confidence_value)
    except Exception as e:
        print("extract data error", e)
    return text, conf_value

def severity_scores(im_gray, check_num, version, dict_result, dict_confidence, type_img):

    center = int(im_gray.shape[1]/2)

    #version old
    if(version == "old"):
        # block 1 = 0-60, block 2 = 290-350, block 3 = 580-640
        # call & crop img (drop top img)
        print("\\\\ block 1 \\\\")
        j = 0
        for i in range(0,1000,20):
            if(j > 650):
                break
            elif(j > 370 and j < 570):
                print("\\\\ block 3 \\\\")
                j = 580
            elif(j > 80 and j < 100):
                print("\\\\ block 2 \\\\")
                j = 290
            # print(i, j)
            if(check_num == "3" or check_num == "6" ):
                sev = resize_img(im_gray[232+j:250+j+4 , center+410+5:im_gray.shape[1]-45])
            else:
                result_m = im_gray[232+j:250+j+4 , center+330+5:im_gray.shape[1]-127]
                result_m_re = im_to_bw(resize_img(result_m))
                # cv2.imshow('window', im_to_bw(result_m_re))
                # cv2.waitKey(0)
                # cv2_imshow(result_m_re)
            

            if(check_num == "1" or check_num == "4" ):
                result_sd = im_gray[232+j:250+j+4 , center+330+61:im_gray.shape[1]-70]
                result_sd_re = resize_img(result_sd)
                # cv2.imshow('window2', im_to_bw(result_sd_re))
                # cv2.waitKey(0)

            if(check_num == "1" or check_num == "4" ):
                mean, mean_conf = extract_text_confidence(result_m_re, "number")
                sd, sd_conf = extract_text_confidence(result_sd_re, "number")

                if(len(mean) >= 2):
                    if(mean[-2] != "." ):
                        print("point of mean is loss")
                        mean = mean[:-1] + "." + mean[-1]
                if(len(sd) >= 2):
                    if(sd[-2] != "."):
                        print("point of sd is loss")
                        sd = sd[:-1] + "." + sd[-1]

                print("mean: " + mean + " sd: " + sd)
                dict_result[type_img].append(mean)
                dict_result[type_img].append(sd)

                dict_confidence[type_img].append(mean_conf)
                dict_confidence[type_img].append(sd_conf)

            if(check_num == "2" or check_num == "5" ):
                # cv2_imshow(result_m_re)
                extent, extent_conf = extract_text_confidence(result_m_re, "number")
                dict_result[type_img].append(extent)
                dict_confidence[type_img].append(extent_conf)
                # print("Extent: " + extent)
            elif(check_num == "3" or check_num == "6" ):
                # cv2_imshow(sev)
                sev_score, sev_conf = extract_text_confidence(sev, "number")
                
                if(len(sev_score) >= 2):
                    if(sev_score[-2] != "." ):
                        print("point of sev is loss")
                        sev_score = sev_score[:-1] + "." + sev_score[-1]
                        print("SEV: " + sev_score)

                dict_result[type_img].append(sev_score)
                dict_confidence[type_img].append(sev_conf)
                # print("SEV: " + sev_score)

            j += 22
            # print(list_result)
            # break

    #version new
    else:
        print("\\\\ block 1 \\\\")
        j = 0
        for i in range(0,1000,20):
            if(j > 680):
                break
            elif(j > 370 and j < 570):
                print("\n \\\\ block 3 \\\\")
                j = 610
            elif(j >= 80 and j <= 100):
                print("\n \\\\ block 2 \\\\")
                j = 305

            #crop img
            if(check_num == "3" or check_num == "6" ):
                sev = erode(resize_img(im_gray[310+j:330+j , -100:]))
            elif(check_num == "2" or check_num == "5" ):
                extent = erode(resize_img(im_gray[310+j:330+j , center+530:]))
            else:
                im_mean = im_gray
                im_mean[310+j:330+j , center+535:-265] = 255
                mean = erode(resize_img(im_mean[310+j:330+j , center+490:-265]))

                im_sd = im_gray
                sd = erode(resize_img(im_sd[310+j:330+j , -265:-240]))

            # cv2.imshow('window1', sev)
            # cv2.waitKey(0)
            

            #Convert to string
            if(check_num == "1" or check_num == "4" ):
                mean, mean_conf = extract_text_confidence(mean, "number")
                sd, sd_conf = extract_text_confidence(sd, "number")
                

                if(len(mean) >= 2):
                    if(mean[-2] != "." ):
                        # print("point of mean is loss")
                        mean = mean[:-1] + "." + mean[-1]
                if(len(sd) >= 2):
                    if(sd[-2] != "."):
                        # print("point of sd is loss")
                        sd = sd[:-1] + "." + sd[-1]

                # print("mean: " + mean + " sd: " + sd)
                dict_result[type_img].append(mean)
                dict_result[type_img].append(sd)

                dict_confidence[type_img].append(mean_conf)
                dict_confidence[type_img].append(sd_conf)

            if(check_num == "2" or check_num == "5" ):
                extent, extent_conf = extract_text_confidence(extent, "number")
                dict_result[type_img].append(extent)
                dict_confidence[type_img].append(extent_conf)
                # print("Extent: " + extent)
            elif(check_num == "3" or check_num == "6" ):
                sev_score, sev_conf = extract_text_confidence(sev, "number")
                if(len(sev_score) > 3):
                    sev_score = sev_score[:3]
                dict_result[type_img].append(sev_score)
                dict_confidence[type_img].append(sev_conf)
                # print("SEV: " + sev_score)

            j += 20
            # print(list_result)
            # break

    return dict_result, dict_confidence

def hn_number(im_gray, hn, version, dict_result, dict_confidence, type_img):
    print("hn_number")
    if(version == "old"):
        # call & crop img (drop top img)
        center = int(im_gray.shape[1]/2)

        hn_number = invert_img(im_gray[110:140, center-100:center+100])
        # cv2.waitKey(0)
    else:
        hn_number = erode(invert_img(im_gray[:40, 150:400]))

    # print("HN:")
    hn_number_str, hn_conf = extract_text_confidence(hn_number, "str")

    dict_result[type_img].append(hn_number_str)
    dict_confidence[type_img].append(hn_conf)

    # Check hn number 
    # if(hn_number_str == hn):
    #     dict_result[type_img].append(hn_number_str)
    #     dict_confidence[type_img].append(hn_conf)
    # else:
    #     raise Exception(f"พบข้อมูลรหัสประจำตัวผู่ป่วยทที่อยู่ในไฟล์ ไม่ตรงกับรหัสประจำตัวผู่ป่วยที่ให้สกัด")
    
    print(dict_result)
    print("HN: ", hn_number_str)
    return dict_result, dict_confidence

def max_perfusion(im_gray, version, dict_result, dict_confidence, type_img):
    center = int(im_gray.shape[1]/2)
    if(version == "old"):
        # call & crop img (drop top img)
        re_img = resize_img(im_gray[185:205, center-110:center-60])
    else:
        max_per = 0
        re_img = resize_img(im_to_bw(im_gray[250:center-530, center-400:center-250]))

    # cv2_imshow(re_img)
    print("Max Perfusion:")
    max_per, max_per_conf = extract_text_confidence(re_img, "number")

    dict_result[type_img].append(max_per)
    dict_confidence[type_img].append(max_per_conf)

    return dict_result, dict_confidence

def left_position(imgray, version, dict_result, dict_confidence, type_img):

    if(version == "old"):
        # call & crop img (drop top img)
        im_gray = imgray
        center = int(im_gray.shape[1]/2)

        #ED
        im_gray[215:230, :50] = 0
        im_gray[215:230, 75:100] = 0
        ed1 = im_to_bw(resize_img(invert_img(im_gray[215:230, :center-350])))
        # cv2_imshow(ed1)

        #ES
        im_gray[230:250, :50] = 0
        im_gray[230:250, 75:100] = 0
        es1 = im_to_bw(erode(resize_img(invert_img(im_gray[230:250, :center-350]))))
        # cv2_imshow(es1)

        #ES
        im_gray[248:265, :35] = 0
        ef1 = im_to_bw(erode(resize_img(invert_img(im_gray[248:265, :center-350]))))
        # cv2_imshow(ef1)

        intervals_img = resize_img(invert_img(im_gray[180:195, :center-350]))
        intervals, intervals_conf = extract_text_confidence(intervals_img, "number")
    else:
        # call & crop img (drop top img)
        im_gray = imgray
        center = int(im_gray.shape[1]/2)

        #ED
        ed1 = (im_gray[95:110, :center-350])

        #ES
        im_gray[230:250, :50] = 0
        im_gray[230:250, 77:100] = 0
        es1 = resize_img(im_gray[110:125, :center-350])

        #ES
        im_gray[248:265, :35] = 0
        ef1 = resize_img(invert_img(im_gray[122:140, :center-350]))

        intervals = "-"

    print("==== ed, es, ef, intervals ====")
    ed, ed_conf = extract_text_confidence(ed1, "number")
    es, es_conf = extract_text_confidence(es1, "number")
    ef, ef_conf = extract_text_confidence(ef1, "number")

    #check_e
    ed = check_e(ed, "ed")
    es = check_e(es, "es")
    intervals = check_e(intervals, "intervals")

    dict_result[type_img].append(intervals)
    dict_result[type_img].append(ed)
    dict_result[type_img].append(es)
    dict_result[type_img].append(ef)

    dict_confidence[type_img].append(intervals_conf)
    dict_confidence[type_img].append(ed_conf)
    dict_confidence[type_img].append(es_conf)
    dict_confidence[type_img].append(ef_conf)

    return dict_result, dict_confidence

def check_e(e, whatE):
    # e = ed, es, ef

    if(e.isdigit()):
        result_e = ""
        if(e[-1:] == "."):
            e = e[:-1]
        if(len(e) > 3):
            for i in e:
                if(i.isdigit()):
                    result_e += i
            if(int(result_e[-3:]) < 100):
                e = str(int(result_e[-3:]))
            else:
                e = result_e[-2:]
        if(int(e) > 100 and whatE != "ed"):
            e = e[:-1]
        if(int(e) > 500 and whatE == "ed"):
            e = e[:-1]
    else:
        e = "-"
    return e

def s_scores(im_gray, version, dict_result, dict_confidence, type_img):

    center = int(im_gray.shape[1]/2)
    # cv2.imshow('window', im_gray[750:-250 , -50:])
    # cv2.waitKey(0)

    if(version == "old"):
        # print(im_gray[750:-300 , center-10:center+150])
        s_s = resize_img(im_to_bw(im_gray[750:-250 , center+100:center+150]))
        # print(s_s)
        sts = resize_img(im_to_bw(im_gray[750:-250 , center+270:center+150+180]))
        sms = resize_img(im_to_bw(im_gray[750:-250 , -50:]))
        sms[:, -30:] = 255

        print("=== s_s, sts, sms ===")
        # cv2_imshow(s_s)
        s_s_score, s_s_conf = extract_text_confidence(s_s, "number")
        # cv2_imshow(sts)
        sts_score, sts_conf = extract_text_confidence(sts, "number")
        # cv2_imshow(sms)
        sms_score, sms_conf = extract_text_confidence(sms, "number")

        # print("x", s_s_score)
        # cv2.imshow('window', im_to_bw(sms))
        # cv2.waitKey(0)
        # sms_new = ""
        # if(len(sms_score) > 1):
        #     for i in sms_score:
        #         print(i)
        #         if(i.isdigit()):
        #             sms_new += i

        # if(s_s_score.isdigit() == False):
        #     s_s_score = "-"
        # else:
        #     s_s_score = s_s_score[-2:]
        # if(sts_score.isdigit() == False):
        #     sts_score = "-"
        # else:
        #     sts_score = sts_score[-2:]
        # if(sms_score.isdigit() == False):
        #     sms_score = "-"
        # else:
        #     sms_score = sms_score[-2:]

        dict_result[type_img].append(s_s_score)
        dict_result[type_img].append(sts_score)
        dict_result[type_img].append(sms_score)

        dict_confidence[type_img].append(s_s_conf)
        dict_confidence[type_img].append(sts_conf)
        dict_confidence[type_img].append(sms_conf)
        # print("S_S: {s_s} STS: {sts} SMS2: {sms}".format(s_s = s_s_score, sts = sts_score, sms = sms_score))
    else:
        s_s = im_to_bw(im_gray[-110:-80 , center+90:center+120])
        sts = resize_img(im_to_bw(resize_img(im_gray[-110:-80 , center+400:center+430])))
        sms = resize_img(im_to_bw(im_gray[750:-300 , -50:]))

        print("=== s_s, sts, sms ===")
        s_s_score, s_s_conf = extract_text_confidence(s_s, "number")
        sts_score, sts_conf = extract_text_confidence(sts, "number")
        sms_score, sms_conf = extract_text_confidence(sms, "number")

        dict_result[type_img].append(s_s_score)
        dict_result[type_img].append(sts_score)
        dict_result[type_img].append(sms_score)

        dict_confidence[type_img].append(s_s_conf)
        dict_confidence[type_img].append(sts_conf)
        dict_confidence[type_img].append(sms_conf)

    return dict_result, dict_confidence

def call_process(basepath, hn):

    df = pd.DataFrame(columns=column_name)
    df_conf = pd.DataFrame(columns=column_name)
    
    dict_result = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}
    dict_confidence = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}
    
    #Call path from directory
    error_list = []
    list_result = []
    list_confidence = []
    msg_error = ""
    for count, filename in zip(range(1,9), os.listdir(basepath)):
        print("\n","round", count)
        type_file = filename[-3:]
        
        if(type_file == "dcm"):
            
            path = basepath+"/"+filename
            print('path:', path)
            print('filename:', filename, "\n")

            img, ds = readdcm(path, hn)
            date = ds.StudyDate

            if(True):

                version = check_version_img(img)
                # cv2_imshow(img)

                # convert to gray
                im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # convert to bw
                im_gray = im_to_bw(im_gray)

                #[top:bottom, left:right]
                im_gray = invert_img(im_gray)
                im_gray = im_gray[:, 28:]


                check_num, type_img = check_number_file(filename)
                # print("check_num", check_num)
                  

                try:
                    # severity score
                    if("ss" in filename or "rs" in filename):
                        
                        if(check_num == "1"):
                            dict_result, dict_confidence = hn_number(im_gray, hn, version, dict_result, dict_confidence, type_img)
                            print("hn >> ",dict_result)
                        
                        dict_result, dict_confidence = max_perfusion(im_gray, version, dict_result, dict_confidence, type_img)
                        print("max per >> ",dict_result)
                        dict_result, dict_confidence = left_position(im_gray, version, dict_result, dict_confidence, type_img)
                        print("ef ed es >> ",dict_result)
                        
                        
                        dict_result, dict_confidence = severity_scores(im_gray, check_num, version, dict_result, dict_confidence, type_img)
                        
                        print("sevirity score >> ",dict_result)
                        print("Extract image", check_num, "success.")
                        
                    # extent score
                    elif("sb" in filename or "rb" in filename):
                        dict_result, dict_confidence = severity_scores(im_gray, check_num, version, dict_result, dict_confidence, type_img)
                        # print(filename, "sevirity score >> ",dict_result)
                        print("Extract image", check_num, filename,"success.")
                    # extent + sev score
                    elif("sd" in filename or "rd" in filename):
                        dict_result, dict_confidence = severity_scores(im_gray, check_num, version, dict_result, dict_confidence, type_img)
                        # print(filename, "sevirity score >> ",dict_result)
                        print("Extract image", check_num, filename, "success.")
                    # SRS, SSS etc
                    elif("sis" in filename or "ris" in filename):
                        dict_result, dict_confidence = s_scores(im_gray, version, dict_result, dict_confidence, type_img)
                        # print(filename, "S_S score >> ",dict_result)
                        print("Extract image", check_num, filename, "success.")
                    
                    # end row in pandas
                    if(count == 8):
                        for count, i in zip(range(1,9), dict_result):
                            list_result = list_result + dict_result[i]
                            list_confidence = list_confidence + dict_confidence[i]

                        if(size(list_result) == 113):
                            list_result.append(date)
                            list_confidence.append(0)
                            
                            df_new_row = pd.DataFrame(data=np.array([list_result]), columns=column_name)
                            df = pd.concat([df,df_new_row], ignore_index=True)

                            df_conf_new_row = pd.DataFrame(data=np.array([list_confidence]), columns=column_name)
                            df_conf = pd.concat([df_conf,df_conf_new_row], ignore_index=True)
                            list_result = []
                            list_confidence = []
                            print("list_result:", list_result)
                            print("==================================")
                            print("list_confidence:", list_confidence)
                            print("Extract image", check_num, "success.")

                            # print(df)
                        else:
                            error_list.append(dict_result)
                            dict_result = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}
                            dict_confidence = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}

                except Exception as e:
                    print("Error!, ")
                    print(str(e))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    
                    print(exc_type, fname, exc_tb.tb_lineno)

                    logging.error(path + " "+str(e))
                    msg_error = str(e)
                    dict_result["error"].append(e)
                    error_list.append(dict_result)
                    dict_result = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}
                    dict_confidence = {'ss':[], 'sb':[], 'sd':[], 'rs':[], 'rb':[], 'rd':[], 'sis':[], 'ris':[], 'error':[]}
                    # break
        else:
            msg_error = "Found files that are not Dicom files. Please check the file and resubmit."
            break

    print("error", error_list)
    # print(msg_error)
    return df, df_conf, msg_error

def crop_img(img):
    img = img[img.shape[0]-1025: , :]
    # print("crop", img.shape[0])
    # cv2.imshow('window2', img)
    # cv2.waitKey(0)
    return img

def check_version_img(img):
    # cv2.imshow('window2', img)
    # cv2.waitKey(0)
    # print(img.shape[0])
    if(img.shape[0] == 1024):
        img = crop_img(img)
    if(img.shape[1] == 1024):
        version = "old"
    elif(img.shape[1] > 1000):
        version = "new"
    else:
        version = "old"
    # print(version)
    return version

def readdcm(path, hn):
  
  ds = pydicom.dcmread(path)
  img = ds.pixel_array

  return img, ds

def check_number_file(filename):
    # print(filename)
    if("ss" in filename):
        return "1", "ss"
    elif("sb" in filename):
        return "2", "sb"
    elif("sd" in filename):
        return "3", "sd"
    elif("rs" in filename):
        return "4", "rs"
    elif("rb" in filename):
        return "5", "rb"
    elif("rd" in filename):
        return "6", "rd"
    elif("sis" in filename):
        return "7", "sis"
    elif("ris" in filename):
        return "8", "ris"
    else:
        return "0", "others"

def main(path, hn):
    # directory = os.path.join(os.path.dirname( __file__ ), path)
    directory = path
    
    try:
        extract_df, confidence_df, msg_error = call_process(directory, hn)
        print(extract_df)
        print(confidence_df)
        print(msg_error)


        if msg_error != "":
            print("Found Error Reason:", msg_error)
            raise Exception('ไม่สามารถสกัดข้อมูลผู้ป่วย')
        if extract_df.empty:
            raise Exception('ไม่สามารถสกัดข้อมูลผู้ป่วย')
        
        print("Extracted quantitative Success:", hn)

    except Exception as e:
        print("Found Error Reason:", e)
        raise Exception(e)

    return extract_df, confidence_df

# df, condf = main("D:\Dropbox\Rjh_Kmitl_Dev\data_for_test\\test dicom_tiff files\\039192-52\dicom\\", "039192-52")