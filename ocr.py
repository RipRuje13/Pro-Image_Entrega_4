import cv2
from PIL import Image
from pytesseract import *
import re

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def reconocer_texto_con_numeros_linea(img):
    # Convertir la imagen a escala de grises
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para obtener una imagen binaria
    _, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Buscar contornos en la imagen binaria
    contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ordenar los contornos de arriba hacia abajo
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    lineas = []

    for contour in contours:
        # Obtener las coordenadas del contorno
        x, y, w, h = cv2.boundingRect(contour)

        # Recortar la región del contorno de la imagen original
        roi = img[y:y+h, x:x+w]

        # Convertir la región recortada en una imagen de PIL
        img_linea = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

        # Reconocer el texto en la línea
        linea_texto = pytesseract.image_to_string(img_linea, lang='spa')

        # Agregar la línea al resultado
        lineas.append(linea_texto.strip())

    # Eliminar los renglones vacíos
    lineas = [linea for linea in lineas if linea.strip() != ""]

    # Concatenar todas las líneas en un solo texto plano
    texto_plano = " ".join(lineas)

    return texto_plano

# Cargar la imagen
img = cv2.imread("m3.jpg")

# Reconocer todo el texto en líneas horizontales y copiarlo a una variable de texto plano
texto_obtenido = reconocer_texto_con_numeros_linea(img)

# Eliminar los renglones vacíos de la variable texto_obtenido
lineas = texto_obtenido.split('\n')
lineas = [linea for linea in lineas if linea.strip() != ""]
texto_obtenido = '\n'.join(lineas)

# Buscar el renglón que contiene la palabra "nombre" y mostrar ese renglón y los tres renglones siguientes
#print("Búsqueda de la palabra 'nombre':")
for i, linea in enumerate(lineas):
    if "nombre" in linea.lower():
        indice = i
        break

if indice is not None:
    print("NOMBRE")
    for j in range(indice+1, min(indice+4, len(lineas))):
        palabras = re.findall(r'\b[A-Za-z]+\b', lineas[j])
        palabras_filtradas = [palabra for palabra in palabras if not any(c.isdigit() or not c.isalpha() for c in palabra)]
        linea_filtrada = ' '.join(palabras_filtradas)
        print(linea_filtrada)
else:
    print("No se encontró un renglón con la palabra 'nombre'.")

print()

# Buscar el renglón que contiene la palabra "domicilio" y mostrar ese renglón y los tres renglones siguientes
#print("Búsqueda de la palabra 'domicilio':")
for i, linea in enumerate(lineas):
    if "domicilio" in linea.lower():
        indice = i
        break

if indice is not None:
    print(f"DOMICILIO")
    #print("Renglones siguientes:")
    for j in range(indice+1, min(indice+4, len(lineas))):
        if j == len(lineas)-1 and "clave" in lineas[j].lower():
            continue  # Omitir la impresión si el último renglón contiene la palabra "clave"
        print(f"{lineas[j]}")
else:
    print("No se encontró un renglón con la palabra 'domicilio'.")

print()

# Buscar la palabra "curp" y mostrar esa palabra y la cadena de caracteres siguiente
#print("CURP")
for i, linea in enumerate(lineas):
    if "curp" in linea.lower():
        indice = i
        break

if indice is not None:
    #print(f"Renglón con la palabra 'curp': {lineas[indice]}")
    palabras = lineas[indice].split()
    if "curp" in palabras:
        indice_palabra_curp = palabras.index("curp")
        if indice_palabra_curp < len(palabras) - 1:
            siguiente_palabra = palabras[indice_palabra_curp + 1]
            print(f"CURP \n{siguiente_palabra}")
        else:
            print("No se encontró una cadena de caracteres siguiente.")
else:
    print("No se encontró un renglón con la palabra 'curp'.")

print()

# Buscar la palabra "emisión" y mostrar esa palabra y la siguiente palabra
#print("\nBúsqueda de la palabra 'emision':")
for i, linea in enumerate(lineas):
    if "emisión" in linea.lower():
        indice = i
        break

if indice is not None:
    print(f"Renglón con la palabra 'emision': {lineas[indice]}")
    palabras = lineas[indice].split()
    if "emisión" in palabras:
        indice_palabra_emision = palabras.index("emisión")
        if indice_palabra_emision < len(palabras) - 1:
            siguiente_palabra = palabras[indice_palabra_emision + 1]

            print(f"Siguiente palabra: {siguiente_palabra}")
        else:
            print("No se encontró una cadena de caracteres siguiente.")
else:
    print("No se encontró un renglón con la palabra 'emision'.")