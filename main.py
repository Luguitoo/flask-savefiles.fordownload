from flask import Flask, render_template, request, send_file
import os
import pathlib

app = Flask(__name__)

folder = os.path.abspath("./media/")
ext_p = set(["docx"])
app.config['folder'] = folder

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        nombre =  request.form.get("nombre")
        archivo = request.files["archivo"]
        #Primero guardar, luego buscar...
        if "archivo" not in request.files:
            print("No envio nada")
            pass
        elif archivo.filename == "":
            print("No mando nada")
            pass
        elif archivo and archpermi(archivo.filename):
            filename = archivo.filename.split('.')
            ext = filename[len(filename) - 1]
            print(ext)
            print(filename)
            print(nombre)
            filename = "documento_" + nombre + "." + ext
            #documento_Carlos.docx
            print(filename)
            archivo.save(os.path.join(app.config["folder"], filename)) #Guarda
        else:
            print("archivo no permitido")
    return render_template('index.html')

@app.route('/buscar', methods = ['GET', 'POST'])
def buscar():
    ruta = pathlib.Path('./media/')
    if request.method == "POST":
        nombre = request.form.get("nombre")
        filename = "documento_" + nombre + ".docx"
        archivo = ruta / filename #Si existe un docx con su nombre
        print(archivo)
        if archivo.exists():
            print("El arhivo existe")
            return send_file(archivo, as_attachment=True)
        else:
            print("No existe")
    return render_template('buscar.html')
def archpermi(filename):
  filename = filename.split('.')
  if filename[len(filename) - 1] in ext_p:
      return True
  return False


if __name__=='__main__':
    app.run(debug = True, port= 8000)