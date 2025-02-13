import discord
import asyncio
from discord.ext import commands


#----------BOT-DISCORD---

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def upload_image(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("No se ha encontrado ninguna imagen adjunta.")
    else:
        # Iterar sobre los archivos adjuntos
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(('jpg', 'jpeg', 'png')):
                # Guardar la imagen en el sistema de archivos local
                filepath = f"images/{attachment.filename}"
                await attachment.save(filepath)
                
                # Enviar la URL de la imagen de vuelta al usuario
                #await ctx.send(clasificador(f"./{attachment.filename}"))
                await ctx.send(clasificador(f"images/{attachment.filename}"))
                await ctx.send(f"Imagen {attachment.filename} guardada con éxito. Disponible en: {attachment.url}")
            else:
                await ctx.send(f"El archivo {attachment.filename} no es una imagen válida.")

@bot.command()
async def hola(ctx):
    await ctx.send(f'Hola, {ctx.author}')


def start_bot():
    asyncio.get_event_loop().run_until_complete(bot.start("token"))

import nest_asyncio
nest_asyncio.apply()

start_bot()



#----------RED-NEURONAL---

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def clasificador(image):
  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model("keras_model.h5", compile=False)

  # Load the labels
  class_names = open("labels.txt", "r").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
  image = Image.open(image).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  # Print prediction and confidence score
  print("Class:", class_name[2:], end="")
  print("Confidence Score:", confidence_score)

  print(class_name)


  if class_name[2:] == "Sedan\n":
    return("Sedan; Ideal para familias y uso diario. Ofrece un buen equilibrio entre comodidad, espacio y eficiencia. Ideal para desplazarse en la ciudad.")
  elif class_name[2:] == "Suv\n":
    return("Suv; Adecuado para quienes necesitan más espacio y capacidad todoterreno. Excelente para familias grandes, y condiciones de carretera adversas. Tienen una posición de conducción elevada que mejora la visibilidad.")
  elif class_name[2:] == "Hatchback\n":
    return("Hatchback; Compacto y versátil, ideal para la vida urbana. Ofrece fácil maniobrabilidad y un buen espacio de carga gracias a su diseño de portón trasero. Auto práctico y económico.")
  elif class_name[2:] == "Coupe\n":
    return("Coupe; Estilo deportivo, con dos puertas y un diseño elegante. Es perfecto para quienes buscan una experiencia de conducción emocionante y no necesitan tanto espacio. Es adecuado para parejas o personas que viajan solas.")
  elif class_name[2:] == "Pickup\n":
    return("Pick-Up; Excelente para trabajos que requieren transportar cargas pesadas. Ideal para construcciones, agricultura y actividades al aire libre. Buena opción para quienes necesitan remolcar otros vehículos o equipos.")


#return "funciona"


#------------FUNCION---

from google.colab import files

path = files.upload()
path = list(path.keys())[0]
image=Image.open(path)

clasificador(image)
