import subprocess,sys, logging,re, asyncio
from json import loads
from time import sleep
from string import ascii_lowercase
from urllib.request import urlopen
from os import system, name
from threading import Thread

logging.basicConfig(level=logging.DEBUG, filename='.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.log(logging.INFO,msg='\n\t\t\t\t[NEW SESSION]\n')

try:
    import requests
    from cefpython3 import cefpython as cef
    from colorama import Cursor
except ImportError:
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    install('cefpython3')
    install('requests')
    install('colorama')
    import requests
    from cefpython3 import cefpython as cef
    from colorama import Cursor

CU=Cursor.UP()
CD=Cursor.DOWN()
CL=Cursor.BACK()
CR=Cursor.FORWARD()
def cls(): 
    if name=='posix':
        _ = system('clear') 
    else: 
        _ = system('cls') 

def refresh_settings():
    global settings
    try:
        settings = open('settings.txt', mode='r+',encoding='utf-8').read().split('\n')
        for i in range(len(settings)):
            settings[i]=settings[i].split(': ')
            if len(settings[i])==1:
                settings[i][0]=settings[i][0][:-1]
                settings[i].append(None)
        settings=dict(settings)
    except FileNotFoundError:
        open('settings.txt', mode='w+',encoding='utf-8')
        settings={}

refresh_settings()
if len(settings.items())>7:
    try:
        for network in ['facebook','instagram','linkedin']:
                if network in sys.argv:
                    settings[network]=1
                else:
                    settings[network]=0
    except IndexError:
        raise IndexError('\n::No social-network specified!')
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg in ['-H','-help','--help','help','--Help','-Help','-h']:         #add linkedin in help message
            print("""
            -A   --algorithm\t\tNyckel algorithm url.
            
            -CID --client_id\t\tClientID token for the algorithm. Can be found on \n\t\t\t\t\t\t\thttps://www.nyckel.com/console/functions/*Your_function_ID*/api.
                                \t                                                      ↑
            -CS  --client_secret\tClientSecret token for the algorithm. Can be found on─┘
            
            -PL  --positive_label\tName(s) of the output(s) of Your nyckel algorithm, that You define as positive.
            
            -L   --location\t\tLocation search query for Facebook and LinkedIn.
            -Q   --query\t\tSearch query.
            -Y   --year\t\tOnly the photos that were posted in or after the given year will be checked.
                 --limit\t\tThe maximum of photos that will be checked per profile. Set to 30 by default.
            
            facebook, instagram\t\tSearch for people in the specified social network.   
            
            
            The script is remembering settings that You have set, so You have to call one of the given below parameters only if You need to change it's value.
            If You haven't launched the script yet, or the settings file in the script directory doesn\'t exist, the first start up configuring procedure will be called.
            """)
            sys.exit()
        if arg in ['-A','--algorithm']:
            settings['algorithm']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-CID','--client_id']:
            settings['client_id']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-CS','--client_secret']:
            settings['client_secret']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-PL','--positive_label']:
            settings['positive_label']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-L','--location']:
            settings['location']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-Q','--query']:
            settings['query']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['-Y','--year']:
            settings['year']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
        elif arg in ['limit',]:
            settings['limit']=sys.argv[i+1] if not sys.argv[i+1].startswith('-') else ''
    file = open('settings.txt','w+',encoding='utf-8')
    write_buffer=[]
    for parameter, value in settings.items():
        if not parameter in[None,'']:
            write_buffer.append(f'{parameter}: {value}') if not value==None else file.write(f'{parameter}: ')
    write_buffer='\n'.join(write_buffer)
    file.write(write_buffer)
    file.close()
    del write_buffer
else:
    cls()
    print('::Looks like this is your first launch of the program.\n\t\t\t\tLet\'s set it up!')
    file = open('settings.txt','w+',encoding='utf-8')
    file.write('algorithm: '+input('::First of all, enter URL of the nyckel algorithm.\nThe link must be such:\n\thttps://www.nyckel.com/v1/functions/*algorithm token*/invoke\n\t\t\t\t>')+'\n')
    a='::Next, You need to enter Your ClientId and ClientSecret. You can find them on the API tab of Your function control panel web-page:'
    print(a)
    print('https://www.nyckel.com/console/functions/*Your function ID*/api'.rjust(len(a)-11))
    del a
    file.write('client_id: '+input(f'\tClientID:\n\tClientSecret:\t{CU}>')+'\n')
    file.write('client_secret: '+input('\tClientSecret:\t>'+CU+CL+' '+CD)+'\n')
    file.write('positive_label: '+input('::Okay, next. Enter the algorithm\'s output\'s name(s), that You will define as positive result:\n\t\t\t\t>')+'\n')
    file.write('location: '+input('::*Facebook and LinkedIn only*\n::What location should the algorithm search?\n\t\t\t\t>')+'\n')
    file.write('query: '+input('::*required field for Instagram*\n::Enter the search query:\t\t>')+'\n')
    file.write('year: '+input('::Photos that were posted not earlier than which year should be checked?\n\t\t>')+'\n')
    file.write('limit: 30\n')
    n=input('::What social network should it crawl?\n\t\t(facebook/instagram/linkedin):\t>')
    for network in ['facebook','instagram','linkedin']:
                if n in network:
                    file.write(f'{network}: 1\n')
                else:
                    file.write(f'{network}: 0\n')
    file.close()
    open('checked profiles.txt', 'w+', encoding='utf-8')
    open('result.txt', 'w+', encoding='utf-8')
    cls()
    refresh_settings()

del CD,CL,CR,CU,Cursor,file

sys.excepthook = cef.ExceptHook
cef.Initialize(settings={'cache_path':'./cache'})

js_scroll_to_bottom="""
console.log('scrolling...')
interval=setInterval(()=>{
if(!document.querySelector('div[role="feed"]>div>div>div>div>div>span[dir="auto"]'))
{window.scrollTo(0,document.body.scrollHeight);}
else{drive_data_to_python('scrolled_to_bottom');clearInterval(interval);console.log(true);}
},100)
"""
token=''
def process_with_nyckel(image):
    global token
    if not token:
        token = loads(requests.post('https://www.nyckel.com/connect/token',
                                data={
                                    'client_id':settings['client_id'],
                                    'client_secret':settings['client_secret'],
                                    'grant_type':'client_credentials',
                                }).text)['access_token']
    headers={'Authorization':'Bearer '+token}
    result = requests.post(settings['algorithm'], headers=headers, files={'data': image})
    return result
def check_image(imageUrl,profileUrl):
    global settings,process_with_nyckel
    result=process_with_nyckel(urlopen(imageUrl))
    drive_data_to_python(f'{result}\n{result.text}')
    if result.status_code<400 and loads(result.text)['labelName'] in settings['positive_label']:
        result_json=loads(result.text)
        open('result.txt','a+', encoding='utf-8').writelines([f'[{result_json["labelName"]} {result_json["confidence"]:.0%}]{profileUrl}\t\t│{imageUrl}\n',])

def click_on_element(x,y):
    browser.SendMouseMoveEvent(int(x), int(y), False, 0)
    browser.SendMouseClickEvent(int(x),int(y),cef.MOUSEBUTTON_LEFT,False,1)
    browser.SendMouseClickEvent(int(x),int(y),cef.MOUSEBUTTON_LEFT,True,1)
def type_string_with_keyboard(string):
        for character in string:
            print(character+' : '+str(ord(character)))
            browser.SendKeyEvent({'type': 3, 'windows_key_code': ord(character), 'character':ord(character),})
def LSD(x:list):                                                    #LSD stands for LoadingStateDecorator
    def check_loading_state(browser,is_loading,*args,**kwargs):
        if is_loading and not x:
            x.append(True)
        else: x.clear()
    return check_loading_state
def drive_data_to_python(drivenData):
    print(drivenData)
    global data
    data=drivenData
def input_from_terminal(prompt=''):
    input_value=input(prompt)
    browser.ExecuteJavascript(f'var py_out={input_value}')
def check_date(date_str):
    year = re.search(r'20\d\d',date_str)
    if year:
        year=int(year.group(0))
    if (year and year>=int(settings['year']))or not year:
        browser.ExecuteJavascript('var date=true')
        return True
    else:
        browser.ExecuteJavascript('var date=false')
        return False
def async_input(prompt:str):
    global async_input_value
    return input(prompt)
if int(settings['instagram']) and not settings['query']:
    raise KeyError('Cannot crawl through Instagram without query parameter')

browser = cef.CreateBrowserSync()
isLoading=[]
browser.SetClientCallback('OnLoadingStateChange',LSD(isLoading))

bindings=cef.JavascriptBindings()
bindings.SetFunction('drive_data_to_python', drive_data_to_python)
bindings.SetFunction('py_click',click_on_element)
bindings.SetFunction('py_type',type_string_with_keyboard)
bindings.SetFunction('check_image',check_image)
bindings.SetFunction('check_date',check_date)
bindings.SetFunction('py_input',input_from_terminal)
browser.SetJavascriptBindings(bindings)


data=False
def CLI_login(network):
    global browser, auth, isLoading
    sleep(7)
    if '/login/' in browser.GetUrl() and not isLoading:
        auth={
            'login':async_input(f"!!You need to log in to {network}!!\n::Enter Your {network} login:\t"),
            'password':async_input(f"::Enter Your {network} password:\t"),
        }
        browser.ExecuteJavascript(f"""
            input_fields=[]
            document.querySelectorAll('input:not([type="hidden"])').forEach(element=>input_fields.push(element.getBoundingClientRect()))
            lx=input_fields[0].x+input_fields[0].width/2
            ly=input_fields[0].y+input_fields[0].height/2
            px=input_fields[1].x+input_fields[1].width/2
            py=input_fields[1].y+input_fields[1].height/2
            py_click(lx,ly)
            py_type('{auth['login']}')
            py_click(px,py)
            py_type('{auth['password']}')
            setTimeout(()=>{{document.querySelector('button[type="submit"]').click()}},1321)
            """)
threads={}
for resource in ['facebook','instagram']:   #add linkedin
    if int(settings[resource]):
        url = 'https://'+resource+'.com/accounts/login/' if resource == 'instagram' else 'https://'+resource+'.com/login/'
        browser.LoadUrl(url)
        isLoading.append(True)
        threads[resource]=Thread(target=CLI_login,args=(resource,))
        threads[resource].start()
        while isLoading or 'login' in browser.GetUrl():
            cef.MessageLoopWork()


if int(settings['facebook']):
    profileUrls=[]
    url = 'https://www.facebook.com/search/people?q=a' if not settings['query'] else f'https://www.facebook.com/search/people?q={settings["query"]}'
    browser.LoadUrl(url)
    if settings['location']:
        isLoading.append(True)
        while isLoading:
            cef.MessageLoopWork()
        browser.ExecuteJavascript(f"""
            var a=document.querySelector('[aria-haspopup="listbox"][role="combobox"]');
            a.click()
            py_type('{settings["location"]}');
            drive_data_to_python('location_entered');
            """)
        while not data=='location_entered':
            cef.MessageLoopWork()
        browser.ExecuteJavascript(f"""
            setTimeout(()=>{{
                a=document.getElementsByClassName('ni8dbmo4 kwzhilbh cbu4d94t j83agx80')[0].getBoundingClientRect();
                py_click(a.x,a.y);
                setTimeout(drive_data_to_python,1000,'location_selected')
                }},1000)
            """)
        while not data=='location_selected':
            cef.MessageLoopWork()
    def collect_profiles():
        global profileUrls, data,browser
        browser.ExecuteJavascript(f"{js_scroll_to_bottom}")
        while not data=='scrolled_to_bottom':
            cef.MessageLoopWork()
        browser.ExecuteJavascript("""
        var py_data=[];
        document.querySelectorAll('span.nc684nl6>a[role="link"]').forEach(element=>py_data.push(element.href))
        drive_data_to_python(py_data)
        """)
        while not type(data)==list:
            cef.MessageLoopWork()
        profileUrls=list(set(profileUrls+data))
    def collect_images(profileUrl,b, isLoading):
        global process_with_nyckel, data
        if not profileUrl in open('checked profiles.txt','r',encoding='utf-8').readlines():
            if 'profile.php?id' in profileUrl:
                b.LoadUrl(profileUrl+'&sk=photos')
            else:
                b.LoadUrl(profileUrl+'/photos_by')
            isLoading.append(True)
            while isLoading:
                cef.MessageLoopWork()
            b.ExecuteJavascript(f"""
                gallery_tabs=document.querySelectorAll('div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')
                if(gallery_tabs.length>1){{
                    image_links=gallery_tabs[0].querySelectorAll('div[class="j83agx80 btwxx1t3 lhclo0ds"]>div[class="rq0escxv rj1gh0hx buofh1pr ni8dbmo4 stjgntxs l9j0dhe7"]>div>div>a')
                    var i = 0
                    py_data= new Array(image_links.length)
                    interval=setInterval(()=>{{
                        if((i<{settings['limit']})&&i<image_links.length){{
                            py_data[i]=image_links[i].href
                            i+=1
                        }}
                        else{{clearInterval(interval);drive_data_to_python(py_data)}}
                    }},0)
                }}
                else{{
                    interval=setInterval(()=>{{
                        image_links=gallery_tabs[0].querySelectorAll('div[class="j83agx80 btwxx1t3 lhclo0ds"]>div[class="rq0escxv rj1gh0hx buofh1pr ni8dbmo4 stjgntxs l9j0dhe7"]>div>div>a')
                        gallery_tabs=document.querySelectorAll('div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')
                        if(image_links.length<{settings['limit']}&&gallery_tabs.length<=1)
                            {{window.scrollTo(0,document.body.scrollHeight);}}
                        else{{
                            py_data=[]
                            image_links.forEach(element=>py_data.push(element.href))
                            drive_data_to_python(py_data)
                            }}
                    }},200)
                }}
                """)
            data=False
            while not type(data)==list:
                cef.MessageLoopWork()
            image_links=data
            for imageUrl in image_links:
                if 'https://www.facebook.com/photo.php?'in str(imageUrl):
                    browser.LoadUrl(imageUrl)
                    isLoading.append(True)
                    while isLoading:
                        cef.MessageLoopWork()
                    browser.ExecuteJavascript("""
                                            drive_data_to_python([document.querySelector('img[data-visualcompletion="media-vc-image"]').src,
                                            [...document.querySelectorAll('div[class="j83agx80 cbu4d94t ew0dbk1b irj2b8pg"]>div.qzhwtbm6.knvmm38d>span[dir="auto"]')].pop().innerText])""")
                    data=['false',]
                    while not type(data[1])==str and data[0]:
                        cef.MessageLoopWork()
                    if check_date(data[1]):
                        check_image(data[0],profileUrl)
                    elif not data[0]:
                        pass
                    else:
                        break
            open('checked profiles.txt','a+',encoding='utf-8').writelines([profileUrl,'\n'])
    if not settings['query']:
        url = browser.GetUrl()
        for letter in ascii_lowercase:
            url=re.sub(r'q=\w*&','q='+letter+'&',url)
            browser.LoadUrl(url)
            isLoading.append(True)
            while isLoading:
                cef.MessageLoopWork()
            collect_profiles()
            for profile in profileUrls:
                collect_images(profile,browser,isLoading)
    else:
        collect_profiles()
        for profile in profileUrls:
            collect_images(profile, browser, isLoading)


if int(settings['instagram']):
    browser.LoadUrl('https://instagram.com/')
    isLoading.append(True)
    while isLoading:
        cef.MessageLoopWork()
    browser.ExecuteJavascript(f"""
        a=document.querySelector('input[autocapitalize="none"][type="text"]').getBoundingClientRect()
        var x=a.x+a.width/2
        var y=a.y+a.height/2
        py_click(x,y)
        py_type('{settings['query']}')
        interval=setInterval(()=>{{if(!document.querySelector('div.lWmzy>div>svg.FSiF6'))
        {{clearInterval(interval);drive_data_to_python('query_entered')}}
        }},1000)
        """)
    while not data=='query_entered':
        cef.MessageLoopWork()
    browser.ExecuteJavascript(f"""
            var py_data=[]
            document.querySelectorAll('a[class="-qQT3"]').forEach(element=>py_data.push(element.href))
            drive_data_to_python(py_data)
        """)
    while type(data) is not list or not data:
        cef.MessageLoopWork()
    urls =data
    for url in urls:
        if '.com/explore/' not in url:
            browser.LoadUrl(url)
            isLoading.append(True)
            while isLoading:
                cef.MessageLoopWork()
            browser.ExecuteJavascript(f"""
                interval=setInterval(()=>{{
                    if(document.querySelectorAll('div.v1Nh3.kIKUG._bz0w>a').length<{settings['limit']}&&document.querySelector('div._4emnV')){{
                        window.scrollTo(0,document.body.scrollHeight)
                    }}
                    else{{
                        py_data=[]
                        document.querySelectorAll('div.v1Nh3.kIKUG._bz0w>a').forEach(element=>py_data.push(element.href))
                        clearInterval(interval)
                        drive_data_to_python(py_data)
                    }}
                    }},20)
                """)
            while 'https://www.instagram.com/p/' not in data[0]:
                cef.MessageLoopWork()
            posts=data
            for post in posts:
                browser.LoadUrl(post)
                isLoading.append(True)
                while isLoading:
                    cef.MessageLoopWork()
                
                browser.ExecuteJavascript("""drive_data_to_python(document.querySelector('a.c-Yi7>time._1o9PC.Nzb55').innerText)""")
                while not type(data) == str:
                    cef.MessageLoopWork()
                if check_date(data):
                    browser.ExecuteJavascript("""interval=setInterval(()=>{
                        button=document.querySelector('button._6CZji')
                        a= new Set()
                        if(button){
                            document.querySelectorAll('div.ZyFrc>div>div.KL4Bh>img').forEach(element=>a.add(element.src))
                            button.click()
                            }
                        else{
                            document.querySelectorAll('div.ZyFrc>div>div.KL4Bh>img').forEach(element=>a.add(element.src))
                            drive_data_to_python([...a])
                            clearInterval(interval)
                            }
                        },100)""")
                    try:
                        while not 'https://scontent-iev1-1.cdninstagram.com/v/' in data[0]:
                            cef.MessageLoopWork()
                        for image in data:
                            check_image(image,url)
                    except IndexError:
                        pass
            open('checked profiles.txt','a+',encoding='utf-8').writelines([url,'\n'])