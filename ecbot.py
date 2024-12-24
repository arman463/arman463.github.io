from bale import *
import random
import time
import requests




bot=Bot(token="2124438657:VjQf6x3U65uXiYjFv9G8xo4KZggNVL4HV1RhfNKR") 




@bot.event
async def on_ready():
     #await bot.send_message(5580807305,"ربات روشن شد")

     print('\nbot amade ast ')





     for i in range(1,50000):
         try:
             
            
                 j=requests.get("https://one-api.ir/joke/?token=412682:671400d39ff8f")
                 d=j.json()
                 d2=d.get('result')
                 time.sleep(1.5)
                 await bot.send_message(5192845849,text="جوک شماره "+str(i)+"\n\n"+str(d2)+"\n\n[سازمان جوک 😄😂](https://ble.ir/jokkhanz)")
                 print("sended "+str(i))
         except:
            print("error")
             

        

bot.run()

