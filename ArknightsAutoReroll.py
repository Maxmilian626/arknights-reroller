#Arknights Automatic Reroller.  Based on https://github.com/nisegami/grand-order-reroller/blob/master/main.py
import cv2
import pyautogui
import time
import numpy as np
import os, os.path
import settings
import mailreader
from PIL import Image

#Constants
NEWBIEREROLL = False #Determines whether or not to do stage 0-1 for rerolling, and then whether or not to do the newbie banner.
HHTIX = 3 #default 3
CLOSENESS_THRESHOLD = .8
salt = settings.BASESALTNUMBER
#Position Dictionaries
DEFAULT = {'x':1020, 'y':1000}

UNDERSTOOD = {'x':900, 'y':790}
ACCOUNT_MANAGEMENT = {'x':1310, 'y':970}
GUEST = {'x':1340, 'y':715}
TOS_READ = {'x':930, 'y':860}
AGREE_TOS = {'x':1060, 'y':950}
NAME_FIELD = {'x': 750, 'y':600}
NAME_CONFIRM = {'x':925, 'y':730}

TWO_X = {'x':1560, 'y': 100}
CONFIRM = {'x':1210, 'y':730 }
CANCEL = {'x':655, 'y':730}
STARTSTAGE = {'x':1640, 'y':940}
MISSIONSTART = {'x':1565, 'y':730}
STAGEMENU = {'x':150, 'y':100}

SKIP_STORY = {'x':1675, 'y':95}
SKIP_SUMMON = {'x':1735, 'y':90}

MAINMENUEXIT = {'x':1700, 'y':110}

TENROLL = {'x':1575, 'y': 915}
ONEROLL = {'x':1280, 'y': 915}



#Operator Dictionaries
TEXAS = {'x1': 1570, 'y1':940, 'x2':850, 'y2':600, 'dx':300, 'dy':0} #dx dy is deploy direction.
EXU = {'x1': 1730, 'y1':940, 'x2':1000, 'y2':450, 'dx':300, 'dy':0}
RANGERS = {'x1':1080, 'y1':940, 'x2':1310, 'y2':280, 'dx':0, 'dy':300}
YATO = {'x1': 1240, 'y1':940, 'x2':1025, 'y2':410, 'dx':300, 'dy':0}



#Base Functions
def wait(given_time):
    time.sleep(given_time)

def click(x, y):
    pyautogui.click(x=x, y=y)

def deploy_operator(x1, y1, x2, y2, dx, dy):
    pyautogui.moveTo(x=x1, y=y1)
    wait(.5)
    pyautogui.dragTo(x2, y2, 2, button='left')
    new_x = x2 + dx
    new_y = y2 + dy
    pyautogui.dragTo(new_x, new_y, 1, button='left')

#Identify
def image_is_on_screen(template_name, region_param=(0,0,1919,1079)): #Region can be optimized.
    template = cv2.imread(os.path.join(
                                'templates',
                                template_name + '.png'),
                    cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(
                np.array(pyautogui.screenshot(
                        region=region_param)),
                cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= CLOSENESS_THRESHOLD)

    # Not sure why this works but okay
    for pt in zip(*loc[::-1]):
        return True

    return False

#Derivative Functions (CV)
def clickUntil(*images):
    try:
        while True:

                 for pos, image in enumerate(images):
                     if image_is_on_screen(image):
                         pyautogui.PAUSE = 1.5
                         wait(0.5)
                         return pos

                 for i in range(10):
                     click(**DEFAULT)
    except KeyboardInterrupt:
            print('\n')


def wait_until(*images):
    while True:
        for pos, image in enumerate(images):
            if image_is_on_screen(image):
                wait(0.5)
                return pos

#Derivative Functions (Mouse)
def agree_ToS():
    click(**TOS_READ)
    click(**AGREE_TOS)

def skip_story():
    click(**SKIP_STORY)
    wait_until('confirm')
    click(**CONFIRM)

def ten_roll(saltnum):
    click(**TENROLL)
    wait(2)
    click(**CONFIRM)
    wait_until('summonskip')
    click(**SKIP_SUMMON)
    wait(10)
    #wait_until('tenrollfinish') #no consistent way to determine random-visually.
    sc = pyautogui.screenshot(region=(50,150, 1800,900))
    rollNo = 'tenroll_'+ str(saltnum) + '.png'
    sc.save(os.path.join('rolls',rollNo))
    clickUntil('can_back')

def one_roll(salt, rollNumber, tutorial=False):
    click(**ONEROLL)
    if tutorial == False:
        wait_until('confirm')
        click(**CONFIRM)
    wait_until('summonskip')
    click(**SKIP_SUMMON)
    wait_until('char_summoned')
    sc = pyautogui.screenshot(region=(50,150, 1750,750))
    rollNo = 'oneroll_' + str(salt) + "_" + str(rollNumber) + '.png'
    sc.save(os.path.join('rolls',rollNo))
    if tutorial == False:
        clickUntil('can_back')


def screenshotTest():
    sc = pyautogui.screenshot(region=(50,150, 1750,750))
    rollNo = 'tenroll_test.png'
    sc.save(os.path.join('rolls',rollNo))



'''

#Required:
- Settings File - window size calibration.  Can make functions for relative positions to support variety of resolutions.
    -Native Screen Resolution = 1080x1920

#Future
- Screen Region Checking
- Image scaling for template matching.  If people are running at a higher/different resolution, the template needs to be constant.
- State Identification?
    - Battle (check for Cost) - logic loop for setting 2x.
    - Main Menu
- Multi-Instance Handling
- Bounding Box finding for more robust detection.

#Truly Automatic Rerolling
- Bind to email using SALT.
- Using gmail api, read email sent from info @yostar.com, constantly refreshing for newest.
- Parse email for numbers.
- Turn numbers into String
- PythonAutoGui type into the bind code area.
- Click(Submit)
- Logout

#Step List

- Automatic Email Binding (Doesn't require resetting)
    - Steps as mentioned above.  Restart, loop.
'''

def guestAccCreate():
    for i in range(2) #Do two sweeps for if understood.
        if image_is_on_screen('understood'):
            click(**UNDERSTOOD)
    wait_until('start')
    click(**ACCOUNT_MANAGEMENT)
    wait(1)
    click(**GUEST)
    wait(1)
    click(**CONFIRM) #When they ask about switching login.
    wait(1)
    click(**CONFIRM) #When they ask about erasing the stuff.

def agree_terms_of_service():
    wait_until('terms_of_service')
    agree_ToS()

def type_name():
    click(**NAME_FIELD)
    wait_until('keyboard ok') #sometimes doesn't get the keyboard up.
    wait(5)
    pyautogui.typewrite(settings.NAME, interval = 0.25)
    click(1720, 965) #Android OK Button
    wait(5) #wait until keyboard gone.
    click(**NAME_CONFIRM)
    print('name entered')

def battle0():
    wait_until('skip1')
    skip_story()
    print('battle0Start')
    clickUntil('deploy_texas')
    deploy_operator(**TEXAS)
    clickUntil('deploy_exusiai')
    deploy_operator(**EXU)
    clickUntil('texas_skill1')
    click(700, 460) #circle around Texas
    clickUntil('texas_skill2')
    click(1260, 600) #Texas' Skill use. Need better ID than "Use"
    clickUntil('c99')
    click(**TWO_X)
    clickUntil('skip2')
    skip_story()
    print('battle0Done')

def tutSummon():
    print('Tutorial Summon')
    wait_until('prts1')
    clickUntil('headhunt1')
    one_roll(salt,0, True)

def squadup():
    clickUntil('squad1')
    click(830, 320) #squad open spot.
    wait(2)
    click(730, 320) #select operator.
    wait(1)
    click(1675, 960) #exiting to home menu
    wait(1)
    click(410, 80)
    wait(1)
    click(170, 360)
    print('Tutorial Summon Done')

def zeroOneSelect():
    print('0-1 Select')
    clickUntil('0-1_start')
    wait(2)
    click(600, 600) #big blue button
    wait_until('0-1_select')
    click(930, 500) #0-1
    wait_until('startStage')
    click(**STARTSTAGE)
    wait_until('missionStart')
    click(**MISSIONSTART)
    wait_until('skip3')
    skip_story()
    print('0-1 Select Done')

def zeroOneCombat():
    print('0-1 Combat')
    wait_until('skip5')
    click(**DEFAULT)
    wait(1)
    click(**DEFAULT)
    print('deploying operators')
    deploy_operator(**RANGERS)
    wait(4)
    deploy_operator(**YATO)
    click(**TWO_X)
    wait_until('skip4')
    skip_story()
    print('0-1 Combat Done')

def TR1_select():
    print('TR-1')
    clickUntil('manage_mission')
    click(420,900)
    clickUntil('startStage')
    wait(2)
    click(**STARTSTAGE)

def TR1_start():
    clickUntil('tr1_start')
    wait(1)
    click(**MISSIONSTART)
    wait_until('skip5')
    skip_story()
    click(**STAGEMENU)
    click(1375, 820) #Confirm is a bit different position here.
    clickUntil('can_back')
    click(110, 80) #back button
    wait(2)
    click(110, 80) #get to front, ambushed by logins
    print('TR-1 Done')

def redeemDaily():
    print('Redeem Daily')
    wait_until('LMDGet')
    click(**DEFAULT)
    wait_until('menuexit')
    click(**MAINMENUEXIT)
    print('Redeem Daily Done')

def redeem7day():
    print('Redeem 7 day')
    wait_until('7day')
    click(500,800)#get Orundum
    wait_until('orundum_get')
    click(**DEFAULT)
    wait_until('rookiemission')
    click(230,340) #rookiemission Button
    wait_until('rookiemissionclear')
    click(1555,300)
    wait_until('orundum_get')
    click(**DEFAULT)
    wait_until('menuexit')
    click(1770,135) #exit is slightly different.
    print('Redeem 7 Day Done')

def redeemMail():
    print('Redeem Mail')
    wait_until('mail_available')
    click(310,80) #mailbox icon
    wait_until('mailbox_loaded')
    click(1600, 960) #CollectAll
    wait(2)
    # wait_until('savage_get')
    # wait(2)
    # click(**DEFAULT)
    # wait(6) #waiting for everything to load
    # click(**DEFAULT)
    # wait_until('mailcanback')
    clickUntil('mailcanback')
    click(120,90) #exit mailbox
    print('Redeem Mail Done')

def convertPO():
    print('Convert PO')
    wait_until('homepage')
    click(1475, 100) #convert button
    wait_until('convertMenuUp')
    for i in range(4):
        click(1630, 275)
        wait(1)
    click(1575,955) #confirm convert button
    print('Convert PO Done')

def roll10():
    print('Rolling')
    wait_until('homepage')
    click(1650, 740) #headhunt button
    wait_until('headhunt2')

    click(1750, 580) #next gacha
    wait_until('otherbanner') #confirm on the next banner and loaded
    print('ready to roll')
    ten_roll(salt)


def yolorolls():
    for i in range(HHTIX):
        one_roll(salt, i+1)

    click(100, 80) #back to main menu
    print('Rolling Done')

def bind_email():
    print('Binding')
    wait_until('homepage')
    click(100,80) #Gear on top left
    wait_until('account')
    click(250, 675) #Accounts Tab
    wait(1)
    click(1080, 260) #Bind
    wait(1)
    click(1000, 475) #mail enter
    wait_until('keyboard ok')
    wait(2)
    new_email= settings.EMAIL + "+" + str(salt) + "@gmail.com"
    pyautogui.typewrite(new_email, interval = 0.25)
    click(1720, 965) #Android kb OK Button

def confirm_email(mailreader):
    click(1200, 580) #the send code button.
    #now we do stuff like use the gmail api.
    code = mailreader.get_code(salt)
    print(code)
    click(900, 600) #code area
    wait_until('androidkbup')
    pyautogui.typewrite(code, interval = 0.25)
    click(1720, 965) #Android kb ok button
    wait(2)
    click(1000,700) #bind button
    wait_until('settings')
    click(1080,740)
    wait(1)
    click(**CONFIRM)
    print('Binding Done')


if __name__ == '__main__':
    mail = mailreader.snippet_reader()
    mail.main()

    try:
        while True:

            print salt
            guestAccCreate()
            agree_terms_of_service()
            type_name()
            battle0()
            tutSummon()
            squadup()
            zeroOneSelect()
            zeroOneCombat()
            TR1_select()
            TR1_start()
            redeemDaily()
            redeem7day()
            redeemMail()
            convertPO()
            roll10()
            yolorolls()
            bind_email()
            confirm_email(mail)
            salt = salt + 1

    except KeyboardInterrupt:
        print('dagnab')
