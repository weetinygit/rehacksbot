#Importing relevant modules
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import paho.mqtt.client as mqtt


#Needed for debug - Programme will print if errors are identified
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#Replace this with your telegram bot token!
TOKEN = "531011921:AAEElnd-R0UwKMmXpW6zjAT8GaI84c0xrqs"

#Replace these parameters with your MQTT parameters
mqtt_user="sguwsyqh"
mqtt_password="JeV_peEntLS_"
mqtt_server="m23.cloudmqtt.com"
mqtt_port=13982

#Assign bot managers
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher     #Needed for callbacks

#Callback functions for telegram bot
def start(bot, update):
    print "Start command received from chat "+str(update.message.chat_id)
    
   # Sends message with reply keyboard attached
    reply_keyboard = [['Turn on lights'],['Turn off lights', 'Later!']]
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, what can I do for you today?", reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
def echo(bot, update):
    print "Message received from chat "+str(update.message.chat_id)+": "+update.message.text
    #Publish MQTT upon receiving "Turn on LED"
    if (update.message.text == "Turn on lights"):
        client.publish("ledStatus", "1", qos=2, retain=False)
        bot.send_message(chat_id=update.message.chat_id, text="Turning on lights")
    elif (update.message.text == "Turn off lights"):
        client.publish("ledStatus", "0", qos=2, retain=False)
        bot.send_message(chat_id=update.message.chat_id, text="Turning off lights")
    elif (update.message.text == "Later!"):
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Ttyl!", reply_markup = reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Didn't quite understand that!")

    
#This function will run on startup
def main():
    #These lines of code attaches commands or messages to the desired callback functions
    start_handler = CommandHandler('start', start)        #Upon receiving '/start' command, run function named 'start'
    dispatcher.add_handler(start_handler)
    
    echo_handler = MessageHandler(Filters.text, echo)     #Upon receiving any messages of text kind, run function named 'echo'
    dispatcher.add_handler(echo_handler)
    

    updater.start_polling(poll_interval = 0.5)            #Start retriving data from telegram server at 0.5s interval    
    updater.idle()

#Callback functions for MQTT with paho
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#MQTT-related declarations
client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(mqtt_user, password=mqtt_password)
client.connect_async(mqtt_server, mqtt_port, 60)
client.loop_start()


#Only run "main" function if this program is called
if __name__ == '__main__':
    main()