#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CupiDetectives
"""

#PRIMER PUNTO DEL PARCIAL.
def crear_sospechoso(codigo: int, nombre: str, edad: int, altura: float, pantalon: str, camisa: str, usaba_gafas: bool, salon: str, coartada_confirmada: bool, huellas_confirmadas: bool) -> dict:
  
     sospechoso = {
        "codigo": codigo,
        "nombre": nombre,
        "edad": edad,
        "altura": altura,
        "pantalon": pantalon,
        "camisa": camisa,
        "usaba_gafas": usaba_gafas,
        "salon": salon,
        "coartada_confirmada": coartada_confirmada,
        "huellas_confirmadas": huellas_confirmadas
     }
     return sospechoso
    

def crear_perfil_culpable(edad_estimada: int, altura_estimada: float, color_pantalon: str, color_camisa: str, usaba_gafas: bool, salon_incidente: str) -> dict:
   
    perfil = {
        "edad_estimada": edad_estimada,
        "altura_estimada": altura_estimada,
        "color_pantalon": color_pantalon,
        "color_camisa": color_camisa,
        "usaba_gafas": usaba_gafas,
        "salon_incidente": salon_incidente
    }
    
    return perfil


def buscar_por_codigo(codigo: int, s1: dict, s2: dict, s3: dict, s4: dict) -> dict:

    if s1["codigo"] == codigo:
        return s1
    elif s2["codigo"] == codigo:
        return s2
    elif s3["codigo"] == codigo:
        return s3
    elif s4["codigo"] == codigo:
        return s4
    else:
        return {} 

def filtrar_sospechosos_por_ubicacion(perfil_culpable: dict, s1: dict, s2: dict, s3: dict, s4: dict) -> str:
    
    salon_culpable = perfil_culpable["salon_incidente"]
    sospechosos_en_salon = []

    for sospechoso in [s1, s2, s3, s4]:
        if sospechoso["salon"] == salon_culpable:
            sospechosos_en_salon.append(str(sospechoso["codigo"]))  

    return ", ".join(sospechosos_en_salon) if sospechosos_en_salon else "Ninguno"


def filtrar_sospechosos_por_vestimenta(perfil_culpable: dict, s1: dict, s2: dict, s3: dict, s4: dict) -> str:

    color_pantalon_culpable = perfil_culpable["color_pantalon"]
    color_camisa_culpable = perfil_culpable["color_camisa"]
    gafas_culpable = perfil_culpable["usaba_gafas"]

    sospechosos_validos = []

    for sospechoso in [s1, s2, s3, s4]:
        if (color_pantalon_culpable in sospechoso["pantalon"] and
            color_camisa_culpable in sospechoso["camisa"] and
            gafas_culpable == sospechoso["usaba_gafas"]):
            sospechosos_validos.append(str(sospechoso["codigo"]))  # Convertimos código a string

    return ", ".join(sospechosos_validos) if sospechosos_validos else "Ninguno"



def filtrar_sospechosos_por_edad_altura(perfil_culpable: dict, s1: dict, s2: dict, s3: dict, s4: dict) -> str:
    
    edad_max = perfil_culpable["edad_estimada"]
    altura_min = perfil_culpable["altura_estimada"] - 0.10  # 10 cm menos
    altura_max = perfil_culpable["altura_estimada"] + 0.10  # 10 cm más

    sospechosos_validos = []

    for sospechoso in [s1, s2, s3, s4]:
        if (sospechoso["edad"] <= edad_max and altura_min <= sospechoso["altura"] <= altura_max):
            sospechosos_validos.append(str(sospechoso["codigo"]))  # Convertimos código a string

    return ", ".join(sospechosos_validos) if sospechosos_validos else "Ninguno"



def calcular_probabilidad_de_culpabilidad(codigo: int, perfil_culpable: dict, s1: dict, s2: dict, s3: dict, s4: dict) -> float:

    sospechosos_ubicacion = filtrar_sospechosos_por_ubicacion(perfil_culpable, s1, s2, s3, s4)
    sospechosos_vestimenta = filtrar_sospechosos_por_vestimenta(perfil_culpable, s1, s2, s3, s4)
    sospechosos_edad_altura = filtrar_sospechosos_por_edad_altura(perfil_culpable, s1, s2, s3, s4)

    codigo_str = str(codigo)

    # Asignar valores de a, b y c según si el código aparece en las listas
    a = 1 if codigo_str in sospechosos_ubicacion.split(", ") else 0
    b = 1 if codigo_str in sospechosos_vestimenta.split(", ") else 0
    c = 1 if codigo_str in sospechosos_edad_altura.split(", ") else 0

    # Calcular la probabilidad
    probabilidad = (a * 0.45) + (b * 0.35) + (c * 0.20)

    # Retornar la probabilidad redondeada a 2 decimales
    return round(probabilidad, 2)



def encontrar_sospechoso_con_mayor_probabilidad(perfil_culpable: dict, s1: dict, s2: dict, s3: dict, s4: dict) -> dict:
    """
    Busca al sospechoso con la mayor probabilidad de ser culpable.
    """

    sospechosos = [s1, s2, s3, s4]
    
    probabilidades = {
        sospechoso["codigo"]: calcular_probabilidad_de_culpabilidad(sospechoso["codigo"], perfil_culpable, s1, s2, s3, s4)
        for sospechoso in sospechosos
    }

    max_probabilidad = max(probabilidades.values())

    candidatos = [s for s in sospechosos if probabilidades[s["codigo"]] == max_probabilidad]

    candidatos = sorted(candidatos, key=lambda s: s["coartada_confirmada"])

    candidatos = sorted(candidatos, key=lambda s: not s["huellas_confirmadas"])

    return candidatos[0]

#Punto #2 del parcial 
def salon(s1: dict, s2: dict, s3: dict, s4: dict, edificio: str) -> bool:
 

    # Revisar si alguno de los sospechosos estuvo en el salón dado
    return any(sospechoso["salon"] == edificio for sospechoso in [s1, s2, s3, s4])

#punto 3 del parcial
def invertir_coartada(s1: dict, s2: dict, s3: dict, s4: dict) -> None:

    # Lista con los diccionarios de los sospechosos
    sospechosos = [s1, s2, s3, s4]

    # Iterar sobre cada sospechoso y modificar su coartada
    for sospechoso in sospechosos:
        sospechoso["coartada_confirmada"] = not sospechoso["coartada_confirmada"]


#Punto 4.
def gafas_altura(s1: dict, s2: dict, s3: dict, s4: dict, altura_cm: int) -> str | None:

    # Lista de diccionarios de sospechosos
    sospechosos = [s1, s2, s3, s4]

    # Filtrar sospechosos que cumplan ambas condiciones
    resultado = [
        str(sospechoso["codigo"])  # Convertir código a string para la salida
        for sospechoso in sospechosos
        if (sospechoso["altura"] * 100 > altura_cm) and sospechoso["usaba_gafas"]
    ]

    # Retornar los códigos separados por comas o None si no hay resultados
    return ", ".join(resultado) if resultado else None


