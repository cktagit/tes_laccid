import os
import telebot

BOT_TOKEN = os.environ['BOT_TOKEN']  #token bot tele

bot = telebot.TeleBot("6279274872:AAHaZJnpwSSZm3OrnX--h_xKHY1OJmzsj-I")


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
  bot.reply_to(message, "lalalala yeyeyeye")


def extract_arg(arg):
  return arg.split()[1:]


@bot.message_handler(commands=['cek'])
def yourCommand(message):
  bot.reply_to(message, extract_arg(message.text))


from http.client import HTTPSConnection
import json


def extract_location(a, b, c, d):
  apiKey = "0a69a1f3c4fa10ba209d"  #Api dari combain
  data = {
    "radioType":
    "gsm",
    "cellTowers": [{
      "mobileCountryCode": a,
      "mobileNetworkCode": b,
      "locationAreaCode": c,
      "cellId": d,
      "signalStrength": -64
    }]
  }
  headers = {"Content-Type": "application/json"}
  conn = HTTPSConnection("apiv2.combain.com")
  conn.request("POST", "/?key=" + apiKey, json.dumps(data), headers)
  response = conn.getresponse()
  result = json.load(response)

  if ("location" in result):
    output = [result['location']['lat'], result['location']['lng']]
  else:
    output = ("The following error occurred: " + result['error']['message'])
  return output


@bot.message_handler(commands=['laccid'])
def get_location(message):
  laccid = extract_arg(message.text)
  laccid = laccid[0].split("-")
  mcc, net, area, cell = laccid

  lat, lon = extract_location(mcc, net, area, cell)
  location = ("https://maps.google.com/maps?q=" + str(lat) + "," + str(lon))
  bot.reply_to(message, location)
  bot.send_location(message.chat.id, lat, lon)


bot.infinity_polling()
