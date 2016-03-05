
# coding: utf-8

# In[3]:

import os
import csv
import pprint
from collections import defaultdict

INFILE = '2008election_wv.csv'
OUTFILE = 'clean2008election_wv.csv'
# header names: cmte_id,cand_id,cand_nm,contbr_nm,contbr_city,contbr_st,contbr_zip,contbr_employer,contbr_occupation,
#               contb_receipt_amt,contb_receipt_dt,receipt_desc,memo_cd,memo_text,form_tp,file_num,tran_id,election_tp

def parse_file(datafile):
    """
    Reads in a CSV and creates a list of dictionaries representing each row of data
    
    Args:
      datafile: The input csv file to process
      
    Returns:
      data: A list of dictionaries representing each row in the csv file
    """
    data = []
    
    with open(datafile, "rb") as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            
            data.append(row)
            
    return data

def write_file(data, datafile):
    """
    Writes a list of dictionaries of data to a datafile
    Ignores any contribution amounts that are less than zero (refunds)
    
    Args:
      data: A list of dictionaries
      datafile: The out csv file to write to
      
    Returns:
      None
    """
    with open(OUTFILE, 'wb') as csvfile:
        
        fieldnames = ['cmte_id','cand_id','cand_nm','contbr_nm','contbr_city','contbr_st','contbr_zip','contbr_employer',
                      'contbr_occupation','occupation_category','contb_receipt_amt','contb_receipt_dt',
                      'receipt_desc','memo_cd','memo_text','form_tp','file_num','tran_id','election_tp']
        
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        
        writer.writeheader()
        
        for row in data:
            
            if float(row['contb_receipt_amt']) > 0:
                
                writer.writerow(row)

def audit_occupations(data):
    """
    Looks for certain keywords in the 'contbr_occupation' column from the csv file
    Modifies the global variable election_data_raw
    
    Args:
      data: A list of dictionaries
      
    Returns:
      None
    """
    EDUCATION_OCCUPATIONS = ['TEACHER', 'HIGH SCHOOL', 'PRINCIPAL', 'EDUCATION', 'INSTRUCTOR',
                             'PROFESSOR', 'LIBRARIAN', 'DEAN', 'GUIDANCE COUNSELOR', 'GRADUATE',
                             'SCHOOL COUNSELOR', 'SUPERINTENDENT', 'VISITING LECTURER', 'COLLEGE',
                             'EDUCATOR']
    
    LEGAL_OCCUPATIONS = ['ATTY', 'ATTORNEY', 'LAWYER', 'LAW CLERK', 'LEGAL ASSISTANT',
                         'LEGAL SECRETARY', 'PARALEGAL']
    
    EXECUTIVE_OCCUPATIONS = ['CEO', 'CFO', 'CHAIRMAN', 'MANAGER', 'MANAGING DIRECTOR',
                             'MANAGEMENT', 'OPERATIONS DIRECTOR', 'OWNER', 'PARTNER',
                             'PRESIDENT', 'VP', 'C.E.O', 'DIRECTOR', 'MGMT']
    
    UNEMPLOYED_OCCUPATIONS = ['NOT EMPLOYED', 'UNEMPLOYED', 'JOB OUT SOURCED']
    
    HOMEMAKER_OCCUPATIONS = ['HOMEMAKER', 'HOUSE HUSBAND', 'HOUSEWIFE', 'MOM']
    
    SELF_EMPLOYED_OCCUPATIONS = ['SELF']
    
    POLITICAL_OCCUPATIONS = ['JUDGE', 'CITY COUNCIL', 'POLITICAL', 'TOWN COUNCIL']
    
    RELIGIOUS_OCCUPATIONS = ['MINISTER', 'PASTOR', 'CHURCH', 'CLERGY']
    
    RETIRED_OCCUPATIONS = ['RETIRED']
    
    STUDENT_OCCUPATIONS = ['STUDENT']
    
    MEDICAL_OCCUPATIONS = ['PHYSICIAN', 'ACUPUNCTURIST', 'CARDIOLOGIST', 'NURSE', 'MEDICAL',
                           'CHIROPRACTOR', 'PHARMACIST', 'PSYCHOLOGIST', 'DENTAL', 'DENTIST',
                           'DIABETES', 'DIETITIAN', 'DOC', 'DOCTOR', 'HEALTH CARE', 'HELATH',
                           'HEALTH', 'HOSPITAL', 'MED', 'NEUROSURGEON', 'OPTOMETRIST',
                           'SURGEON', 'PHARMACIST', 'PHARMACY', 'PHYSICAL THERAPIST',
                           'PHSICIAN', 'PHYCHOLOGIST', 'RADIOLOGIST', 'RADIOLOGY', 'RN']
    
    OCCUPATIONS = {'EDUCATION' : EDUCATION_OCCUPATIONS,
                   'LEGAL' : LEGAL_OCCUPATIONS,
                   'EXECUTIVE' : EXECUTIVE_OCCUPATIONS,
                   'UNEMPLOYED' : UNEMPLOYED_OCCUPATIONS,
                   'HOMEMAKER' : HOMEMAKER_OCCUPATIONS,
                   'SELF_EMPLOYED' : SELF_EMPLOYED_OCCUPATIONS,
                   'POLITICAL' : POLITICAL_OCCUPATIONS,
                   'RELIGIOUS' : RELIGIOUS_OCCUPATIONS,
                   'RETIRED' : RETIRED_OCCUPATIONS,
                   'STUDENT' : STUDENT_OCCUPATIONS,
                   'MEDICAL' : MEDICAL_OCCUPATIONS
                  }
    
    for i, row in enumerate(data):
        
        for key, occupation_list in OCCUPATIONS.iteritems():
        
            for occupation in occupation_list:
                
                if row['contbr_occupation'].find(occupation) != -1:
                    
                    #categories[key].add(row['contbr_occupation'])
                    
                    election_data_raw[i]['occupation_category'] = key
            
        if 'occupation_category' not in election_data_raw[i].keys():
            
            election_data_raw[i]['occupation_category'] = 'OTHER'
                     
# Process the 2008 election csv file
election_data_raw = parse_file(INFILE)
audit_occupations(election_data_raw)
write_file(election_data_raw, OUTFILE)


# In[ ]:



