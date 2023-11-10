import pygame,math,random,datetime,time,json,copy
import matplotlib.pyplot as plt, numpy as np
import PyUI as PyUI
pygame.init()
screen = pygame.display.set_mode((1200, 800),pygame.RESIZABLE)
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
            "artistsName" : song[0],
            "trackName" : song[1],
            "msPlayed" : random.randint(20,240000)
        }

def dummyjson(size=20000):
    data = []
    for a in range(size):
        data.append(makedummy())
    with open('StreamingHistory1.json','w') as f:
        json.dump(data,f)

def loadjson():
    with open('StreamingHistory1.json','r') as f:
        data = json.load(f)
    return data
    
class Plot:
    def __init__(self):
        pass
    def plot(data,songs,samplerate,samplesize,start,end):
        for s in songs:
            y = []
            x = []
            for a in 
                if datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                    if (a['trackName'],a['artistsName']) == s:




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

        self.years = [a+1 for a in range(int(timetodate(self.firstsong).split('-')[0]),int(timetodate(self.lastsong).split('-')[0]))]
        self.months = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
        
        self.sumdata()
        self.makegui()
    def makegui(self):
        # Search Bar
        self.mainsearchbar = ui.makesearchbar(20,36,width='w/2-40',objanchor=(0,'h/2'),textsize=35,command=self.search)
        
        # Date system
        ui.maketext(20,36,'',35,ID='datedisplay',anchor=('w/2',0),objanchor=(0,'h/2'))
        self.setdatetext(False)
        # Date menu
        window = ui.makewindow(0,20,327,300,objanchor=('w/2',0),anchor=('w/2',0),ID='datewindow',bounditems=[

            ui.maketext(0,5,'Start Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,35,[x+1 for x in range(31)],command=self.setdatetext,pageheight=220,ID='dropdownstartday',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[0])-1),
            ui.makedropdown(80,35,self.months,command=self.setdatetext,pageheight=220,ID='dropdownstartmonth',layer=2,startoptionindex=int(timetodate(self.firstsong,True).split('/')[1])),
            ui.makedropdown(233,35,self.years,command=self.setdatetext,pageheight=220,ID='dropdownstartyear',layer=2),

            ui.maketext(0,70,'End Date',35,objanchor=('w/2',0),anchor=('w/2',0)),
            ui.makedropdown(10,105,[x+1 for x in range(31)],command=self.setdatetext,pageheight=150,ID='dropdownendday',startoptionindex=int(timetodate(self.lastsong,True).split('/')[0])-1),
            ui.makedropdown(80,105,self.months,command=self.setdatetext,pageheight=150,ID='dropdownendmonth',startoptionindex=int(timetodate(self.lastsong,True).split('/')[1])),
            ui.makedropdown(233,105,self.years,command=self.setdatetext,pageheight=150,ID='dropdownendyear',startoptionindex=-1),

            ui.makebutton(0,-10,'Apply',32,self.search,objanchor=('w/2','h'),anchor=('w/2','h'),layer=0)
        ])
        ui.makebutton(40,36,'Edit',35,anchor=('w/2+ui.IDs["datedisplay"].width',0),objanchor=(0,'h/2'),command=window.open)
        # Main table
        titles = ['','Track','Artist','Listens','Total Playtime','']
        titleobjs = [ui.maketext(0,0,a,30,textcenter=True) for a in titles]
        self.maintable = ui.makescrollertable(20,80,[],titleobjs,textsize=25,boxheight=[40,-1],boxwidth=[50,-1,-1,-1,-1,80],width='w-40',pageheight='h-100',scalesize=False,guessheight=36)
        self.refreshfiltered()
    def search(self):
        ui.IDs['datewindow'].shut()
        self.sumdata()
        artist = self.mainsearchbar.text
        track = artist
        self.refreshfiltered(artist,track)
    def refreshfiltered(self,artist='',track='',cutoff=25):
        ndata = []
        for a in self.summeddata:
            if (a['Artist'].lower()!='daughter') and (artist.lower() in a['Artist'].lower() or track.lower() in a['Track'].lower()):
                ndata.append(a)
        ndata = ndata[:cutoff]
        tabledata = []
        for i,a in enumerate(ndata):
            tabledata.append([ui.maketext(0,0,str(i+1),textcenter=True,col=self.maintable.col),a['Track'],a['Artist'],ui.maketext(0,0,str(a['Listens']),textcenter=True,col=self.maintable.col),mstostr(a['Playtime']),ui.makebutton(0,0,'{dots}')])
        self.maintable.data = tabledata
        self.maintable.refresh()


        
    def sumdata(self):
        starttime = self.daterange[0]
        endtime = self.daterange[1]
        self.summeddatadict = {}
        tempdata = copy.deepcopy(self.data)
        for a in tempdata:
            if datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
                if not((a['trackName'],a['artistsName']) in self.summeddatadict):
                    self.summeddatadict[(a['trackName'],a['artistsName'])] = {"Artist":a['artistsName'],
                                                                              "Track":a['trackName'],
                                                                              "Listens":self.countsong((a['trackName'],a['artistsName']),starttime,endtime),
                                                                              "Playtime":self.countsong((a['trackName'],a['artistsName']),starttime,endtime,False)}
        self.summeddata = [self.summeddatadict[a] for a in self.summeddatadict]
        self.summeddata.sort(key=lambda x: x["Listens"],reverse=True)
    def countsong(self,info,starttime,endtime,num=True):
        count = 0
        playtime = 0
        for a in self.data:
            if (a['trackName'],a['artistsName']) == info and datetotime(a['endTime'])>starttime and datetotime(a['endTime'])<endtime:
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

























