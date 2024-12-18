import pygame,math,random,datetime,time,json,copy,os
from matplotlib import pyplot as plt
import numpy as np
from UIpygame import PyUI as PyUI
pygame.init()
screen = pygame.display.set_mode((1200, 630),pygame.RESIZABLE)
ui = PyUI.UI()
pygame.display.set_caption('Spotify Data')
done = False
clock = pygame.time.Clock()
ui.styleload_green()
ui.styleset(scalesize=False)

months_of_the_year = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']

def timetodate(time,display=False):
    st = str(datetime.datetime.fromtimestamp(time))
    if display:
        st = st.replace('-','/')
        lis = st.split()[0].split('/')
        return f'{lis[2]}/{lis[1]}/{lis[0]}'
    else:
        return st.rsplit(':',1)[0]

def datetotime(date):
    split = date.split()
    for a in '/-:.,':
        split[0] = split[0].replace(a,'-')
        
    year,month,day = split[0].split('-')
    dat = datetime.date(int(year),int(month),int(day))
    if len(split)>1:
        for a in '/-:.,':
            split[1] = split[1].replace(a,':')
        hour,minute = split[1].split(':')
        tim = datetime.time(int(hour),int(minute))
    else:
        tim = datetime.time(0,0)
    dat = datetime.datetime.combine(dat,tim)
    return dat.timestamp()
def datetoweekday(date):
    split = date.split()
    for a in '/-:.,':
        split[0] = split[0].replace(a,'-')
        
    year,month,day = split[0].split('-')
    dat = datetime.date(int(year),int(month),int(day))
    return dat.weekday()

def mstostr(ms):
    sec = ms/1000
    h = int(sec//3600)
    m = str(int(sec%3600//60))
    s = str(int(sec%60))
    ms = sec%1
    if len(s) == 1: s = '0'+s
    if h == 0:
        return f'{m}m {s}s'
    else:
        return f'{h}h {m}m {s}s'
    
def makedummy():
    music = [['Get the "StreamingHistory.json" files in the same folder as this one','U didnt do the files right'],['The "StreamingHistoryfake.json" that is','Delete the file when u have fixed it']]
    song = random.choice(music)
    
    return {"endTime" : timetodate(random.choice([time.time(),time.time()-69*30*24*60*60])),
            "artistName" : song[0],
            "trackName" : song[1],
            "msPlayed" : random.randint(20,240000)
        }

def dummyjson(size=20000):
    data = []
    for a in range(size):
        data.append(makedummy())
    with open('StreamingHistoryfake.json','w') as f:
        json.dump(data,f)
    return data

def intotextfile(data):
    with open('alldata.txt','w') as f:
        for a in data:
            try:
                f.writelines(f'artist:{a["artistName"]} track:{a["trackName"]} time:{mstostr(a["msPlayed"])} endTime:{a["endTime"]}\n')
            except:
                f.writelines(f'Unkown_Song time:{mstostr(a["msPlayed"])} endTime:{a["endTime"]}\n')

def converttofulldata(data,no_username='Unknown User'):
    ndata = []
    for d in data:
        if "ts" in d: # check if full data rather than year data
            ndata.append(d)
            ndata[-1]['endTime'] = d['ts'].replace('T',' ').rsplit(':',1)[0]
            ndata[-1]['msPlayed'] = d['ms_played']
            ndata[-1]['artistName'] = d['master_metadata_album_artist_name']
            ndata[-1]['trackName'] = d['master_metadata_track_name']
            if 'username' in ndata[-1]:
                ndata[-1]['username'] = ndata[-1]['username'].replace("58zgbg1s1y50n9szffm1llhqu",'Christian')
            else:
                ndata[-1]['username'] = no_username
            ndata[-1]['album'] = ndata[-1]["master_metadata_album_album_name"]
        else:
            ndata.append({"ts":d['endTime'].replace(' ','T')+':00Z',
                          "username":"unknown","platform":"unknown",
                          "ms_played":d['msPlayed'],"conn_country":"GB",
                          "ip_addr_decrypted":"unknown","user_agent_decrypted":"unknown",
                          "master_metadata_track_name":d['trackName'],
                          "master_metadata_album_artist_name":d['artistName'],
                          "master_metadata_album_album_name":"unknown",
                          "spotify_track_uri":"unknown","episode_name":None,
                          "episode_show_name":None,"spotify_episode_uri":None,
                          "reason_start":"unknown","reason_end":"unknown",
                          "shuffle":-1,"skipped":-1,"offline":-1,
                          "offline_timestamp":0,"incognito_mode":-1,
                          'endTime':d['endTime'],'msPlayed':d['msPlayed'],
                          'artistName':d['artistName'],'trackName':d['trackName'],
                          'album':'unknown'})
        if ndata[-1]['artistName'] == None: ndata[-1]['artistName'] = 'None'
        if ndata[-1]['trackName'] == None: ndata[-1]['trackName'] = 'None'
        if ndata[-1]['album'] == None: ndata[-1]['album'] = 'None'
    intotextfile(ndata)
    return ndata

def count_streaminghistory_files(path):
    filesyear = [PyUI.resourcepath(os.path.join(path,f)) for f in os.listdir(PyUI.resourcepath(path)) if (('StreamingHistory' in f) and f[len(f)-5:]=='.json')]
    filesall = [PyUI.resourcepath(os.path.join(path,f)) for f in os.listdir(PyUI.resourcepath(path)) if (('Streaming_History' in f) and f[len(f)-5:]=='.json')]
    return len(filesyear+filesall)

def loadjson(path='',no_username='Unknown User'):
    data = []
    filesyear = [PyUI.resourcepath(os.path.join(path,f)) for f in os.listdir(PyUI.resourcepath(path)) if (('StreamingHistory' in f) and f[len(f)-5:]=='.json')]
    filesall = [PyUI.resourcepath(os.path.join(path,f)) for f in os.listdir(PyUI.resourcepath(path)) if (('Streaming_History' in f) and f[len(f)-5:]=='.json')]
    print(filesall)
    files = []
    if len(filesyear) == 0: files = filesall
    elif len(filesall) == 0: files = filesyear
    else: files = filesall
    
    for a in files:
        with open(a,'r',encoding='utf8') as f:
            data += json.load(f)
##    if len(data) == 0:
##        data = dummyjson(420)
    return converttofulldata(data, no_username)
    
class Plot:
    def __init__(self):
        pass
    def plot(data,songs,start,end,samplerate,samplesize):
        pointspertime = round(samplesize/samplerate)
        data.sort(key = lambda x: datetotime(x['endTime']))
        for song in songs:
            print(song)
            s = song[0]
            artistmode = song[1]
            albummode = song[2]
            everything = song[3]
            graph = []
            samples = [0]
            t = start-samplesize
            index = 0
            while datetotime(data[index]['endTime'])<t:
                index+=1
            while t<end and index+1<len(data):
                a = data[index]
                index+=1
                if (not(artistmode or albummode or everything) and (a['trackName'],a['artistName'],a['username']) == (s[0],s[1],s[3])) or (artistmode and (a['artistName'],a['username']) == (s[1],s[3])) or (albummode and (a['album'],a['username']) == (s[2],s[3])) or (everything and (a['username'] == s[3])): #(not artistmode and (a['trackName'],a['artistName'],a['album'],a['username']) == s) or (artistmode and (a['artistName'],a['username']) == (s[1],s[2])) or (everything and a['username'] == s[2]):
                    while datetotime(a['endTime'])>t+samplerate:
                        if t>start: graph.append([datetime.datetime.fromtimestamp(t),sum(samples[-pointspertime:])])
                        samples.append(0)
                        t+=samplerate
                    samples[-1]+=a['msPlayed']/(1000*60*60)
            while t<end:
                graph.append([datetime.datetime.fromtimestamp(t),sum(samples[-pointspertime:])])
                samples.append(0)
                t+=samplerate
                    
            plt.xticks(rotation=30)

            while len(graph)>4 and graph[4][1] == 0:
                del graph[0]
                    
            
            if not everything or len(songs)!=1:
                if everything: name = f'Everything ({s[3]})'
                elif artistmode: name = f'{s[1]} ({s[3]})'
                elif albummode: name = f'{s[2]} - {s[1]} ({s[3]})'
                else: name = f'{s[0]} - {s[1]} ({s[3]})'
                plt.plot(np.array([x[0] for x in graph]),np.array([x[1] for x in graph]),label=name)
            else:
                plt.plot(np.array([x[0] for x in graph]),np.array([x[1] for x in graph]))
        plt.xlabel('Dates')
        plt.ylabel(f'Listen Time Over {round(samplesize/60/60/24)} Days in Hours')
        everything = True
        albummode = True
        artistmode = True
        for s in songs:
            artistmode = (artistmode and s[1])
            albummode = (albummode and s[2])
            everything = (everything and s[3])

        if len(songs) == 1:
            if everything: plt.title(f'All Music ({songs[0][0][3]})')
            elif artistmode: plt.title(f'{songs[0][0][1]}')
            elif albummode: plt.title(f'{songs[0][0][2]}-{songs[0][0][1]}')
            else: plt.title(f'{songs[0][0][0]}-{songs[0][0][1]}')
        else:
            if everything: plt.title('All Music')
            elif artistmode: plt.title('Artists')
            elif albummode: plt.title('Albums')
            else: plt.title('Songs')
            leg = plt.legend(loc='upper left')
        plt.show()
    def plotsummed(summeddata):
        plt.yscale('symlog')
        plt.plot(np.array([a['Playtime']/1000/60 for a in summeddata]))
        plt.show()
    def plotday(data,songs,start,end,typ):
        data.sort(key = lambda x: datetotime(x['endTime']))
        if typ == 'week':
            xaxis = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        elif typ == 'day':
            xaxis = [str(a+1)+'am' for a in range(12)]+[str(a+1)+'pm' for a in range(12)]
        elif typ == 'month':
            wordends = ['st','nd','rd']+['th' for a in range(17)]+['st','nd','rd']+['th' for a in range(7)]+['st']
            xaxis = [str(a+1)+wordends[a] for a in range(31)]
        elif typ == 'year':
            xaxis = months_of_the_year
            
        for song in songs:
            s = song[0]
            artistmode = song[1]
            everything = song[2]
            bars = [0 for a in range(len(xaxis))]
            for a in data:
                if (not artistmode and (a['trackName'],a['artistName'],a['username']) == s) or (artistmode and (a['artistName'],a['username']) == (s[1],s[2])) or (everything and a['username'] == s[2]):
                    t = a['msPlayed']/1000/60/60
                    if typ == 'week': bars[datetoweekday(a['endTime'])]+=t
                    elif typ == 'day': bars[int(a['endTime'].split()[1].split(':')[0])]+=t
                    elif typ == 'month': bars[int(a['endTime'].split()[0].split('-')[2])-1]+=t
                    elif typ == 'year': bars[int(a['endTime'].split()[0].split('-')[1])-1]+=t
            if not everything:
                if artistmode: name = f'{s[1]}'
                else: name = f'{s[0]} - {s[1]}'
                plt.bar(xaxis,bars,label=name)
            else: plt.bar(xaxis,bars)
        plt.ylabel(f'Total Listen Time in Hours')
        if typ == 'week': plt.xticks(rotation=18)
        else: plt.xticks(rotation=45)
        if not everything:
            leg = plt.legend(loc='upper left')
        plt.show()

        

        
        

        
                        




class Main:
    def __init__(self):
        self.data_paths = []
        self.make_init_page()
    def make_init_page(self):
        # Init page
        ui.maketext(0,70,'Select a file to get data',70,anchor=('w/2',0),center=True)
        
        data = []#['Current Path',count_streaminghistory_files(''),ui.makebutton(0,0,'Select',30,toggleable=True,ID='path_select_button_1')]]
        for index,fil in enumerate(['.']+next(os.walk('.'))[1]):
            func = PyUI.funcer(self.set_selected_path,path=fil)
            if index == 0: name = 'Current Path'
            else: name = f'/{fil}'
            data.append([name,count_streaminghistory_files(fil),ui.makebutton(0,0,'Select',30,command=func.func,toggleable=True,ID=f'path_select_button_{len(data)+1}')])

##        ui.IDs['path_select_button_1'].press()
##        bindtoggles = [f'path_select_button_{n+1}' for n in range(len(data))]
##        for row in data:
##            row[2].bindtoggle = bindtoggles
            
        
        ui.makescrollertable(0,180,data,['File Path','Detected Files',''],anchor=('w/2',0),objanchor=('w/2',0),width='w*0.6',verticalspacing=4)

        ui.makebutton(0,130,'GO',60,self.init_data,anchor=('w/2',0),center=True)

    def set_selected_path(self,path):
        if path in self.data_paths:
            self.data_paths.remove(path)
        else:
            self.data_paths.append(path)
        
    def init_data(self):
        self.data = []
        for path in self.data_paths:
            self.data+=loadjson(path,path.split()[0])

        self.number_users = len(self.data_paths)
        # if self.number_users == 2:
        #     self.calculate_overlap(False, False)

        self.firstsong = time.time()
        self.lastsong = 0
        self.storedsel = []
        ui.searchresultsnum = len(self.data)
        for a in self.data:
            t = datetotime(a['endTime'])
            if t<self.firstsong: self.firstsong = t-10
            if t>self.lastsong: self.lastsong = t+10
        self.daterange = [self.firstsong,self.lastsong]

        self.years = [a+1 for a in range(int(timetodate(self.firstsong).split('-')[0])-1,int(timetodate(self.lastsong).split('-')[0]))]
        self.months = months_of_the_year

        self.sumdata(False,False,False,False,True)

        self.make_gui()
        self.refreshtopcharts()

        ui.movemenu('start','up',backchainadd=False)
        

    def make_gui(self):
        compare = self.number_users > 1
        compare_string = compare*'-133'

        # Start page
        ui.maketext(0,-200,'Spotify Stats',100,anchor=('w/2','h/2'),center=True,scalesize=True,menu='start')
        ui.makebutton(0,-100,'Song Table',50,lambda: ui.movemenu('tablepage','up'),anchor=('w/2','h/2'),center=True,scalesize=True,menu='start')

        # Start page date system

        ui.maketable(-110,-50,[],[ui.maketext(0,0,'Top Artists',40,backingcol=(87, 132, 86),textcenter=True)],verticalspacing=5,textsize=30,textcenter=False,anchor=('w/2','h/2'),objanchor=('w',0),ID='top artists',width=300,boxheight=[60,-1],height=300,scalesize=True,menu='start')
        ui.maketable(110,-50,[],[ui.maketext(0,0,'Top Songs',40,backingcol=(87, 132, 86),textcenter=True)],verticalspacing=3,textsize=30,textcenter=False,anchor=('w/2','h/2'),ID='top songs',width=300,boxheight=[60,-1],height=300,scalesize=True,menu='start')
        ui.maketext(0,-45,'',40,anchor=('w/2','h/2'),textcenter=True,center=True,centery=False,maxwidth=300,scalesize=True,ID='top text',menu='start')

        ui.makebutton(-20,36,'Back',35,ui.menuback,'tablepage',anchor=('w',0),objanchor=('w','h/2'))
        
        # Search Bar
        self.mainsearchbar = ui.makesearchbar(20,36,width='w/2-20'+compare_string,objanchor=(0,'h/2'),textsize=35,command=self.search,menu='tablepage')
        
        # Date system
        ui.maketext(20,36,'',35,ID='datedisplay',anchor=('w/2'+compare_string,0),objanchor=(0,'h/2'),menu='tablepage')
        self.setdatetext(False)
        # Date menu
        window = ui.makewindow(0,20,327,435,objanchor=('w/2',0),anchor=('w/2',0),menu='tablepage',ID='datewindow',bounditems=[
            
            ui.maketext(0,5,'Start Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,35,[x+1 for x in range(31)],command=self.setdatetext,pageheight=220,ID='dropdownstartday',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[0])-1),
            ui.makedropdown(80,35,self.months,command=self.setdatetext,pageheight=220,ID='dropdownstartmonth',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[1])-1),
            ui.makedropdown(233,35,self.years,command=self.setdatetext,pageheight=220,ID='dropdownstartyear',layer=2),

            ui.maketext(0,70,'End Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,105,[x+1 for x in range(31)],command=self.setdatetext,pageheight=150,ID='dropdownendday',startoptionindex=int(timetodate(self.lastsong,True).split('/')[0])-1),
            ui.makedropdown(80,105,self.months,command=self.setdatetext,pageheight=150,ID='dropdownendmonth',startoptionindex=int(timetodate(self.lastsong,True).split('/')[1])-1),
            ui.makedropdown(233,105,self.years,command=self.setdatetext,pageheight=150,ID='dropdownendyear',startoptionindex=-1),

            ui.makeslider(100,165,140,15,100,boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(-10,0,'Results',objanchor=('w','h/2'),anchor=(0,'h/2'))],increment=1,ID='searchresultsnum',startp=30,layer=0),
            ui.makeslider(100,205,140,15,"ui.searchresultsnum-min(ui.searchresultsnum,100)",boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(-20,0,'Start',objanchor=('w','h/2'),anchor=(0,'h/2'))],increment=1,ID='searchstartnum',startp=0,layer=0),

            ui.makelabeledcheckbox(75,235,'Artist Mode',35,textpos='right',toggle=False,ID='artistmode',layer=0,command=lambda: self.bindtoggle(['albummode','combineall'])),
            ui.makelabeledcheckbox(75,275,'Album Mode',35,textpos='right',toggle=False,ID='albummode',layer=0,command=lambda: self.bindtoggle(['artistmode','combineall'])),
            ui.makelabeledcheckbox(75,315,'Combine All',35,textpos='right',toggle=False,ID='combineall',layer=0,command=lambda: self.bindtoggle(['artistmode','albummode'])),

            ui.makebutton(0,350,'Sort By: Listens',30,objanchor=('w/2',0),anchor=('w/2',0),toggleable=True,togglecol=0,toggletext='Sort By: Time',ID='sortbylistens'),
            
            ui.makebutton(0,-10,'Apply',32,self.search,objanchor=('w/2','h'),anchor=('w/2','h'),layer=0)
        ])
        ui.makebutton(40,36,'Edit',35,anchor=('w/2+ui.IDs["datedisplay"].width'+compare_string,0),objanchor=(0,'h/2'),command=self.openeditmenu,menu='tablepage')

        # Main table
        self.maintable = ui.makescrollertable(20,72,[],[],textsize=25,boxheight=[40,-1],boxwidth=[50,-1,-1,-1,-1,-1,80],width='w-40',pageheight='h-92',scalesize=False,guessheight=36,menu='tablepage',ID='main_data_table')
        self.refreshfiltered()

        # Graph table
        ui.makebutton(115,36,'Graph',35,self.opengraphmenu,anchor=('w/2+ui.IDs["datedisplay"].width'+compare_string,0),objanchor=(0,'h/2'),menu='tablepage')
        window = ui.makewindow(0,20,327,260,objanchor=('w/2',0),anchor=('w/2',0),menu='tablepage',ID='graphwindow',bounditems=[
            ui.makeslider(20,95,220,15,365,minp=1/24,boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(20,-10,'Time(days)',objanchor=('w/2','h'),anchor=('w/2',0))],increment=1/24,ID='graph time',startp=30,layer=0),
            ui.makeslider(20,165,220,15,100,minp=1,boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(20,-10,'Points per Time',objanchor=('w/2','h'),anchor=('w/2',0))],increment=1,ID='graph PpT',startp=30,layer=0),

            ui.makedropdown(0,15,['Normal','Day','Week','Month','Year'],30,objanchor=('w/2',0),anchor=('w/2',0),layer=1,ID='graph type'),
            ui.makebutton(0,180,'Clear',32,command=self.clearselected,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makebutton(0,-10,'Create',32,command=self.generategraph,objanchor=('w/2','h'),anchor=('w/2','h'),layer=0),
            ])

        # Compare Menu
        if compare:
            ui.makebutton(215, 36, 'Compare', 35, self.opencomparemenu, anchor=('w/2+ui.IDs["datedisplay"].width'+compare_string, 0),objanchor=(0, 'h/2'), menu='tablepage')
            ui.makewindowedmenu(0,20,1000,'h-40','comparemenu','tablepage',objanchor=('w/2',0),anchor=('w/2',0),ID='comparewindow',bounditems=[
                          ui.makescrollertable(10,10,['no'],['title'],width=980,pageheight='h-20',ID='comparetable',guessheight=36,scalesize=False)])
    def search(self):
        ui.IDs['datewindow'].shut()
        self.sumdata()
        search = self.mainsearchbar.text
        artist,track,album = '','',''
        if ':' in search:
            split = search.split(':')
            searchtype = split[0].lower().strip()
            if searchtype == 'album':
                album = split[1]
            elif searchtype in ['track','song']:
                track = split[1]
            elif searchtype == 'artist':
                artist = split[1]   
        else:
            artist = search
            track = search
            album = search
        self.refreshtopcharts()
        self.refreshfiltered(artist,track,album)
        
    def refreshfiltered(self,artist='',track='',album=''):
        cutoff = copy.copy(ui.IDs['searchresultsnum'].slider)
        startp = copy.copy(ui.IDs['searchstartnum'].slider)
        if 'artistmode' in ui.IDs: artistmode,albummode,everything = ui.IDs['artistmode'].toggle,ui.IDs['albummode'].toggle,ui.IDs['combineall'].toggle
        else: artistmode,albummode,everything = False,False,False
            
        ndata = []
        for i,a in enumerate(self.summeddata):
            if artist+track+album == '' or ((a['Artist']!=None and artist!='' and artist.lower() in a['Artist'].lower()) or (a['Track']!=None and track!='' and track.lower() in a['Track'].lower())) or (a['Album']!='unknown' and album!='' and album.lower() in a['Album'].lower()):
                ndata.append([a,i])
        ui.searchresultsnum = len(ndata)
        ui.IDs['searchresultsnum'].refresh()
        ui.IDs['searchstartnum'].refresh()
        
        if startp+cutoff>len(ndata):
            startp = max(0,len(ndata)-cutoff)
        ndata = ndata[startp:startp+cutoff]
        tabledata = []
        for a,i in ndata:
            func = PyUI.funcer(self.updateselected,song=[(a['Track'],a['Artist'],a['Album'],a['Listener']),artistmode,albummode,everything])
            tabledata.append([ui.maketext(-100,0,str(i+1),textcenter=True,col=self.maintable.col),a['Track'],a['Artist'],
                              a['Album'],a['Listener'],ui.maketext(-100,0,str(a['Listens']),textcenter=True,col=self.maintable.col),
                              mstostr(a['Playtime']),ui.makebutton(-50,0,'{dots}',toggleable=True,ID=f'{a["Track"]},{a["Artist"]}',command=func.func)])
            if everything:
                del tabledata[-1][3]
                del tabledata[-1][2]
                del tabledata[-1][1]
            elif artistmode:
                del tabledata[-1][3]
                del tabledata[-1][1]
            elif albummode:
                del tabledata[-1][3]
                del tabledata[-1][1]
                tabledata[-1].insert(1,a['Album'])
            tabledata[-1][-1].song = (a['Track'],a['Artist'],a['Album'])
            if [(a['Track'],a['Artist'],a['Album']),artistmode,albummode,everything] in self.storedsel:
                tabledata[-1][-1].toggle = False
        self.maintable.startboxwidth = [50,-1,-1,-1,-1,-1,-1,80]
        titles = ['','Track','Artist','Album','Listener','Listens','Total Playtime','']
        if albummode:
            self.maintable.startboxwidth = [50,-1,-1,-1,-1,-1,80]
            titles = ['','Album','Artist','Listener','Listens','Total Playtime','']
        if artistmode:
            self.maintable.startboxwidth = [50,-1,-1,-1,-1,80]
            titles = ['','Artist','Listener','Listens','Total Playtime','']
        if everything:
            self.maintable.startboxwidth = [50,-1,-1,-1,80]
            titles = ['','Listener','Listens','Total Playtime','']
        self.maintable.titles = [ui.maketext(0,-100,a,30,textcenter=True) for a in titles]
        self.maintable.data = tabledata

        self.maintable.threadrefresh()

    def refreshtopcharts(self):
        topartists = [[a["Artist"]] for a in self.sumdata(True,True,False,False)[:5]]
        topsongs = [[a["Track"]+'\n{"'+a["Artist"]+'" col=(190,200,160) scale=0.8}'] for a in self.sumdata(True,False,False,False)[:5]]
        ui.IDs['top artists'].data = topartists
        ui.IDs['top artists'].refresh()
        ui.IDs['top songs'].data = topsongs
        ui.IDs['top songs'].refresh()
        t0 = self.sumdata(True,False,False,True)
        if t0 == []: t0 = {'Listens':0,'Playtime':0}
        else: t0 = t0[0]
        days = ((self.daterange[1]-self.daterange[0])/60/60/24)
        
        total = [str(t0['Listens']),mstostr(t0['Playtime']),str(round(days/30))+' Months',
                 mstostr((t0['Playtime'])/days)]
        if days<30: total[2] = str(round(days))+' Days'
        for i in range(len(total)):
            total[i] = '{"'+total[i]+'" col=(170,190,150)}'
        txt = f'Data Over\n{total[2]}\nTotal Listens\n{total[0]}\nListen Time\n{total[1]}\nTime Per day\n{total[3]}'
        ui.IDs['top text'].settext(txt)
        
        
        
    def sumdata(self,retur=False,artistmode=-1,albummode=-1,everything=-1,sortbylistens=-1):
        starttime = self.daterange[0]
        endtime = self.daterange[1]
        if artistmode == -1:
            artistmode = ui.IDs['artistmode'].toggle
        if albummode == -1:
            albummode = ui.IDs['albummode'].toggle
        if everything == -1:
            everything = ui.IDs['combineall'].toggle
        if sortbylistens == -1:
            sortbylistens = ui.IDs['sortbylistens'].toggle
            
        self.summeddatadict = {}

        for a in self.data:
            if datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                key = (a['trackName'],a['artistName'],a['username'])
                if artistmode: key = (a['artistName'],a['username'])
                if albummode: key = (a['album'],a['username'])
                if everything: key = (a['username'],)
                if not(key in self.summeddatadict):
                    self.summeddatadict[key] = {"Artist":a['artistName'],"Track":a['trackName'],"Listens":0,"Playtime":a['msPlayed'],'Listener':a['username'],'Album':a['album']}
                else:
                    self.summeddatadict[key]['Playtime']+=a['msPlayed']
                if self.summeddatadict[key]['Playtime']>30000:
                    self.summeddatadict[key]['Listens']+=1

        lis = list(self.summeddatadict.values())
        if sortbylistens: lis.sort(key=lambda x: (x["Listens"]*1000000+x['Playtime']/100000),reverse=True)
        else: lis.sort(key=lambda x: (x["Listens"]/1000000+x['Playtime']*100000),reverse=True)
            
        if not retur: self.summeddata = lis
        else: return lis

    def calculate_overlap(self,artistmode,albummode,compare_size=2):
        summeddata = self.sumdata(True, artistmode, albummode, False, True)
        collecting = []
        overlap = []
        if artistmode: matcher = ['Artist']
        elif albummode: matcher = ['Album']
        else: matcher = ['Artist','Track']

        user_listen_data = {}

        # Calculate all overlaps in music and add it to overlap list
        for song in summeddata:
            if song['Listener'] not in user_listen_data:
                user_listen_data[song['Listener']] = {'Listen_Time':song['Playtime'],'Listens':song['Listens']}
            else:
                user_listen_data[song['Listener']]['Listen_Time'] += song['Playtime']
                user_listen_data[song['Listener']]['Listens'] += song['Listens']

            match_found = False
            for found in collecting:
                matches = True
                for m in matcher:
                    if song[m] != found[m]:
                        matches = False
                        break
                if matches:
                    match_found = True
                    found['Listens'][song['Listener']] = song['Listens']
                    found['Playtime'][song['Listener']] = song['Playtime']
                    if len(found['Listens']) == compare_size:
                        overlap.append(found)
            if not match_found:
                collecting.append({'Artist':song['Artist'],
                                'Track':song['Track'],
                                'Album':song['Album'],
                                'Listens':{song['Listener']:song['Listens']},
                                'Playtime':{song['Listener']:song['Playtime']}})

        for song in overlap:
            for user in song['Playtime']:
                song['Playtime'][user]/=user_listen_data[user]['Listen_Time']
        # Sort and return the overlap
        def sort_key(song):
            val = 1
            for user in song['Playtime']:
                val*=song['Playtime'][user]
            song['Match_Value'] = val
            return val
        overlap.sort(key=sort_key, reverse=True)
        return overlap

    def load_compare_table(self):
        artistmode = ui.IDs['artistmode'].toggle
        albummode = ui.IDs['albummode'].toggle
        overlap = self.calculate_overlap(artistmode, albummode, self.number_users)
        matchsize_accounter = overlap[0]['Match_Value']

        sortbylistens = ui.IDs['sortbylistens'].toggle
        items_in_table = ui.IDs['searchresultsnum'].slider
        start_index = min(ui.IDs['searchstartnum'].slider,len(overlap)-items_in_table)

        # Ensure only one of songmde, albummode and artistmode are True
        songmode = False
        if artistmode: albummode = False
        elif not albummode: songmode = True

        # Create table
        titles = ['']+['Track','Artist','Album']*songmode+['Album','Artist']*albummode+['Artist']*artistmode+['Listens Match']
        boxwidth = [50]+[200]*(len(titles)-2)+[-1]
        slider_width = ui.IDs['comparetable'].width-50-200*(len(titles)-2)-15
        data = []
        for i,song in enumerate(overlap[start_index:start_index+items_in_table]):
            new_line = [ui.maketext(-100,0,str(i+start_index+1),textcenter=True,col=self.maintable.col)]
            new_line+= [song['Track'],song['Artist'],song['Album']]*songmode
            new_line+= [song['Album'], song['Artist']] * albummode
            new_line+= [song['Artist']]*artistmode
            st = ', '.join([f'{song["Listens"][user]}' for user in song['Listens']])
            new_line+= [ui.makeslider(0, 0, slider_width, 30, startp=song['Match_Value']/matchsize_accounter, maxp=1,
                                      movetoclick=False, roundedcorners=0,
                      button=ui.makebutton(0, 0, '', width=0, height=0, borderdraw=False, backingdraw=False,
                                           clickableborder=0),
                                      bounditems=[ui.maketext(-5,0,st,anchor=('w','h/2'),textcol=PyUI.shiftcolor_rgb(PyUI.Style.defaults['textcol'],-30),objanchor=('w','h/2'),backingcol=(107,132,106),backingdraw=False)])]
            data.append(new_line)

        ui.IDs['comparetable'].wipe()
        ui.IDs['comparetable'].startboxwidth = boxwidth
        ui.IDs['comparetable'].titles = [ui.maketext(0,-100,a,30,textcenter=True) for a in titles]
        ui.IDs['comparetable'].data = data
        ui.IDs['comparetable'].threadrefresh()


    def countsong(self,info,starttime,endtime,num=True):
        count = 0
        playtime = 0
        for a in self.data:
            if (a['trackName'],a['artistName']) == info and datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                count+=1
                playtime+=a['msPlayed']
        if num: return count
        return playtime

    def bindtoggle(self,bindings):
        for b in bindings:
            ui.IDs[b].toggle = False
    def setdatetext(self,pull=True):
        if pull:
            self.ui = ui
            self.daterange = [datetotime(f"{ui.IDs['dropdownstartyear'].active}-{self.months.index(self.ui.IDs['dropdownstartmonth'].active)+1}-{ui.IDs['dropdownstartday'].active}"),
                              datetotime(f"{ui.IDs['dropdownendyear'].active}-{self.months.index(self.ui.IDs['dropdownendmonth'].active)+1}-{ui.IDs['dropdownendday'].active}")]
        ui.IDs['datedisplay'].settext(timetodate(self.daterange[0],True)+' {arrow stick=0.5 scale=0.75} '+timetodate(self.daterange[1],True))
    def opengraphmenu(self):
        ui.IDs['datewindow'].shut()
        ui.IDs['graphwindow'].open()
    def openeditmenu(self):
        ui.IDs['graphwindow'].shut()
        ui.IDs['datewindow'].open()
    def opencomparemenu(self):
        ui.IDs['graphwindow'].shut()
        ui.IDs['datewindow'].shut()
        self.load_compare_table()
        ui.movemenu('comparemenu','down')
    def clearselected(self):
        self.storedsel = []
        for a in self.maintable.table:
            if type(a[-1]) == PyUI.BUTTON:
                a[-1].toggle = True
    def updateselected(self,song):
        if song in self.storedsel:
            self.storedsel.remove(song)
        else:
            self.storedsel.append(song)
    def generategraph(self):
        typ = ui.IDs['graph type'].active.lower()
##        self.storeselected()
        if len(self.storedsel)>0:
            time = ui.IDs['graph time'].slider
            PpT = ui.IDs['graph PpT'].slider
            if typ == 'normal': Plot.plot(self.data,self.storedsel,self.daterange[0],self.daterange[1],(time/PpT)*24*60*60,time*24*60*60)
            else: Plot.plotday(self.data,self.storedsel,self.daterange[0],self.daterange[1],typ)
    def generatetimerankinggraph(self):
        Plot.plotsummed(self.summeddata)

main = Main()

while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if ui.activemenu == 'start':
                    ui = PyUI.UI()
                    ui.styleload_green()
                    ui.styleset(scalesize=False)
                    new_main = Main()
                    ui.movemenu('main', length=0, backchainadd=False)
                elif ui.activemenu == 'main':
                    done = True
                else:
                    ui.menuback()
    screen.fill(PyUI.Style.wallpapercol)
    ui.rendergui(screen)
    
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit()



















