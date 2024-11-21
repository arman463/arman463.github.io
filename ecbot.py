from bale import *
import random
import time
import requests





#print("----------\n\n\n")

print("\n\nrunning bot ...")
     

mutegr={'test'}



bot=Bot(token="2050020615:9kYPZ5NBO5xh7z1MJwYhnXekcHOGWLN3eGRWPxcO")



qu={
    "هرهرهر":"نخند😐"
    ,"خداحافظ":"خداحافظ داداچ"
    ,"خدافظ":"خداحافظ داداچ"}




x=0
y=0
import time
user=0
chatid=0
cor=False
cornum=0
@bot.event
async def on_ready():
     #await bot.send_message(5580807305,"ربات روشن شد")

     print('\nbot amade ast ')




@bot.event
async def on_message(message: Message):

    
    
    print("\npayam : ",message.text,"\naz taraf : ",message.author.first_name)


    global qu

    global mutegr

    global cor

    global cornum

    if message.text == "آن میوت کردن" :
        if not message.chat_id in mutegr :
             #await bot.delete_message(chat_id=message.chat_id,message_id=message.message_id)
             
             await bot.send_message(message.chat_id,"گروه در حال حاضر ميوت نيست !")

        else :
             mutegr.remove(message.chat_id)
             await bot.send_message(message.chat_id,"ارسال پيام آزاد شد !")

             



    if message.chat_id in mutegr :
         await bot.delete_message(chat_id=message.chat_id,message_id=message.message_id)
         return()
   
    global user
    global chatid

    user=message.author.id
    chatid=message.chat_id


    #if message.text=="اسم شانسی سریع" :
         #myl=["آرمان","عرفان","محيا"]
         #myl2=random.choice(myl)
         #await bot.send_message(message.chat_id,str(myl2))


    if "ارسال" in message.text :

        if not message.author.id == 1366209144 :
            await bot.send_message(message.chat_id,"دسترسي نداري")
            #
        else :
            #
            #
            msg=message.text.replace("ارسال ","")
         
            if "گروه باحالان" in msg :
                await bot.send_message(5580807305,msg.replace("گروه باحالان",""))

            elif "عرفان" in message.text :
             
                await bot.send_message(2027032713,msg.replace("عرفان",""))
                print("sended")

            elif "الین" in message.text :
                await bot.send_message(2099562928,msg.replace("الین",""))
                print("sended")
    if "حساب کردن " in message.text :
        ev = message.text.replace("حساب کردن ","")
        pplus=message.text.replace("+","")
        pplus=pplus.replace("*","")
        pplus=pplus.replace("-","")
        pplus=pplus.replace("/","")
    ##print(pplus.isnumeric)

        if pplus.isnumeric :
          
              await message.reply(str(eval(ev)))



 
    if message.text=="میوت کردن گروه":
         await bot.send_message(chat_id=chatid,text="گروه ميوت شد")
         mutegr.add(message.chat_id)



    if message.text in qu :
         for i in qu.keys() :
              if i == message.text :
                   await bot.send_message(chat_id=chatid,text=qu.get(i))

    #if cor == True :
         #time.sleep(1)
         #cornum+=1
         #await bot.send_message(chat_id=chatid,text=str(cornum))


    if "ترجمه" in message.text:
         print("this is test !")
         c=await bot.send_message(chat_id=chatid,text="gekko")
         #print(c.message_id)
         await bot.edit_message(message_id=c.message_id,chat_id=chatid,text="hey !")
         #await bot.send_message(chat_id=chatid,text=tra.translate(message.text.replace("ترجمه","")))



    if message.text=="فال حافظ":
          j=requests.get("https://one-api.ir/hafez/?token=412682:671400d39ff8f")
          
          d=j.json()
          d2=d.get('result')
          #print(d2.get("RHYME"))
          print(str(d2))

          tx="فال حافظ گرفته شد ! 📖\n\n"+d2.get("TITLE")+"\n\n"+"```[مشاهده کامل]"+d2.get("RHYME")+"```"+"\nتفسیر و معنی : \n\n"+d2.get("MEANING")
          await bot.send_message(text=tx,chat_id=chatid,reply_to_message_id=message.message_id)



    if message.text=="قیمت دلار" :
        j=requests.get("https://one-api.ir/price/?token=412682:671400d39ff8f")
        j2=j.json()
        j3=j2.get('result').get("currencies").get("dollar").get("p")
        await message.reply("قيمت دلار در حال حاضر "+str(j3)+" ريال است ")

    if message.text=="قیمت سکه":


        j=requests.get("https://one-api.ir/price/?token=412682:671400d39ff8f")
        j2=j.json()
        j3=j2.get('result').get("coin")

        i="قيمت سکه امامي "+j3.get("sekee").get("p")+" ريال است \n\n"

        g="قیمت یک گرم سکه "+j3.get("gerami").get("p")+" ريال است \n\n"

        b="قيمت سکه بهار آزادي "+j3.get("sekeb").get("p")+" ريال است \n\n"

        n="قيمت نيم سکه "+j3.get("nim").get("p")+" ريال است \n\n"

        r="قيمت ربع سکه "+j3.get("rob").get("p")+" ريال است \n\n"


        
        await message.reply(i+b+n+r+g+"اطلاعات به روز است و از سايت tgju.org دريافت مي شود")
        


    if "😂" in message.text :
          await message.reply("😐😂😂😐")


    if True :
         pass


         

         

         
         

          




    

             


    #if message.text=="مدیر کن":
         #if message.author.id==1366209144 or message.author.id==2099562928:
          #await bot.send_message(message.chat_id,"جناب رييس بله حتما !")
         # await bot.promote_chat_member(chat_id=message.chat_id,user_id=message.author.id,can_post_messages=True,can_change_info=True,can_edit_messages=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True)
          #await bot.promote_chat_member(chat_id=message.chat_id,user_id=2099562928,can_post_messages=True)
         #else :
               
               #await bot.send_message(message.chat_id,"به حرف تو گوش نميدم !"+str(message.author.id))

@bot.event
async def on_callback(callback: CallbackQuery):

     if callback.data == "rem":
          await bot.send_message(chat_id=chatid,text="از گروه باحالان حذف شدي چون خودت گفتي هرهرهر")
          await bot.ban_chat_member(chat_id=chatid,user_id=user)
     elif callback.data == "norem":
          await bot.send_message(chatid,"هرهرهر ترسيدي ؟ ولي بازم من چند ثانيه ديگه حذفت ميکنم")
          time.sleep(5)
          await bot.send_message(chatid,"شوخي کردم ترسو !")

        
             
             



bot.run()

