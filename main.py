from roboflow import Roboflow
import telebot
bot = telebot.TeleBot('5763022714:AAHmv9n1caRLk5QplFaiG2RUOnpCzwr7WKs')

@bot.message_handler(content_types=["photo"])
def send_photo(message):
    rf = Roboflow(api_key="qvDhnX4pAdOURz3f7kyI")
    project = rf.workspace().project("dogs-cats-rats")
    model = project.version(2).model

    photoID = message.photo[-1].file_id
    photoInfo = bot.get_file(photoID)
    downloader = bot.download_file(photoInfo.file_path)

    with open("result.jpg", "wb") as new_file:
        new_file.write(downloader)

    model.predict("result.jpg", confidence=40, overlap=30).save("prediction.jpg")

    with open("prediction.jpg", "rb") as prediction:
        bot.send_photo(message.chat.id, prediction)

bot.polling()