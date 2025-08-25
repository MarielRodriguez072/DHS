
def main():
    nombrearchivo = "registro_temperatura365d_smn.txt"


    with open(nombrearchivo, 'r', encoding='latin1' ) as archivo:
        print("hola")

        lineas = archivo.readlines()

        for linea in lineas:
            print(linea)
            
            
if __name__ == "__main__":
    main()