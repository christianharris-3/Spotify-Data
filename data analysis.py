import pygame,math,random,datetime,time,json,copy,os
##import matplotlib.pyplot as plt, numpy as np
import PyUI as PyUI
pygame.init()
screen = pygame.display.set_mode((1200, 630),pygame.RESIZABLE)
ui = PyUI.UI()
done = False
clock = pygame.time.Clock()
ui.styleload_green()
ui.styleset(scalesize=False)

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

    music = [['Coldplay', 'Paradise'], ['Coldplay', 'Talk'], ['Coldplay', 'Viva La Vida'], ['Coldplay', 'Major Minus'], ['Coldplay', 'Charlie Brown'], ['Coldplay', 'Lovers in Japan'], ['Coldplay,Rihanna', 'Princess of China'], ['Coldplay', 'Low'], ['Coldplay', 'Speed of Sound'], ['Coldplay', 'A L I E N S'], ['Coldplay', 'Clocks'], ['Coldplay', 'Spies'], ['Coldplay', 'Trouble'], ['Wilbur Soot', 'Your Sister Was Right'], ['Lovejoy', 'One Day'], ['Lovejoy', 'The Fall'], ['Lovejoy', "It's All Futile! It's All Pointless!"], ['Lovejoy', 'Call Me What You Like'], ['Lovejoy', 'Portrait of a Blank Slate'], ['Alec Benjamin', 'Match In The Rain'], ['Alec Benjamin', 'Paper Crown'], ['Dream,Alec Benjamin', 'Change My Clothes'], ['Alec Benjamin', 'Older'], ['Alec Benjamin', "Devil Doesn't Bargain"], ['Imagine Dragons', 'Friction'], ['Imagine Dragons', 'Believer'], ['Imagine Dragons', 'Demons'], ['Imagine Dragons', 'Dream'], ['The Wombats', 'Greek Tragedy'], ['The Wombats', 'Our Perfect Disease'], ['The Wombats', 'Method to the Madness'], ['The Wombats', "If You Ever Leave, I'm Coming with You"], ['The Wombats', 'Ready for the High'], ['Muse', "Won't Stand Down"], ['Muse', 'Hysteria'], ['Muse', 'Undisclosed Desires'], ['Two Door Cinema Club', 'Are We Ready (Wreck)'], ['Two Door Cinema Club', 'Good Morning'], ['Two Door Cinema Club', 'Golden Veins'], ['Two Door Cinema Club', 'Sun'], ['Two Door Cinema Club', 'I Can Talk'], ['Two Door Cinema Club', 'Pyramid'], ['Two Door Cinema Club', 'Sleep Alone'], ['Panic! At The Disco', 'I Write Sins Not Tragedies'], ['Two Door Cinema Club', 'What You Know'], ['Panic! At The Disco', "Don't Threaten Me with a Good Time"], ['Panic! At The Disco', 'One of the Drunks'], ['Keane', 'Somewhere Only We Know'], ['OneRepublic', 'Run'], ['OneRepublic', 'Life In Color'], ['OneRepublic,Santigold', 'NbHD'], ['OneRepublic', 'Wherever I Go'], ['OneRepublic', 'If I Lose Myself'], ['OneRepublic', 'Love Runs Out'], ['OneRepublic', 'Counting Stars'], ['Of Monsters and Men', 'Dirty Paws'], ['Of Monsters and Men', 'Mountain Sound'], ['Of Monsters and Men', 'Empire'], ['Of Monsters and Men', 'Human'], ['Of Monsters and Men', 'Little Talks'], ['Of Monsters and Men', 'Wild Roses'], ['Of Monsters and Men', 'Wolves Without Teeth'], ['Bastille', 'Icarus'], ['Bastille', 'Pompeii'], ['Fall Out Boy', 'Centuries'], ['Fall Out Boy', 'Fourth Of July'], ['Bastille', 'Poet'], ['Metric', 'Breathing Underwater'], ['Fall Out Boy', 'Immortals'], ['Metric', 'Art of Doubt'], ['Metric', 'Gold Guns Girls'], ['Metric', 'Synthetica'], ['Metric', 'What Feels Like Eternity'], ['Bombay Bicycle Club', 'What If'], ['Farewell Fighter', 'Golden'], ['Jeremy Blake', 'Sing Me to Sleep'], ['SAINTE', 'Technicolor'], ['Fish in a Birdcage,Philip Bowen', 'Rule #27 - Drunk on Pride'], ['Autoheart', 'The Sailor Song'], ['Seabird', 'Golden Skies'], ['Koethe', 'Run Forever'], ['CHVRCHES', 'The Mother We Share'], ['Draper', 'Who Are You'], ['Kulick', 'Colors'], ['888', 'Critical Mistakes'], ['San Fermin', 'Jackrabbit'], ['Now, Now', 'Wolf'], ['I See Stars', 'Youth'], ['C418', 'Key'], ['C418', 'Door'], ['C418', 'Subwoofer Lullaby'], ['C418', 'Death'], ['C418', 'Living Mice'], ['C418', 'Moog City'], ['C418', 'Haggstrom'], ['C418', 'Minecraft'], ['C418', 'Mice On Venus'], ['C418', 'Dry Hands'], ['C418', 'Wet Hands'], ['C418', 'Clark'], ['C418', 'Chris'], ['C418', 'Excuse'], ['C418', 'Sweden'], ['C418', 'Cat'], ['C418', 'Dog'], ['C418', 'Danny'], ['C418', 'Beginning'], ['C418', 'Droopy Likes Ricochet'], ['C418', 'Droopy Likes Your Face'], ['C418', 'Oxyg,ne'], ['C418', 'kquinoxe'], ['C418', 'Intro'], ['C418', 'Far'], ['C418', 'Blocks'], ['C418', 'Mall'], ['C418', 'Strad'], ['C418', 'Stal'], ['C418', 'Wait'], ['C418', 'Dreiton'], ['C418', 'Beginning 2'], ['C418', 'Taswell'], ['C418', 'Ballad of the Cats'], ['C418', 'Kyoto'], ['C418', 'Aria Math'], ['C418', 'Floating Trees'], ['C418', 'Warmth'], ['C418', 'Haunt Muskie'], ['C418', 'Mutation'], ['C418', 'Biome Fest'], ['C418', 'Concrete Halls'], ['C418', 'Moog City 2'], ['C418', 'Flake'], ['C418', 'Blind Spots'], ['C418', 'Dead Voxel'], ['C418', 'Alpha'], ['C418', 'Ki'], ['C418', 'Axolotl'], ['C418', 'Dragon Fish'], ['C418', 'Shuniji'], ['Lena Raine', 'Pigstep (Stereo Mix)'], ['Lena Raine', 'So Below'], ['Lena Raine', 'Rubedo'], ['Lena Raine', 'Chrysopoeia'], ['Lena Raine', 'Stand Tall'], ['Lena Raine', 'Left to Bloom'], ['Lena Raine', 'Ancestry'], ['Lena Raine', 'Wending'], ['Lena Raine', 'Infinite Amethyst'], ['Lena Raine', 'One More Day'], ['Lena Raine', 'otherside'], ['Kumi Tanioka', 'Floating Dream'], ['Kumi Tanioka', 'Comforting Memories'], ['Kumi Tanioka', 'An Ordinary Day'], ['Lena Raine', 'Firebugs'], ['Lena Raine', 'Aerie'], ['Lena Raine', 'Labyrinthine'], ['Aaron Cherof', 'Echo in the Wind'], ['Aaron Cherof', 'A Familiar Room'], ['Aaron Cherof', 'Bromeliad'], ['Aaron Cherof', 'Crescent Dunes'], ['Aaron Cherof', 'Relic'], ['Marcus Warner', 'Tokyo Rain'], ['Geek Music', 'Interstellar- Main Theme'], ['Hans Zimmer', 'Time'], ['Deadly Avenger', 'Fracture'], ['Yann Tiersen', "Comptine d'un autre -t-, l'apr,s-midi"], ['Hans Zimmer,James Everingham,Adam Lukas', 'Antarctica or Bust'], ['Bicep', 'Glue'], ['65daysofstatic', "Aren't We All Running"], ['Ludovico Einaudi,Daniel Hope,I Virtuosi Italiani', 'Experience'], ['Marcus Warner,Kirsten Horne', 'Deep Blue'], ['Generdyn', 'Ware Is Caleb'], ['Ludwig Gransson', 'Can You Hear The Music'], ['Jamie Duffy', 'Solas'], ['Arcade Fire,Owen Pallett', 'Song on the Beach'], ['Two Steps from Hell', 'Liberty Rising'], ['The Home Of Happy,James Hosmer Griffith,Pablo Clements', 'Echoes'], ['The Home Of Happy,Ryan Small,Maja Slatinsek', 'Fight For It'], ['C418', 'Aria Math but long'], ['unknown', 'Sad Past'], ['Dodie', 'She'], ['Daughter', 'Be On Your Way'], ['Daughter', 'Youth'], ['Daughter', 'Dandelion'], ['Daughter', 'Landfill'], ['Daughter', 'No Care'], ['Daughter', 'Candles'], ['Daughter', 'Human'], ['Daughter', 'Party'], ['Daughter', 'Smother'], ['Daughter', 'Smoke'], ['Daughter', 'Still'], ['Daughter', 'Winter'], ['Daughter', 'Run'], ['Novo Amor', 'Anchor'], ['Runnner,Sun June', 'Colors'], ["Bear's Den", 'When You Break'], ['The Paper Kites', 'Paint'], ['Daughter', 'Burn It Down'], ['Runnner', 'Vines to Make It All Worth It'], ['Tropic Gold', 'Breathe'], ['Normandie', 'Collide'], ['Normandie', 'Blood In The Water'], ['Asking Alexandria', 'Alone In A Room'], ['Bring Me The Horizon', 'MANTRA'], ['Palisades', 'Erase The Pain'], ['Normandie', 'White Flag'], ['Normandie', 'Chemicals'], ['Normandie', 'Enough'], ['Normandie', 'Awakening'], ['Normandie', 'Believe'], ['Normandie', 'Babylon'], ['Normandie', 'Calling'], ['Normandie', 'The Storm'], ['Normandie', 'Epilogue'], ['Young Medicine', 'ShinjQ'], ['Twin Wild', 'Willow Tree'], ['Holding Absence', 'Monochrome'], ['I See Stars', 'Running With Scissors'], ['I See Stars', 'Calm Snow'], ['Bring Me The Horizon', 'Follow You'], ['unknown', 'Coldplay - Paradise (Lyrics)'], ['unknown', 'Coldplay Megamix (Music Video)'], ['Coldplay', 'Fix You'], ['unknown', 'Coldplay - Adventure Of A Lifetime (Official Video)']]
    song = random.choice(music)
    
    return {"endTime" : timetodate(random.randint(1600000000,int(time.time()))),
            "artistName" : song[0],
            "trackName" : song[1],
            "msPlayed" : random.randint(20,240000)
        }

def dummyjson(size=20000):
    data = []
    for a in range(size):
        data.append(makedummy())
    with open('StreamingHistorydummy.json','w') as f:
        json.dump(data,f)

def loadjson():
    data = []
    files = [PyUI.resourcepath(''+f) for f in os.listdir(PyUI.resourcepath('')) if (f[len(f)-5:]=='.json' and 'StreamingHistory' in f)]
    for a in files:
        with open(a,'r',encoding='utf8') as f:
            data += json.load(f)
    return data
    
class Plot:
    def __init__(self):
        pass
    def plot(data,songs,start,end,samplerate,samplesize,artistmode,everything):
        for s in songs:
            graph = []
            samples = [0]
            t = start-samplerate
            index = 0
            while t<end and index+1<len(data):
                a = data[index]
                index+=1
                if (not artistmode and (a['trackName'],a['artistName']) == s) or (artistmode and a['artistName'] == s[1]) or (everything):
                    while datetotime(a['endTime'])>t+samplerate:
                        t+=samplerate
                        graph.append([datetime.datetime.fromtimestamp(t),sum(samples[-4:])])
                        samples.append(0)
                    samples[-1]+=1
            plt.xticks(rotation=30)
            if not everything:
                if artistmode: name = f'{s[1]}'
                else: name = f'{s[0]} - {s[1]}'
                plt.plot(np.array([x[0] for x in graph]),np.array([x[1] for x in graph]),label=name)
            else:
                plt.plot(np.array([x[0] for x in graph]),np.array([x[1] for x in graph]))
        if everything:
            plt.title('All Music')
        else:
            if len(songs) == 1:
                if artistmode: plt.title(f'{songs[0][1]}') 
                else: plt.title(f'{songs[0][0]}-{songs[0][1]}')
            else:
                if artistmode: plt.title('Artists')
                else: plt.title('Songs')
            leg = plt.legend(loc='upper left')
        plt.show()
            
                        




class Main:
    def __init__(self):
        self.data = loadjson()
        self.firstsong = time.time()
        self.lastsong = 0
        for a in self.data:
            t = datetotime(a['endTime'])
            if t<self.firstsong: self.firstsong = t
            if t>self.lastsong: self.lastsong = t
        self.daterange = [self.firstsong,self.lastsong]
        
        self.years = [a+1 for a in range(int(timetodate(self.firstsong).split('-')[0])-1,int(timetodate(self.lastsong).split('-')[0]))]
        self.months = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
        
        self.sumdata()
        self.makegui()
        self.refreshtopcharts()
    def makegui(self):
        # Main page
        ui.maketext(0,-200,'Spotify Stats',100,anchor=('w/2','h/2'),center=True,scalesize=True)
        ui.makebutton(0,-100,'Song Table',50,lambda: ui.movemenu('tablepage','up'),anchor=('w/2','h/2'),center=True,scalesize=True)

        # Main page date system

        ui.maketable(-110,-50,[],[ui.maketext(0,0,'Top Artists',40,backingcol=(87, 132, 86),textcenter=True)],textsize=30,textcenter=False,anchor=('w/2','h/2'),objanchor=('w',0),ID='top artists',width=300,boxheight=[60,-1],height=300,scalesize=True)
        ui.maketable(110,-50,[],[ui.maketext(0,0,'Top Songs',40,backingcol=(87, 132, 86),textcenter=True)],textsize=30,textcenter=False,anchor=('w/2','h/2'),ID='top songs',width=300,boxheight=[60,-1],height=300,scalesize=True)
        ui.maketext(0,20,'',40,anchor=('w/2','h/2'),textcenter=True,center=True,maxwidth=300,scalesize=True,ID='top text')

        ui.makebutton(-20,36,'Back',35,ui.menuback,'tablepage',anchor=('w',0),objanchor=('w','h/2'))



        
        # Search Bar
        self.mainsearchbar = ui.makesearchbar(20,36,width='w/2-40',objanchor=(0,'h/2'),textsize=35,command=self.search,menu='tablepage')
        
        # Date system
        ui.maketext(20,36,'',35,ID='datedisplay',anchor=('w/2',0),objanchor=(0,'h/2'),menu='tablepage')
        self.setdatetext(False)
        # Date menu
        window = ui.makewindow(0,20,327,355,objanchor=('w/2',0),anchor=('w/2',0),menu='tablepage',ID='datewindow',bounditems=[

            ui.maketext(0,5,'Start Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,35,[x+1 for x in range(31)],command=self.setdatetext,pageheight=220,ID='dropdownstartday',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[0])-1),
            ui.makedropdown(80,35,self.months,command=self.setdatetext,pageheight=220,ID='dropdownstartmonth',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[1])),
            ui.makedropdown(233,35,self.years,command=self.setdatetext,pageheight=220,ID='dropdownstartyear',layer=2),

            ui.maketext(0,70,'End Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,105,[x+1 for x in range(31)],command=self.setdatetext,pageheight=150,ID='dropdownendday',startoptionindex=int(timetodate(self.lastsong,True).split('/')[0])-1),
            ui.makedropdown(80,105,self.months,command=self.setdatetext,pageheight=150,ID='dropdownendmonth',startoptionindex=int(timetodate(self.lastsong,True).split('/')[1])),
            ui.makedropdown(233,105,self.years,command=self.setdatetext,pageheight=150,ID='dropdownendyear',startoptionindex=-1),

            ui.makeslider(100,165,140,15,"min(ui.lensummeddata,100)",boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(-10,0,'Results',objanchor=('w','h/2'),anchor=(0,'h/2'))],increment=1,ID='searchresultsnum',startp=30,layer=0),
            ui.makeslider(100,205,140,15,"ui.lensummeddata-min(ui.lensummeddata,100)",boundtext=ui.maketextbox(15,0,'',65,objanchor=(0,'h/2'),anchor=('w','h/2'),numsonly=True,linelimit=1),objanchor=(0,'h/2'),bounditems=[ui.maketext(-20,0,'Start',objanchor=('w','h/2'),anchor=(0,'h/2'))],increment=50,ID='searchstartnum',startp=0,layer=0),

            ui.makelabeledcheckbox(75,235,'Artist Mode',35,textpos='right',toggle=False,ID='artistmode',layer=0),
            ui.makelabeledcheckbox(75,275,'Combine All',35,textpos='right',toggle=False,ID='combineall',layer=0),
            ui.makebutton(0,-10,'Apply',32,self.search,objanchor=('w/2','h'),anchor=('w/2','h'),layer=0)
        ])
        ui.makebutton(40,36,'Edit',35,anchor=('w/2+ui.IDs["datedisplay"].width',0),objanchor=(0,'h/2'),command=window.open,menu='tablepage')

        # Main table
        self.maintable = ui.makescrollertable(20,72,[],[],textsize=25,boxheight=[40,-1],boxwidth=[50,-1,-1,-1,-1,80],width='w-40',pageheight='h-92',scalesize=False,guessheight=36,menu='tablepage')
        self.refreshfiltered()
        ui.makebutton(115,36,'Graph',35,self.opengraphmenu,anchor=('w/2+ui.IDs["datedisplay"].width',0),objanchor=(0,'h/2'),menu='tablepage')
    def search(self):
        ui.IDs['datewindow'].shut()
        self.sumdata()
        artist = self.mainsearchbar.text
        track = artist
        self.refreshtopcharts()
        self.refreshfiltered(artist,track)
    def refreshfiltered(self,artist='',track=''):
        cutoff = ui.IDs['searchresultsnum'].slider
        startp = ui.IDs['searchstartnum'].slider
        if 'artistmode' in ui.IDs: artistmode,everything = ui.IDs['artistmode'].toggle,ui.IDs['combineall'].toggle
        else: artistmode,everything = False,False
            
        ndata = []
        for a in self.summeddata:
            if (artist.lower() in a['Artist'].lower() or track.lower() in a['Track'].lower()):
                ndata.append(a)
        if startp+cutoff>len(ndata):
            startp = max(0,len(ndata)-cutoff)
        ndata = ndata[startp:startp+cutoff]
        tabledata = []
        for i,a in enumerate(ndata):
            if (i+1)%200 == 0: print(i+1)
            tabledata.append([ui.maketext(-100,0,str(startp+i+1),textcenter=True,col=self.maintable.col),a['Artist'],ui.maketext(-100,0,str(a['Listens']),textcenter=True,col=self.maintable.col),mstostr(a['Playtime']),ui.makebutton(-50,0,'{dots}',toggleable=True)])
            if everything:
                del tabledata[-1][1]
            elif not artistmode: tabledata[-1].insert(1,a['Track'])
            tabledata[-1][-1].song = (a['Track'],a['Artist'])
            
        self.maintable.startboxwidth = [50,-1,-1,-1,-1,80]
        titles = ['','Track','Artist','Listens','Total Playtime','']
        if artistmode:
            self.maintable.startboxwidth = [50,-1,-1,-1,80]
            titles = ['','Artist','Listens','Total Playtime','']
        if everything:
            self.maintable.startboxwidth = [50,-1,-1,80]
            titles = ['','Listens','Total Playtime','']
        self.maintable.titles = [ui.maketext(0,0,a,30,textcenter=True) for a in titles]
        self.maintable.data = tabledata

        self.maintable.threadrefresh()

    def refreshtopcharts(self):
        topartists = [[a["Artist"]] for a in self.sumdata(True,True,False)[:5]]
        topsongs = [[a["Track"]+'\n{"'+a["Artist"]+'" col=(190,200,160) scale=0.8}'] for a in self.sumdata(True,False,False)[:5]]
        ui.IDs['top artists'].data = topartists
        ui.IDs['top artists'].refresh()
        ui.IDs['top songs'].data = topsongs
        ui.IDs['top songs'].refresh()
        t0 = self.sumdata(True,False,True)[0]
        total = [str(t0['Listens']),mstostr(t0['Playtime'])]
        perday = t0['Playtime']/(self.daterange[1]-self.daterange[0])/1000/60/60/24
        for i in range(len(total)):
            total[i] = '{"'+total[i]+'" col=(190,200,160)}'
        txt = f'Total Listens\n{total[0]}\nWhich is\n{total[1]}\nPer day\n{perday}'
        ui.IDs['top text'].settext(txt)
        
        
        
    def sumdata(self,retur=False,artistmode=-1,everything=-1):
        starttime = self.daterange[0]
        endtime = self.daterange[1]
        if artistmode == -1:
            if 'artistmode' in ui.IDs: artistmode = ui.IDs['artistmode'].toggle
            else: artistmode = False
        if everything == -1:
            if 'artistmode' in ui.IDs: everything = ui.IDs['combineall'].toggle
            else: everything = False
        self.summeddatadict = {}

        for a in self.data:
            if datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                key = (a['trackName'],a['artistName'])
                if artistmode: key = a['artistName']
                if everything: key = 1
                if not(key in self.summeddatadict):
                    self.summeddatadict[key] = {"Artist":a['artistName'],"Track":a['trackName'],"Listens":1,"Playtime":a['msPlayed']}
                else:
                    self.summeddatadict[key]['Playtime']+=a['msPlayed']
                    self.summeddatadict[key]['Listens']+=1
        if not retur:
            self.summeddata = list(self.summeddatadict.values())
            self.summeddata.sort(key=lambda x: x["Listens"],reverse=True)
            ui.lensummeddata = len(self.summeddata)
        else:
            lis = list(self.summeddatadict.values())
            lis.sort(key=lambda x: x["Listens"],reverse=True)
            return lis
    def countsong(self,info,starttime,endtime,num=True):
        count = 0
        playtime = 0
        for a in self.data:
            if (a['trackName'],a['artistName']) == info and datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                count+=1
                playtime+=a['msPlayed']
        if num: return count
        return playtime

    def setdatetext(self,pull=True):
        if pull:
            self.ui = ui
            self.daterange = [datetotime(f"{ui.IDs['dropdownstartyear'].active}-{self.months.index(self.ui.IDs['dropdownstartmonth'].active)+1}-{ui.IDs['dropdownstartday'].active}"),
                              datetotime(f"{ui.IDs['dropdownendyear'].active}-{self.months.index(self.ui.IDs['dropdownendmonth'].active)+1}-{ui.IDs['dropdownendday'].active}")]
        ui.IDs['datedisplay'].settext(timetodate(self.daterange[0],True)+' {arrow stick=0.5 scale=0.75} '+timetodate(self.daterange[1],True))
    def opengraphmenu(self):
        songs = []
        for a in self.maintable.table:
            if type(a[-1]) == PyUI.BUTTON:
                if not a[-1].toggle:
                    songs.append(a[-1].song)
        if len(songs)>0:
            Plot.plot(self.data,songs,self.daterange[0],self.daterange[1],7*24*60*60,30*24*60*60,ui.IDs['artistmode'].toggle,ui.IDs['combineall'].toggle)
        
main = Main()

while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
    screen.fill(PyUI.Style.wallpapercol)
    ui.rendergui(screen)



    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit()






















