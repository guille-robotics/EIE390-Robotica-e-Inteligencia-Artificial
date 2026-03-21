print("Ingrese Nombre: ")
nombre=input().strip().lower() #strip(), permite quitar espacios en blanco al inicio y final, lower(), permite colocar todo en minuscula
print("Ingrese Edad: ")
edad=int(input().strip())

if edad>= 18:
    print(f"Usted, {nombre}, es mayor de edad, porque tiene {edad} años")
else:
    print(f"Usted, {nombre}, es menor de edad, porque tiene {edad} años")
        
