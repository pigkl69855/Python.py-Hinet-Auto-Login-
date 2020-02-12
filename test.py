
# Hinet Auto Login 1.1.0  2020_2_12
# "上次成功連線時間" , "經過時間" 新功能增加完成



# 修正138 改為 2秒
# 修正145 改為 2秒
#  159 3sec


# 1.0 完成於 19/12/9  10:00am
# 只差實際使用上是否會出現錯誤

### 執行時需要有管理員權限 ###

#hinet正式版  0.9版  耗時5hr  


# 1.5hr 升級為 0.9.10  新功能 wifi自動重新連線
#   python Hinet_AutoConnect.py
# 15min 升級為 0.9.20 新功能 成功連線計次

#自動化偵測斷線     {改成被動強制重啟}
#可能主要WI-FI斷線    {待處理}
#可能沒進入正常網頁而崩潰 {待測試}
# 修正 browser.close() 改為 quit() 關閉所有的網頁 

#測試時可能要而外加上 try close 關閉瀏覽器 以免確定登入的提示框口 導致程式崩潰 {待測試}
# try 實行錯誤 應該會有錯誤類型  找到並用預防語法  {解決}
#如果要連線ps4還要自動開啟 熱點  {先決用手動開啟(先遠端到筆電上)}
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading

#設計斷線連線成功 計次紀錄  

resetNetWork=False

localtime = time.localtime(time.time())
TemporaryHour = localtime.tm_hour
TemporaryMin = localtime.tm_min
timePassCounter=0
# int ( timePassCounter ) 

#可能會造成雙網卡連線錯誤   {問題待發現}
#可試的方法 block wifi     {問題待發現}
def connect_wifi():
    response = os.system("netsh wlan connect name=\"CHT Wi-Fi(HiNet)\" interface=\"Wi-Fi 2\"")  #修改成hinet------------------
    # netsh wlan connect name=pccu interface=Wi-Fi  成功 (surface go)
    # netsh wlan connect name="CHT Wi-Fi(HiNet)" interface="Wi-Fi 2"
    # disconnect 分法 可能造成問題  (是否可以改成cmd模式)
def disconnect_wifi():
    response = os.system("netsh wlan disconnect interface=\"Wi-Fi 2\"")
    # netsh wlan disconnect interface="Wi-Fi 2"
def check_ping():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "@@@@@@@@@@@@@@@@@@@@@deBug---Network Active"
        print(pingstatus)
        return True
    else:
        pingstatus = "@@@@@@@@@@@@@@@@@@@@@deBug---Network Error"
        print(pingstatus)
        global timePassCounter
        timePassCounter=0
        return False

def delayCount():
    x=0
    while x != 600 :  # 原本為 600 測試 請改成 7
        time.sleep(1)
        x+=1
        global timePassCounter
        global TemporaryHour
        global TemporaryMin
        localtime = time.localtime(time.time())
        timePassCounter+=1
        mathMin=timePassCounter/60
        mathHour=mathMin/60

        if TemporaryHour > 12:
            # TemporaryHour -= 12
            print("deBug---delay秒數: ", x, "       成功重新連線次數", connectSuccessCount, "          等待10分鐘次數", ccount,
                  "       如果斷線輸入 \"r\"重新連網","      上次成功連線時間為 ", TemporaryHour-12, ":", TemporaryMin, "pm","  經過時間 ",int(mathHour),":",int(mathMin))

        else:
            print("deBug---delay秒數: ", x, "       成功重新連線次數", connectSuccessCount, "          等待10分鐘次數", ccount,
                  "       如果斷線輸入 \"r\"重新連網","      上次成功連線時間為 ", TemporaryHour, ":", TemporaryMin, "am","  經過時間 ",int(mathHour),":",int(mathMin))

        global resetNetWork
        if(resetNetWork==True):
            print("#####################deBug---收到 RESET指令 正在執行")
            x=600
            resetNetWork=False

def timeCounter():  #用來print 上次成功登入時間 與 連線經過時間
    localtime = time.localtime(time.time())
    global TemporaryHour
    global TemporaryMin
    TemporaryHour = localtime.tm_hour
    TemporaryMin = localtime.tm_min

    passHour=localtime.tm_hour-TemporaryHour
    passMin=localtime.tm_min-TemporaryMin
    
    if(TemporaryHour>12):
        TemporaryHour-=12
        print("上次成功連線時間為 ",TemporaryHour,":",TemporaryMin,"pm")
    else:
        print("上次成功連線時間為 ",TemporaryHour,":",TemporaryMin,"am")            

def userInput():
    while(True):
        ans=input()
        if ans=="r":
            global resetNetWork
            resetNetWork=True
        time.sleep(1)

t = threading.Thread(target=userInput)
t.start()

usernameStr = 'yourusername'
passwordStr = 'yourpassword'#密碼記得改正
situation=False 
#HinetLoginSmoothly=True    #此語法目前沒用 可能沒進入正常網頁而崩潰
connectSuccessCount=0  #Hinet帳密登入成功次數
ccount=0     #等待10分鐘次數

print("@@@@@@@@@@@@@@@@@@@@@deBug---啟動前delay八秒 可進行遠端斷線")
time.sleep(8)      #等候8秒

while True:  #延遲10分鐘
    if check_ping()==True:
        situation=True
    else:
        situation=False
    while situation!=True:
        print("@@@@@@@@@@@@@@@@@@@@@deBug---開啟瀏覽器中")
        browser = webdriver.Chrome()
        browser.get('https://authweb.hinet.net/auth/auth_login/login1?client_ip=100.64.123.240&session=&key=ca1776787eaca8c9f063fdcbc9597b17&loginurl=https%3A%2F%2Fwlangw.hinet.net%2Fv2_0%2Fcht_auth%2Fauth_page.php&vendor=cht&gwip=168.95.179.12&gwport=2%2F2%2F1%3A2706.0&eqs_vlanid=2706.0&umac=d8%3Ac4%3A97%3Ab8%3A74%3A5c')
        print("@@@@@@@@@@@@@@@@@@@@@deBug---進入網頁中")

        # fill in username and hit the next button
        #設定第二選項
        #if browser.find_element_by_css_selector("a[onclick=\"seltype(2)\"]"):
        try :
            print("@@@@@@@@@@@@@@@@@@@@@deBug---開始設定-設定第二選")
            selectHinet=browser.find_element_by_css_selector("input[id=\"option2\"]")
            selectHinet.click()
            #設定一個span 有關hinet與預付卡
            print("@@@@@@@@@@@@@@@@@@@@@deBug---完成-設定第二選")
            username = browser.find_element_by_css_selector("input[value=\"範例：87654321\"]")#將id搜尋改成name搜尋
            username.send_keys(usernameStr)
            print("@@@@@@@@@@@@@@@@@@@@@deBug---完成-帳號輸入")
            # wait for transition then continue to fill items

            
            time.sleep(0.5)
            print("@@@@@@@@@@@@@@@@@@@@@deBug---delay-500毫秒")
            
            # 98 行是否可以進行修正  目前password變數 看似用不到
            # 舊版
            # password = browser.find_element_by_css_selector("input[value=\"範例：87654321\"]").send_keys(Keys.TAB,"gibrhaud")
            # 新版
            browser.find_element_by_css_selector("input[value=\"範例：87654321\"]").send_keys(Keys.TAB,passwordStr)
            print("@@@@@@@@@@@@@@@@@@@@@deBug---send tab")
            
            print("@@@@@@@@@@@@@@@@@@@@@deBug---send password")
            
            #.send_keys(passwordStr)

        #   password = WebDriverWait(browser, 10).until(
        #      EC.presence_of_element_located((By.css.selector, "tr[id=\"hinet2\"]"))) #By.css.selector可能出問題
        #   password.send_keys(passwordStr)                       #<input name="passwd" type="password" class="input">
        #   print("@@@@@@@@@@@@@@@@@@@@@deBug---完成-密碼輸入")   #再不行改成 key pass tab

            #presence,ec,until
            signInButton = browser.find_element_by_css_selector("div[class=\"enterBtn\"]")#
            signInButton.click()
            print("@@@@@@@@@@@@@@@@@@@@@deBug---完成-Hinet登入")
            timeCounter()
        #else:
        #break

            #測試後移 (3行)
        except:                 #finally使用??   except
            print("@@@@@@@@@@@@@@@@@@@@@deBug---錯誤-未正常登入帳密-進入except")
            print("@@@@@@@@@@@@@@@@@@@@@deBug---#延遲5秒")
            time.sleep(2)      #延遲2秒
            print("@@@@@@@@@@@@@@@@@@@@@deBug---#網頁關閉")
            #browser.close()    #網頁關閉
            browser.quit() #-----------------------------------
        try:
            print("@@@@@@@@@@@@@@@@@@@@@deBug---正常-進入else")
            print("@@@@@@@@@@@@@@@@@@@@@deBug---#延遲5秒")
            time.sleep(2)      #延遲2秒
            print("@@@@@@@@@@@@@@@@@@@@@deBug---#網頁關閉")
            # browser.close()    #網頁關閉
            browser.quit() #-----------------------------------
            print("@@@@@@@@@@@@@@@@@@@@@deBug---#ping google.com測試 ~~測試是否可正常使用網路")
            if check_ping()==True:
                situation=True
                connectSuccessCount+=1
                print("成功重新連線次數",connectSuccessCount)
                print("@@@@@@@@@@@@@@@@@@@@@deBug---設定 bool--situation = True")
            else:
                print("@@@@@@@@@@@@@@@@@@@@@deBug---斷網重連---else:")
                disconnect_wifi()  #斷線網路
                print("@@@@@@@@@@@@@@@@@@@@@deBug---wifi斷線")
                time.sleep(3)      #等候3秒
                print("@@@@@@@@@@@@@@@@@@@@@deBug---斷網重連")
                connect_wifi()     #重新連線網路

        except:
            print("!!!!!!!!!!!!!!!!!!!!!!進入-except-程式可出錯")
            try:
                # browser.close()    #網頁關閉
                browser.quit() #-----------------------------------
            except:
                print("!!!!!!!!!!!!!!!!!!!!!!進入 第二次關閉網頁錯誤")
      
        if(situation==False):
            print("@@@@@@@@@@@@@@@@@@@@@deBug---斷網重連---2 except:")
            disconnect_wifi()  #斷線網路
            print("@@@@@@@@@@@@@@@@@@@@@deBug---wifi斷線-stop 5 sec")
            time.sleep(5)      #等候5秒
            print("@@@@@@@@@@@@@@@@@@@@@deBug---斷網重連")
            connect_wifi()
    if situation==True:
        ccount+=1
        delayCount()
    
