# importing csv module
import csv
from flask import render_template, url_for, flash, redirect, request,jsonify
from werkzeug.utils import secure_filename
import random
import os
from app import app, db, bcrypt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import random
from linkedin_scraper import Company, actions
from time import sleep
from parsel import Selector
import requests
import csv
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
from os import walk
# initializing the titles and rows list
fields = []
rows = []
profile_data_list=[]
from flask import Flask, render_template, request
global people_name


local_list = []
linkedindata_list =[]
url_not_found_list = []
a_list = []
b_list = []
res = []
reg_fields      = ['Website', 'Company Name','Full Address', 'Postcode','Phone', 'Registration Number', 'Career Page URL','Linkedin URL', "Email", "Instagram_url", "Facebook_url", "Twitter_url",'Industry Sector','Company_size_info']
linkedinfields  = ['Website', 'Industry Sector','Company Type','Company_size_info']
empfields = ['Links']
profile_fields  = ['Name', 'Designation',"Company","Address","Duration", 'Emp Link']


# app = Flask(__name__)
# app.secret_key = 'secret_key'



# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'login'

# from routes import profile_scrapper

# app.register_blueprint(linkedin_scrapper.mod)
# app.register_blueprint(profile_scrapper.mod)





def getdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') 
    return soup

@app.route('/', methods=['GET', 'POST'])
@login_required
def reg_file():
    if current_user.is_active==1:
        if request.method == 'POST':
            path = 'static/'
            for folder, subfolders, files in os.walk('static/'):
                for file in files:
                    if file.endswith('.csv'):
                        path = os.path.join(folder, file)
                        print('deleted : ', path )
                        os.remove(path)

           
            resume      = request.files['files']
            people_name = request.form['people_name']
            strfilename = str(resume)
            filename    = secure_filename(resume.filename)
            ext         = filename.split('.')
            name        = str(random.randint(1000, 10000)) + '.' + ext[len(ext) - 1]
            resume.save(os.path.join(os.getcwd() + '/app/static', name))
            df = pd.read_csv (r'G:/rishabh/test/app/static/'+name)
            namelist = df.iloc[:,0].tolist()
            formattedname = df.iloc[:,1].tolist()
            p_data        = []
            p_data.append(people_name)
            reg_data(namelist,formattedname,p_data)
        # driver.close()
        return render_template('index.html')
    else:
        print(current_user.is_active,"****")
        flash('Login Unsuccessful. Please contact to admin', 'danger')
        return redirect(url_for('logout'))



@app.route('/linkedin_scrapper', methods=['GET', 'POST'])
@login_required
def linkedin_scrapper():
    

    if request.method == 'POST':
        directory = 'app/static/'
        files_in_directory = os.listdir(directory)
        filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        resume        = request.files['files']
        people_name   = request.form['people_name']
        strfilename   = str(resume)
        filename      = secure_filename(resume.filename)
        ext           = filename.split('.')
        name          = str(random.randint(1000, 10000)) + '.' + ext[len(ext) - 1]
        resume.save(os.path.join(os.getcwd() + '/app/static', name))
        df            = pd.read_csv (r'G:/rishabh/test/app/static/'+name)
        print(df,"***")
        linkedinlist  = df.iloc[:,7].tolist()
        company_name  = df.iloc[:,1].tolist()
        p_data        = []
        p_data.append(people_name)
        link_data(linkedinlist,company_name,p_data)
    return render_template('linkedin_scrapper.html')


@app.route('/profile_scrapper', methods=['GET', 'POST'])
@login_required
def profile_scrapper():
    if request.method == 'POST':
        directory = 'app/static/'
        files_in_directory = os.listdir(directory)
        filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)

        resume        = request.files['files']
        # people_name   = request.form['people_name']
        strfilename   = str(resume)
        filename      = secure_filename(resume.filename)
        ext           = filename.split('.')
        name          = str(random.randint(1000, 10000)) + '.' + ext[len(ext) - 1]
        resume.save(os.path.join(os.getcwd() + '/app/static', name))

        df            = pd.read_csv (r'G:/rishabh/test/app/static/'+name)
        linkedinlist  = df.iloc[:,0].tolist()
        
        profile_data(linkedinlist)
    return render_template('profile_scrapper.html')




data = ''
data_list=[]
wrong_url_list = []
filename =''

def findlinkedinreg(formattedname):
    
    try:
        driver.get("https://www.google.com/search?q=" +
                                formattedname+" "+"linkedin" + "&start=" + str(0))
        driver.implicitly_wait(1)
    except Exception as e:
        print(e,"_______________________error_____________________")

    results = driver.find_elements_by_css_selector('div.g')
    link = results[0].find_element_by_tag_name("a")
    href = link.get_attribute("href")
    sleep(1)
    current_url = href
    return current_url



#find registration number

def find_registration(formattedname):
    # sleep(0.5)
    # op = webdriver.ChromeOptions()
    # op.add_argument('headless')
    # driver = webdriver.Chrome()
    print(formattedname,"888888888888888888888888888888")
    soup = ''
    loop_counter = 0
    reg_num = ''
    address = ''
    postalcode = ''
    contact    = ''
    converturl   = re.sub("[' ,)(]", "+", str(formattedname))
    a ="https://find-and-update.company-information.service.gov.uk/search/companies?q="+converturl
    soup = getdata(a)
    images = soup.select('a')
    
    reg = soup.find_all("li", {"class": "type-company"})
    for i in reg:
        if loop_counter==0:
            ak = i.find_all("p")
            reg_num =  ak[0].get_text().split("-",1)[0]
            address =  ak[1].get_text()
            postalcode = str(address)[-8:]
            reg_num    = reg_num.replace(',','')
            break
        
        loop_counter = loop_counter+1

    try:
        driver.get("https://www.google.com/search?q=" +
                                    formattedname+ "&start=" + str(0))
        driver.implicitly_wait(1)
    except Exception as e:
        print(e,"_______________________error_____________________")
 
    
    
    current_url1 = driver.current_url
    sleep(1.5)
    url_data=driver.page_source
    
    if url_data:
        sleep(0.5)
        url_soup = BeautifulSoup(url_data, 'html.parser')
        for data in url_soup.find_all("span"):
            abc =data.find_all("span", {"class": "LrzXr zdqRlf kno-fv"})
            
            if abc:
                contact = abc[0].get_text()
    # phone       = phone.find_all("span", {"class": "LrzXr zdqRlf kno-fv"})
    # print

    #find linkedin link
    linkedin_url = findlinkedinreg(formattedname)
    return reg_num,address,postalcode,contact,linkedin_url



def find_career(career_url,formattedname):
    careers   = ''
    careers_url = ""
    email       = ""
    
    if str(career_url)!="nan" and str(career_url)!="":
        if not "www" in str(career_url):
            
            split_url = career_url.split("//",1)[1]
            split_url = "http://www."+split_url
        else:
            split_url = career_url.split("www.",1)[1]
            split_url = "http://www."+split_url

    else:
        try:
            driver.get("https://www.google.com/search?q="+
                                formattedname+"&start="+str(0))
            driver.implicitly_wait(1)
        except Exception as e:
            print(e,"_______________________error_____________________")

        current_url1 = driver.current_url

        results = driver.find_elements_by_css_selector('div.g')
        link = results[0].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        # sleep(1)   
        split_url = href
        split_url = split_url.split("www.",1)[1]
        split_url = "http://www."+split_url
    
    soup      = getdata(split_url)
    
    careers   = ''
    linkdin_url = ''
    facebook_url = ''
    twitter_url = ''
    instagram_url = ''
    images    = soup.select('a')
    for image in images:
        
        src = image.get('href')
        text1 = image.get('text')


        if "career" in str(src)  or "careers" in str(src) or "job" in str(src) or "recruit" in str(src):
            # data.append("careers")
            
            careers = src
           

        if "linkedin" in str(src):
            linkdin_url = src


        #facebook_url 
        if "facebook" in str(src):
            if not "?" in str(src):
                facebook_url = src

        #facebook_url 
        if "twitter" in str(src):
            if not "?" in str(src):
                twitter_url = src

        #facebook_url 
        if "instagram" in str(src):
            if not "?" in str(src):
                instagram_url = src

        mail_list = re.findall('\w+@\w+\.{1}\w+', src)
        if mail_list:
            email = re.sub("[' ,)(]", "+", str(mail_list))


        else:
            if text1:
                mail_list1 = re.findall('\w+@\w+\.{1}\w+', str(text1))
                if mail_list:
                    email = re.sub("[' ,)(]", "+", str(mail_list1))
                else:
                    email = ""

    if split_url:
        if "www" in str(careers) or "http" in str(careers):
            careers_url = careers

        else:
            
            c = split_url+"/",careers
            c = re.sub("[' ,)(]", "", str(c))
            careers_url =str(c).strip()
    # driver.close()
    print(email,"email", instagram_url,"instagram_url",twitter_url,"twitter_url",facebook_url)
    return careers_url,linkdin_url,split_url,email, instagram_url,facebook_url,twitter_url



def generate_csv(filename):
    # # writing to csv file
    sleep(0.5)
    # print(data_list,"data_listdata_list")
    with open("app/static/company_details/"+filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(reg_fields)
        # writing the data rows
        csvwriter.writerows(data_list)

def reg_data(namelist,formattedname,p_data):
    counter = 1
    limit   = 2
    count_line = [1]
    for i,j in zip(formattedname,namelist):
        
        if str(j)!="nan":
            print("********************")
            pass
        else:
            j =''

            

        d=[]
        e=[]
        add_data  = []
        e.append(j)
        d.append(i)
        linkedinlist = []
        # pool = Pool(processes=4)
        try:
            find_career_data = list(map(find_career,e,d))
        except Exception as f:
            print(f,"find_career___________error")
        careers_url,linkdin_url,split_url,email,instagram_url,facebook_url, twitter_url = find_career_data[0]

        
        try:
            find_registration_data = ThreadPool(1).map(find_registration,d)
        except Exception as e:
            print(e,"find_registration___________error")
        reg_num,address,postalcode,contact,linkedin_url = find_registration_data[0]

        
        #linkedin_data
        linkedinlist.append(linkedin_url)
        # try:
        linkdindata = list(map(findlinkedin,linkedinlist,p_data,d,count_line))
            # except Exception as e:
            #     print(e,"findlinkedin___________error")
        website_info,Industry_info,Type,Company_size_info,emp_linklist = linkdindata[0]
        
        
        if split_url:
            add_data.append(split_url)
        else:
            add_data.append("")
        add_data.append(i)

        if address:
            add_data.append(address)
        else:
            add_data.append("")

        if postalcode:
            add_data.append(postalcode)
        else:
            add_data.append("")

        if contact:
            add_data.append(contact)
        else:
            add_data.append("")

        if reg_num:
            add_data.append(reg_num)
        else:
            add_data.append("")

        if careers_url:
            add_data.append(careers_url)
        else:
            add_data.append("")

        if linkedin_url:
            add_data.append(linkedin_url)
        else:
            add_data.append("")

        if email:
            add_data.append(email)
        else:
            add_data.append("")

        if instagram_url:
            add_data.append(instagram_url)
        else:
            add_data.append("")

        if facebook_url:
            add_data.append(facebook_url)
        else:
            add_data.append("")

        if twitter_url:
            add_data.append(twitter_url)
        else:
            add_data.append("")

        #linkedin info add

        if Industry_info:
            add_data.append(Industry_info)
        else:
            add_data.append("")


        # if Type:
        #     add_data.append(Type)
        # else:
        #     add_data.append("")
        if Company_size_info:
            add_data.append(Company_size_info)
        else:
            add_data.append("")

        count_line[0] =counter+1
        local_list.append(emp_linklist)
        data_list.append(add_data)

    fname       = str(random.randint(1000, 10000))+".csv"
    filename    = "company_details"+fname
    emp_profile = "emp_profile_link"+fname

    ab  = [item for sublist in local_list for item in sublist]
    abc = extractDigits(ab)

    sleep(2)
    generate_csv(filename)
    generate_empcsv(emp_profile)
    
    










########################################################33
#linkedin_scrapper

def findlinkedin(company_link,pc,company_name,count_line):
    
    company_link   = str(re.sub("[' ,)(]", "", str(company_link)))
    print(pc,"***********************###",company_link,"___",company_name)
    url_data = ''
    images   = ''
    src      = ''
    address1 = ""
    address2 = ""
    emp_url  = ""
    
    employee_pos  = ""
    employee_name = ""
    website       = ""
    phone_info    = ""
    Industry_info = ""
    Type          = ""
    Founded       = ""
    Company_size_info  = ""
    website_info   = ""
    linkedin_info      = []
    emp_url_list       = []
    employee_pos_list  = []
    employee_name_list = []
    emp_linklist = []
    linkdin_url  = ""
    if "linkedin" in str(company_link):

        # company_link = company_link.split("?",1)[0]
        
        driver.get(company_link+"/about/")
        sleep(5)
        url_data=driver.page_source
        if url_data:
            sleep(0.5)
            url_soup = BeautifulSoup(url_data, 'html.parser')
            index = 0
            for data,i in zip(url_soup.find_all("dt"),url_soup.find_all("dd")):
                
                # if "Website" in str(data.get_text().strip()):
                #     for j in i.find("span", {"class": "link-without-visited-state"}):
                #         website_info =j.get_text()
                        
                        
                # if "Phone" in str(data.get_text().strip()):
                #     for k in i.find("span", {"class": "link-without-visited-state"}):
                #         phone_info =k.get_text()
                #         # print(phone_info,"PhonePhonePhone")

                if "Industry" in str(data.get_text().strip()):
                    Industry_info = i.get_text().strip()

                if "Company size" in str(data.get_text().strip()):
                    Company_size_info = i.get_text().strip()

                if "Type" in str(data.get_text().strip()):
                    Type = i.get_text().strip()

                if "Founded" in str(data.get_text().strip()):
                    Founded = i.get_text().strip()


            
        else:
            pass


        #find employee link from linkedin xray
        search_form_name = company_name +" "+ pc
        try:
            driver.get("https://recruitmentgeek.com/tools/linkedin")
            driver.implicitly_wait(1)
        except Exception as e:
            print(e,"_______________________error_____________________")
        driver.find_element_by_xpath("//input[@class='gsc-input' and @type='text']").send_keys(search_form_name)
        sleep(2)
        if count_line==1:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqs-cookie-banner-v2-accept sqs-cookie-banner-v2-cta']"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='sqs-popup-overlay-close']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='gsc-search-button gsc-search-button-v2']"))).click()
        sleep(2)
        url_data=driver.page_source
        if url_data:
            sleep(0.5)
            url_soup = BeautifulSoup(url_data, 'html.parser')
            for data in url_soup.find_all("div", {"class": "gs-webResult gs-result"}):
                if data:
                    anchor = data.find_all("a", {"class": "gs-title"})
                    ancor_data =anchor[0].text

                    if company_name.lower() in str(ancor_data.lower()) and pc.lower() in str(ancor_data.lower()):
                        try:
                            var1 = anchor[0].get('href')
                            emp_linklist.append(var1)
                        except Exception as e:
                            print(e,"error***************************************")
                        


        #find emplyees
        # driver.get(company_link+"/people/?keywords="+pc)
        # # sleep(10)
        # sleep(7)
        # pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
        # run_time, max_run_time = 0, 1
        # while True:
        #     iteration_start = time.time()
        #     # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        #     driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')

        #     post_scroll_height = driver.execute_script('return document.body.scrollHeight;')

        #     scrolled = post_scroll_height != pre_scroll_height
        #     timed_out = run_time >= max_run_time

        #     if scrolled:
        #         run_time = 0
        #         pre_scroll_height = post_scroll_height
        #     elif not scrolled and not timed_out:
        #         run_time += time.time() - iteration_start
        #     elif not scrolled and timed_out:
        #         break
        # sleep(5)
        # people_data=driver.page_source
        
        # if people_data:
            
        #     people_soup = BeautifulSoup(people_data, 'html.parser')
        #     images = people_soup.select('li')
        #     employee_postion_tuple = []
        #     employee_postion_list  = []
        #     employee_name_tuple    = []
        #     employee_name_list     = ()
            
        #     for i in images:
        #         find_designation   = i.find_all("div", {"class": "lt-line-clamp lt-line-clamp--multi-line ember-view"})
        #         emp__name          = i.find("div", {"class": "org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view"})
        #         emp_link =           i.find("a",{"class":"link-without-visited-state"})
        #         # print("lolololo",emp_link)
        #         if emp_link:
        #             try:
        #                 var1 = "https://www.linkedin.com"+ emp_link.get('href')
        #                 emp_linklist.append(var1)
        #                 print(var1,"var1var1var1_____________________$$$$$$$$$")
        #             except Exception as e:
        #                 print(e,"error***************************************")
    else:
        print("linkedin url not found")
        url_not_found_list.append(company_link)
    if emp_linklist:
        emp_linklist.pop(0)
    return company_name,Industry_info,Type,Company_size_info,emp_linklist




def generate_company_details_csv(filename):
    # # writing to csv file
    sleep(0.5)
    with open("app/static/company_linkedin_details/"+filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(linkedinfields)
        # writing the data rows
        csvwriter.writerows(linkedindata_list)

def extractDigits(lst):
    
    for el in lst:
        sub = el.split(', ')
        res.append(sub)
      
    return(res)


def generate_empcsv(emp_profile):
    
    sleep(0.5)

    with open("app/static/emp_profile_link/"+emp_profile, 'a') as csvfi:
        # creating a csv writer object
        csvwriter = csv.writer(csvfi)
        # writing the fields
        csvwriter.writerow(empfields)
        # writing the data rows
        csvwriter.writerows(res)

def link_data(namelist,company_name,p_data):
    counter = 1
    limit   = 2
    count_line = [1]
    for i,j in zip(namelist,company_name):
        if str(i)!="nan" and str(j)!="nan":
            # print(company_name,"____________")
            # pass
            d=[]
            e=[]
            link_data  = []
            d.append(i)
            e.append(j)
            
            # try:
            linkdindata = list(map(findlinkedin,d,p_data,e,count_line))
            # except Exception as e:
            #     print(e,"findlinkedin___________error")
             
            website_info,Industry_info,Type,Company_size_info,emp_linklist = linkdindata[0]
            
            if website_info:
                link_data.append(website_info)
            else:
                link_data.append("")

            

            if Industry_info:
                link_data.append(Industry_info)
            else:
                link_data.append("")


            if Type:
                link_data.append(Type)
            else:
                link_data.append("")
            if Company_size_info:
                link_data.append(Company_size_info)
            else:
                link_data.append("")

            

            linkedindata_list.append(link_data)
            local_list.append(emp_linklist)
            count_line[0] =counter+1
            # if counter==limit:
            #     break
            # counter = counter+1
            
    
    ab  = [item for sublist in local_list for item in sublist]
    abc = extractDigits(ab)
    # abc = str(abc)[1:-1]
    

    
    
    filename    = str(random.randint(1000, 10000))+".csv"
    emp_profile = "emp_profile_link"+filename
    filename    = "company_linkedin_details"+filename
    
    sleep(2)
    generate_company_details_csv(filename)
    generate_empcsv(emp_profile)
    


















##############################################################################
#linkedinprofile_scrapper



def findlinkedinprofile(company_link):
    
    # company_link   = str(re.sub("[' ,)(]", "", str(company_link)))
    emp_name    = ''
    # print("***********************###",company_link)
    company_link   = company_link.replace('uk','www')
    url_soup    = ''
    get_text    = ''
    emp_name    = ''
    designation = ''
    company     = ''
    address     = ''
    duration    = ''
    soup        = ''
    driver.get(company_link)
    get_text    = driver.page_source
    # sleep(2)
    soup        = BeautifulSoup(get_text, "html.parser")
    # sleep(2)
    emp_name    =  soup.find("h1", {"class": "text-heading-xlarge inline t-24 v-align-middle break-words"})
    designation =  soup.find("h3", {"class": "t-16 t-black t-bold"})
    company     =  soup.find("p", {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
    address     =  soup.find("span", {"class": "text-body-small inline t-black--light break-words"})
    duration    =  soup.find("h4", {"class": "pv-entity__date-range t-14 t-black--light t-normal"})

   
    try:
        emp_name = emp_name.get_text().strip()
    except Exception as e:
        print(e,"emp_name error")

    try:
        designation = designation.get_text().strip()
    except Exception as e:
        print(e,"designation error")


    try:
        company = company.get_text().strip()
    except Exception as e:
        print(e,"company error")
    try:
        address = address.get_text().strip()
    except Exception as e:
        print(e,"address error")

    try:
        duration = duration.get_text().strip()
    except Exception as e:
        print(e,"duration error")


    
    
    return emp_name,designation,company,address,duration

def generateprofile_csv(filename):
    # # writing to csv file
    sleep(0.5)
    with open("app/static/all_employee_details/"+filename, 'w', encoding="utf-8") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(profile_fields)
        # writing the data rows
        csvwriter.writerows(profile_data_list)


def profile_data(namelist):
    counter = 0
    limit   = 5
    
    for i in namelist:
        if str(i)!="nan":
            d=[]
            add_data  = []
            d.append(i)
            
            
            try:
                linkdindata = list(map(findlinkedinprofile,d))
            except Exception as e:
                print(e,"findlinkedin___________error")
             
            emp_name,designation,company,address,duration= linkdindata[0]
            
            if emp_name:
                add_data.append(emp_name)
            else:
                add_data.append("")

            if designation:
                add_data.append(designation)
            else:
                add_data.append("")

            if company:
                add_data.append(company)
            else:
                add_data.append("")

            if address:
                add_data.append(address)
            else:
                add_data.append("")
            if duration:
                add_data.append(duration)
            else:
                add_data.append("")
            
            add_data.append(i)
            profile_data_list.append(add_data)

            
    
    filename = "all_employee_details"+str(random.randint(1000, 10000))+".csv"
    sleep(2)
    generateprofile_csv(filename)
   







@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = LoginForm()
   
    if request.method == 'POST':
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            # print("****************88")
            return redirect(next_page) if next_page else redirect(url_for('reg_file'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        

    return render_template('sign-in.html', title = 'Log In', form = form)



# signup
@app.route("/sign-up", methods=['GET', 'POST'])
def Signup():
    form = RegistrationForm()
    if current_user.is_authenticated:
       return redirect(url_for('reg_file'))
    
   
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=hashed_password
                )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')

    return render_template('sign-up.html', title='Sign up', fm=form)


# alluser
@app.route("/user", methods=['GET', 'POST'])
def user():
    
    if current_user.usertype=='0':
        
        if request.method=="POST":
            userid = request.form['userid']
            status = request.form['status']
            if status=='0':
                new_status = False
                
            else:
                new_status = True
            print(new_status,"**",status,userid) 
            user = User.query.get_or_404(userid)
            user.is_active = new_status
            db.session.commit()
        all_user = User.query.all()
        return render_template('user.html', title='User',all_user=all_user)
    else:
        return redirect('/')



# signup
@app.route("/company-files", methods=['GET', 'POST'])
def allimages():
    f = []
    path = "app/static/company_details/"
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return render_template('files.html', title='Sign up',files=f)


# employee profile details
@app.route("/employee-files", methods=['GET', 'POST'])
def employeefiles():
    f = []
    path = "app/static/all_employee_details/"
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    print(f)
    return render_template('employee_profiles.html', title='Sign up',files=f)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#find duplicate data from csv file
# @app.route('/find-duplicate', methods=['GET', 'POST'])
# def findduplicate():
#     if request.method=="POST":
#         branch = []
#         file      = request.files['files']
#         data      = pd.read_csv(file)
#         if data:
#             test_list = ['ltd','inc','llp','llc']
#             for i in data.index:
#               x = data.iloc[i,0].find('-')
#               if x !=-1:
#                 # print(data.iloc[i,0])
#                 branch.append('Branch')
#               else:
#                 res = any(ele in data.iloc[i,0].lower() for ele in test_list)
#                 if res:
#                   branch.append('parent')
#                 else:
#                   branch.append('')



#             data['Branch'] = branch
#         else:
#             print("no data")












# if __name__ == '__main__':
#     app.run(debug=True, port=5000)





