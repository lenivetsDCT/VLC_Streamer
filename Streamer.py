import vlc,threading,os,sys
from datetime import datetime

if len(sys.argv) == 1:
   glob = "E:\\"
else:
   glob = sys.argv[1]
p={}
med={}
port=1908
bport=1908
run=False
run_dir=''

def run_movie(dir):
    global port
    global med
    global p
    global run
    for file in os.listdir(dir):
        if file.endswith(".ts"):
           med[port] = vlc.Instance("""--input-repeat=-1 --sout=#:http{mux=ts,dst=:"""+str(port)+"""/} :file-caching=500 :sout-all :sout-keep -I dummy""").media_new(os.path.join(dir,file))
           p[port]=med[port].player_new_from_media()
           p[port].play()
           port+=1

def set_time ():
    global p
    for r in range(bport, port):
       p[r].set_time(round((datetime.now().hour*60+ datetime.now().minute)) % round(p[r].get_length()/1000/60)*60*1000)
    print("-- Time set to correct --")

def do_every (interval, worker_func, iterations = 0):
  if iterations != 1:
    threading.Timer (
      interval,
      do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
    ).start ()
  worker_func ()

def print_status ():
    for r in range(bport, port):
        print("[",datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"]",'Media: %s' % med[r].get_mrl()," | ",'Current time: %s/%s min' % (round(p[r].get_time()/1000/60), round(med[r].get_duration()/1000/60))," | ",'Position: %s' % round(p[r].get_position()*100,1), "%")
    print('\n')

def get_dir ():
    global glob
    global run
    global run_dir
    global port
    for root, dirs, files in os.walk(glob):
        for tmp in dirs:
          if len(tmp.split('_')) > 1:
             if datetime.strptime('2017-'+tmp.split('_')[1], '%Y-%d%m').date() >= datetime.now().date():
               if datetime.strptime('2017-'+tmp.split('_')[0], '%Y-%d%m').date() <= datetime.now().date():
                  if run_dir != os.path.join(root,tmp):
                     for r in range(bport, port): 
                        p[r].stop()
                        port=bport
                     run_movie(os.path.join(root,tmp))
                     run_dir=os.path.join(root,tmp)
                     run = True
do_every (10,get_dir)

if run == True:
   do_every (5, print_status)
   
if run == True:
   t = threading.Timer (3,set_time)
   t.start()
