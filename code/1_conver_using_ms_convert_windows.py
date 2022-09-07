import os
import pandas as pd
import subprocess

#'C:\\Program Files\\ProteoWizard\\ProteoWizard 3.0.18282.8016b683d\\msconvert.exe'
import glob
from datetime import date


os.chdir("K:\DF_LAB_FILES\CODE_GIT_HUB_2017_Aug_31\Compounds_Across_Amazon_XCMS_3_V1_2022_7_26")
uplc_results=pd.read_csv("./data/text_xcms.csv")
uplc_results


converted_path="K:\\Lab_Map\\Database\\2015_Relational_DB\\DATA_STORAGE\\UPLC_MS_DATA\\Data_Not_Active_Projects_etc\\10_Converted_Data\\Ecuador_Amazon\\"
raw_path= "K:\\Lab_Map\\Database\\2015_Relational_DB\\DATA_STORAGE\\UPLC_MS_DATA\\8_Active_Projects/Ecuador_Amazon.PRO\\Data\\"

#make projcet folder:

if not os.path.exists(converted_path+"Standard"):
    os.makedirs(converted_path+"Standard")

if not os.path.exists(converted_path+"Blank"):
    os.makedirs(converted_path+"Blank")

for folder in uplc_results.Associated_Combined.dropna().unique():
    if not os.path.exists(converted_path+  str(folder)):
        print("writing " + str(folder))
        os.makedirs(converted_path+ str(folder))
    
###### Ecuador files
#msconver_exe= '"C:\\Users\\dlforrister\\AppData\\Local\\Apps\\ProteoWizard 3.0.22208.6839020 64-bit\\msconvert.exe"'  
msconvert = 'msconvert.exe --mzML --32 --zlib --filter "msLevel 1-2" '

#list all files in raw folder
files_raw = [os.path.basename(x) for x in glob.glob(raw_path + "*.raw")]
failed_files=pd.DataFrame()
#row = uplc_results.iloc[0]
for index, row in uplc_results.iterrows():
    uplc_file_to_convert = row["file_name"]
    print(uplc_file_to_convert)
    if uplc_file_to_convert + ".raw" not in files_raw:
        print(uplc_file_to_convert + " unable to be converted")
        failed_files.append(pd.DataFrame({'file_name':[row["file_name"]],'index': [index],'reason':["file not in raw file folder"]}))
    
    raw_path_ind= raw_path + uplc_file_to_convert + ".raw"
    
    if row["sample_type"] == "Standard":
        output=converted_path+"Standard\\"

    if row["sample_type"] == "Blank":
        output=converted_path+"Blank\\"

    if row["sample_type"] == "Sample":
        output=converted_path + str(row["Associated_Combined"])+"\\"

    if index % 10 == 0:
        print("converting " + str(index) + " of " + str(len(uplc_results.index)))
    if not os.path.exists(output+ "\\"+ uplc_file_to_convert + ".mzML"):
        try:
            mzxml_path = "-o " + output
            msconvert_com = msconvert  + raw_path_ind + " " + mzxml_path
            print(raw_path_ind)
            #subprocess.check_call(msconvert_com,shell=True)
            subprocess.call(msconvert_com,shell=True)
        except Exception as e:
                print(" unable to be converted" + uplc_file_to_convert)
                failed_files.append(pd.DataFrame({'file_name':[row["file_name"]],'index': [index],'reason':["msconvert issue"]}))

        
    
failed_files
