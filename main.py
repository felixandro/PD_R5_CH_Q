import streamlit as st
import pandas as pd
from random import choice, random
import json
import time
import textwrap
import services as s

############################################
### Variables de Estado ####################
############################################

if "hora_id" not in st.session_state:
    st.session_state.hora_id = time.strftime("%Y-%m-%d %H:%M:%S")

if "id_encuestador" not in st.session_state:
    st.session_state.id_encuestador = False

if "texto_introductorio" not in st.session_state:
    st.session_state.texto_introductorio = False

if "caracteristicas" not in st.session_state:
    st.session_state.caracteristicas = False

if "perfiles" not in st.session_state:
    st.session_state.perfiles = False

if "ingreso" not in st.session_state:
    st.session_state.ingreso = False

if "perfiles_jv" not in st.session_state:
    st.session_state.intro_perfiles_jv = False
    st.session_state.perfiles_jv = False
    st.session_state.cursor_jv = 0

#if "lista_tarjetas" not in st.session_state:
#    st.session_state.lista_tarjetas = list(range(1,9))
#    st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
#    st.session_state.orden_tarjetas = [st.session_state.nro_tarjeta]

if "alt_A" not in st.session_state:
    alternativas = [1, 2]
    st.session_state.alt_A = choice(alternativas)
    alternativas.remove(st.session_state.alt_A)
    st.session_state.alt_B = alternativas[0]

if "elecciones_dict" not in st.session_state:
    st.session_state.elecciones_dict = {}

#if "encuestadores_dict" not in st.session_state:
#    encuestadores_df = pd.read_csv("encuestadores.csv", sep =";")
#    st.session_state.encuestadores_dict = be.generar_encuestadores_dict(encuestadores_df)

if "horas_list" not in st.session_state:
    st.session_state.horas_list = []

st.set_page_config(layout="centered")

# Imagen de fondo

background_url = "https://raw.githubusercontent.com/felixandro/PD_R5_CH_Q/refs/heads/master/fondo.png"
s.agregar_imagen_fondo(background_url)

# Identificación del Encuestador

if not st.session_state.id_encuestador:

    s.texto_con_fondo("Encuestador", upper_margin=0)

    id_encuestador = st.selectbox(
        "",
        [""] + ["x"]
    )

    if id_encuestador != "" :
        next_button_0 = st.button("Siguiente", use_container_width=True, type = "primary", key = "next_button_0")

        if next_button_0:
            st.session_state.id_encuestador = True
            st.session_state.id_encuestador_valor = id_encuestador
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            st.rerun()


# Características del Encuestado

if st.session_state.id_encuestador and not st.session_state.caracteristicas:

    s.texto_con_fondo(f"Encuestador: {st.session_state.id_encuestador_valor}", 
                    upper_margin="1rem",
                    bg_color="rgba(10, 20, 176, 0.95)",
                    text_color="#FFFFFF")
    
    s.texto_con_fondo("Tipo de Vehículo", upper_margin=0)

    tipo_veh = st.selectbox(
        "",
        ["", "Vehículo Liviano", "Camión Simple", "Camión Pesado"]
    )

    s.texto_con_fondo("Género", upper_margin=0)

    genero = st.selectbox(
        "",
        ["", "Femenino", "Masculino", "No Responde"]
    )

    s.texto_con_fondo("Edad", upper_margin=0)

    edad = st.number_input(
        "",
        min_value=14,
        max_value=100,
        value=None,
        step=1
    )

    s.texto_con_fondo("¿Cuál es el propósito de su viaje?", upper_margin=0)

    proposito = st.selectbox(
        "",
        ["", "Trabajo", "Estudio", "Otro"]
    )

    if tipo_veh != "" and genero != "" and edad  and proposito != "":

        next_button_1 = st.button("Siguiente", use_container_width=True, type = "primary", key = "next_button_1")

        if next_button_1:
            st.session_state.caracteristicas = True
            st.session_state.tipo_veh = tipo_veh
            st.session_state.genero = genero
            st.session_state.edad = edad
            st.session_state.proposito = proposito
            st.session_state.nro_disenho = s.definir_nro_disenho(tipo_veh)
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            st.session_state.nro_bloque = 1 if random() < 0.5 else 2
            st.session_state.lista_tarjetas = s.definir_lista_tarjetas(st.session_state.nro_disenho, st.session_state.nro_bloque)
            st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
            st.session_state.orden_tarjetas = [st.session_state.nro_tarjeta]
            st.rerun()

# Texto introductorio
if st.session_state.caracteristicas and not st.session_state.texto_introductorio:

    nro_disenho = st.session_state.nro_disenho
    with open(f'Disenhos/disenho_{nro_disenho}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]
    
    texto_introductorio1 = textwrap.dedent(f"""
        El tramo Chonchi - Quellón de la ruta 5, en el que se encuentra transitando hoy, actualmente posee **una pista por sentido y no cuenta con cobro de peaje**.
        
        En un **hipotético futuro**, el tramo podría pasar a tener **dos pistas por sentido**, lo cual aumentaría la velocidad de circulación, reduciendo así los tiempos de viaje. Sin embargo, esto implicaría la inclusión de una **plaza de peaje** que cobraría una cierta tarifa.
        
        En este sentido, el objetivo de la encuesta es medir su disposición a pagar por las eventuales diminuciones en los tiempos de viaje. Para esto le presentaremos cuadros comparativos entre la situación **actual** y un hipotético escenario **futuro** (Mostrar Cuadro).""")
    
    texto_introductorio2 = textwrap.dedent(f"""
        En cada cuadro, el costo y tiempo de viaje futuros irán cambiando. 

        Seleccione la **situación futura** cuando considere que estaría dispuesto a pagar el peaje por las reducciones en tiempo de viaje.
        
        En caso contrario, seleccione la **situación actual** cuando crea que las reducciones en tiempo de viaje no son suficientes y/o el peaje estaría por sobre lo que estaría dispuesto a pagar.
                                           
        Analice con detención e intente plasmar su disposición a pagar verdadera en cada una de las preguntas.""")


    s.texto_con_fondo(texto_introductorio1, upper_margin="1rem")

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]

    niveles_a_ejemplo = [altA_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"] 
    niveles_b_ejemplo = [altB_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"]
    
    s.perfil_eleccion(niveles_a_ejemplo, niveles_b_ejemplo)
    s.texto_con_fondo(texto_introductorio2, upper_margin="1rem")

    next_button_2 = st.button("Siguiente", use_container_width=True, type = "primary", key = "next_button_2")
    if next_button_2:
        st.session_state.texto_introductorio = True
        st.session_state.hora_id = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
        st.rerun()

# Perfiles de Elección

elif st.session_state.texto_introductorio and not st.session_state.perfiles:

    nro_disenho = st.session_state.nro_disenho
    with open(f'Disenhos/disenho_{nro_disenho}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]

    s.texto_con_fondo(f"Pregunta {len(st.session_state.orden_tarjetas)} - ¿Cuál Situación Prefiere?", upper_margin=0)

    niveles_a = [altA_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"]
    niveles_b = [altB_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"]
    s.perfil_eleccion(niveles_a, niveles_b)

    button_a = st.button(altA_label, use_container_width= True)
    button_b = st.button(altB_label, use_container_width= True)

    if button_a:
        s.texto_con_fondo(f"Seleccionó {altA_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altA_label
        
    if button_b:
        s.texto_con_fondo(f"Seleccionó {altB_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altB_label

    if  st.session_state.nro_tarjeta in st.session_state.elecciones_dict:
        next_button_3 = st.button("Siguiente", use_container_width=True, type = "primary", key = "next_button_3")

        if next_button_3:
            st.session_state.lista_tarjetas.remove( st.session_state.nro_tarjeta)
            hora_actual = time.strftime("%Y-%m-%d %H:%M:%S")
            # respuesta = {
            #             "id_encuestador": st.session_state.id_encuestador_valor,
            #             "lugar": st.session_state.lugar,
            #             "hora_id": st.session_state.hora_id,
            #             "genero": st.session_state.genero,
            #             "edad": st.session_state.edad,
            #             "proposito": st.session_state.proposito,
            #             "disenho": st.session_state.nro_disenho,
            #             "tarjeta": st.session_state.nro_tarjeta,
            #             "a1": data[f"alt{st.session_state.alt_A}"],
            #             "c_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][0],
            #             "tv_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][1],
            #             "te_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][2],
            #             "tc_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][3],
            #             "tr_a1": int(len(altA_label.split("-"))-1),
            #             "a2": data[f"alt{st.session_state.alt_B}"],
            #             "c_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][0],
            #             "tv_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][1],
            #             "te_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][2],
            #             "tc_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][3],
            #             "tr_a2": int(len(altB_label.split("-"))-1),
            #             "choice": st.session_state.elecciones_dict[st.session_state.nro_tarjeta],
            #             "fecha": hora_actual,
            #             "bloque": st.session_state.nro_bloque,
            #             "id_respuesta": be.generar_id_respuesta(
            #                 hora_id=st.session_state.hora_id,
            #                 nro_disenho=st.session_state.nro_disenho,
            #                 nro_tarjeta=st.session_state.nro_tarjeta,
            #                 id_encuestador=st.session_state.id_encuestador_valor,
            #                 edad=st.session_state.edad,
            #                 genero=st.session_state.genero,
            #                 proposito=st.session_state.proposito
            #             )
            #         }
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            #s.guardar_respuestas(respuesta)

            if len(st.session_state.elecciones_dict) <= 4:
                st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
                st.session_state.orden_tarjetas.append(st.session_state.nro_tarjeta)
                st.rerun()
            else:
                st.session_state.perfiles = True
                st.rerun()

                
    #st.divider()
    #st.write(f"Tarjeta seleccionada: {st.session_state.nro_tarjeta}")
    #st.write(f"Alternativa A: {st.session_state.alt_A} {altA_label}")
    #st.write(f"Alternativa B: {st.session_state.alt_B} {altB_label}")

    #st.write("Tus elecciones hasta ahora:")
    #st.write(st.session_state.elecciones_dict)
    #st.write("Orden de tarjetas seleccionadas:")
    #dst.write(st.session_state.orden_tarjetas)

if st.session_state.perfiles and not st.session_state.ingreso:

    s.texto_con_fondo("¿Cuántos vehículos posee en el hogar?", upper_margin=0)

    veh_hogar = st.selectbox(
        "",
        ["", "0", "1", "2 o más"]
    )

    s.texto_con_fondo("¿En qué rango se encuentra su ingreso familiar mensual?", upper_margin=0)

    ing_familiar = st.selectbox(
        "",
        ["", 
         "Menos de 500.000", 
         "Entre    500.001 y   750.000", 
         "Entre    750.001 y 1.000.000",
         "Entre  1.000.001 y 1.250.000",
         "Entre  1.250.001 y 1.500.000", 
         "Entre  1.500.001 y 1.750.000",
         "Entre  1.750.001 y 2.000.000",
         "Entre  2.000.001 y 2.250.000",
         "Entre  2.250.001 y 2.500.000",
         "Más de 2.500.000",
         "No Responde"]
    )

    if veh_hogar != "" and ing_familiar != "":
        next_button_4 = st.button("Siguiente", use_container_width=True, type = "primary", key = "next_button_4")

        if next_button_4:
            st.session_state.ingreso = True
            st.session_state.veh_hogar = veh_hogar
            st.session_state.ing_familiar = ing_familiar
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            assert len(st.session_state.horas_list) == 9

            # ingresos_respuesta = {
            #     "id_encuestador": st.session_state.id_encuestador_valor,
            #     "lugar": st.session_state.lugar,
            #     "hora_id": st.session_state.hora_id,
            #     "genero": st.session_state.genero,
            #     "edad": st.session_state.edad,
            #     "proposito": st.session_state.proposito,
            #     "veh_hogar": veh_hogar,
            #     "ingreso": ing_familiar,
            #     "nro_dis" : st.session_state.nro_disenho,
            #     "bloque": st.session_state.nro_bloque,
            #     "id_encuesta": s.generar_id_encuesta(
            #         hora_id=st.session_state.hora_id,
            #         nro_disenho=st.session_state.nro_disenho,
            #         id_encuestador=st.session_state.id_encuestador_valor,
            #         edad=st.session_state.edad,
            #         genero=st.session_state.genero,
            #         proposito=st.session_state.proposito
            #     )
            # }

            tiempos_respuesta = s.generar_tiempos_dict(st.session_state.horas_list)

            # total_dict = ingresos_respuesta | tiempos_respuesta

            # s.guardar_ingresos(total_dict)
            st.rerun()

if st.session_state.ingreso:

    s.texto_con_fondo("¡Encuesta Finalizada!", upper_margin="1rem")

    new_survey_button = st.button("Nueva Encuesta", use_container_width=True, type = "primary")

    if new_survey_button:
        id_encuestador = st.session_state.id_encuestador_valor

        st.session_state.clear()
        st.session_state.id_encuestador = True
        st.session_state.id_encuestador_valor = id_encuestador
        
        st.session_state.horas_list = []
        st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

        st.rerun()


    #st.write("Tus respuestas han sido guardadas exitosamente.")
    
    # Mostrar tabla de resultados
    #st.write("Resultados de la Encuesta:")
    
    # Crear DataFrame con las respuestas
    #df = pd.DataFrame(st.session_state.elecciones_dict.items(), columns=["Tarjeta", "Elección"])
    
    # Mostrar DataFrame como tabla
    #st.dataframe(df, use_container_width=True)

    # Mostrar información adicional
    #st.write(f"Vehículos en el hogar: {st.session_state.veh_hogar}")
    #st.write(f"Ingreso familiar mensual: {st.session_state.ing_familiar}")

