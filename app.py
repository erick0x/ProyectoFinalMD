import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from pymongo import MongoClient
import base64
import os

# ---------------------------------------------------------
# 1. CONEXIÓN A MONGO ATLAS
# ---------------------------------------------------------
client = MongoClient("mongodb+srv://erick:Xrer90lyyV80dN9a@cluster0.yux1ode.mongodb.net/")
db = client["ProyectoMD"]
coleccion_indicadores = db["indicadores"]
coleccion_resenas = db["reseñas"]

# Cargar datos de indicadores
data_indicadores = list(coleccion_indicadores.find({}, {"_id": 0}))
df_indicadores = pd.DataFrame(data_indicadores)

# Cargar TODAS las reseñas
data_resenas = list(coleccion_resenas.find())
df_resenas = pd.DataFrame(data_resenas)

pueblos = sorted(df_indicadores["Town"].unique())
primer_pueblo = pueblos[0]

print("✅ Conexión exitosa a MongoDB")
print(f"✅ {len(df_resenas)} reseñas cargadas")

# ---------------------------------------------------------
# 2. CARGAR LOGOS DESDE ASSETS
# ---------------------------------------------------------
def encode_img(path):
    try:
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except:
        return None

# Rutas para Render (usando rutas relativas)
turismo_src = encode_img("assets/turismo.png")
pueblos_src = encode_img("assets/pueblos.png")
estrellas_src = encode_img("assets/estrellas.png")

# ---------------------------------------------------------
# 3. URL DE IMÁGENES (mantener igual)
# ---------------------------------------------------------
url_imgs = {
    "Ajijic":"https://mexicorutamagica.mx/wp-content/uploads/2023/11/costa-ajijic-pueblo-magico-de-jalisco.jpg",
    "Atlixco":"https://twotravelturtles.com/wp-content/uploads/2024/03/PXL_20240322_1617352412-1.jpg",
    "Bacalar":"https://mexicancaribbean.travel/wp-content/uploads/2024/09/Bacalar-CenoteAzul_11zon-1-scaled.jpg",
    "Bernal":"https://www.de-paseo.com/queretaro/wp-content/uploads/2024/08/bernal-blog-turismo-100x667-destacad2024-640x480.jpg",
    "Chiapa_de_Corzo":"https://www.gob.mx/cms/uploads/article/main_image/84933/Can_o_n-del-Sumidero-web.jpg",
    "Cholula":"https://casaeva.travel/wp-content/uploads/2020/03/1.jpg",
    "Coatepec":"https://www.gob.mx/cms/uploads/article/main_image/85510/COATEPEC-KIOSKO-web.jpg",
    "Creel":"https://haciendadonarmando.com/wp-content/uploads/2024/08/RA5_9167-1280x853-1.jpg",
    "Cuatro_Cienegas":"https://upload.wikimedia.org/wikipedia/commons/5/50/Las_Playitas_Cuatrocienegas_2.jpg",
    "Cuetzalan":"https://escapadas.mexicodesconocido.com.mx/wp-content/uploads/2020/10/Quetzalan_Iglesia-de-los-Jarritos_MF_ok-scaled-1-e1614282751581.jpg",
    "Dolores_Hidalgo":"https://mexitours.travel/wp-content/uploads/2024/02/Dolores-Hidalgo-1-1024x765.jpg",
    "Huasca_de_Ocampo":"https://www.gob.mx/cms/uploads/image/file/515923/Hda-Santa-Maria-Regla-Huasca-web.jpg",
    "Isla_Mujeres":"https://upload.wikimedia.org/wikipedia/commons/e/e7/Isla_Mujeres_aerial_%2829729604048%29.jpg",
    "Ixtapan_de_la_Sal":"https://www.gob.mx/cms/uploads/image/file/533308/Estado-de-Mexico_Ixtapan-de-la-sal-web.jpg",
    "Izamal":"https://www.yucatan.gob.mx/docs/galerias/izamal/2.jpg",
    "Loreto":"https://cdn.myuvci.com/uploads/destination/mainImage/5/24-08-UVCI-LTO-BLOG-WEB.jpg",
    "Malinalco":"https://www.mexicodesconocido.com.mx/wp-content/uploads/2025/08/EdomexTurismo_1200-900x600.jpg",
    "Mazunte":"https://www.excelsior.com.mx/media/inside-the-note/pictures/2025/03/31/mazunte-oaxaca-pueblo-magico_0.jpg",
    "Metepec":"https://edomex.quadratin.com.mx/www/wp-content/uploads/2025/09/Desbanca-Metepec-a-Valle-de-Bravo-como-el-Pueblo-Magico-favorito--1160x700.jpg",
    "Orizaba":"https://media-cdn.tripadvisor.com/media/attractions-splice-spp-674x446/0d/0d/92/d2.jpg",
    "Palenque":"https://www.worldhistory.org/img/r/p/1500x1500/3097.jpg",
    "Parras":"https://pueblosmagicos.mexicodesconocido.com.mx/wp-content/uploads/2023/09/IMG4922_coahuila_parras_vino_don_leo_vinedo_vinedos_botellas_barril_AM.jpg",
    "Patzcuaro":"https://upload.wikimedia.org/wikipedia/commons/0/04/Patzcuaro-church.jpg",
    "Real_de_Catorce":"https://upload.wikimedia.org/wikipedia/commons/1/14/Panor%C3%A1mica_de_Real_de_Catorce.jpg",
    "San_Cristobal_de_las_Casas":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/San_Crist%C3%B3bal_de_Las_Casas_18.jpg/1200px-San_Crist%C3%B3bal_de_Las_Casas_18.jpg",
    "Sayulita":"https://sayulitabeach.com/site/wp-content/uploads/slideshow-gallery/sayulitatown-1_mini.jpg",
    "Tapalpa":"https://www.caminoreal.com/storage/app/uploads/public/66f/b90/6ca/66fb906ca503a038754258.jpg",
    "Taxco":"https://www.gob.mx/cms/uploads/article/main_image/83002/PANORAMICA-DE-TAXCO-web.jpg",
    "Teotihuacan":"https://lugares.inah.gob.mx/sites/default/files/zonas/382_A_arqueologia_2.jpg",
    "Tepotzotlan":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Aqueduct_Arcos_del_Sitio.jpg/330px-Aqueduct_Arcos_del_Sitio.jpg",
    "Tepoztlan":"https://media.admagazine.com/photos/618a6050b67f79aa891ed801/master/w_1600%2Cc_limit/89805.jpg",
    "Tequila":"https://escapadas.mexicodesconocido.com.mx/wp-content/uploads/2020/10/MD436_Viaje-Tequila-BI_ok-1.jpg",
    "Tequisquiapan":"https://www.entornoturistico.com/wp-content/uploads/2021/08/Centro-de-Tequisquiapan.jpg",
    "Tlaquepaque":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Tlaquepaque%2C_Jalisco%2C_Mexico%2C_2021_-_101.jpg/1200px-Tlaquepaque%2C_Jalisco%2C_Mexico%2C_2021_-_101.jpg",
    "TodosSantos":"https://nomanbefore.com/wp-content/uploads/2020/01/Todos_Santos-3209.jpg",
    "Tulum":"https://media.tacdn.com/media/attractions-splice-spp-674x446/06/75/bc/3d.jpg",
    "Valladolid":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Valladolid_iglesia_2.jpg/1200px-Valladolid_iglesia_2.jpg",
    "Valle_de_Bravo":"https://images.squarespace-cdn.com/content/v1/5eacfbcb226dc82fa32ebc80/53523f43-a0d5-4f19-b0a3-f175aa82a385/Plaza-de-la-Independencia-Valle-de-Bravo-Pueblo-Magico-cerca-de-CDMX.jpg",
    "Xilitla":"https://www.nomadictravelscapes.com/wp-content/uploads/2022/10/Hotel-Tapasoli-xilitla-las-pozas.jpg",
    "Zacatlan":"https://www.excelsior.com.mx/media/pictures/2025/04/15/3291402.jpg"
}

# ---------------------------------------------------------
# 4. COORDENADAS (mantener igual)
# ---------------------------------------------------------
coords = {
    "Ajijic": (20.2986, -103.2565),
    "Atlixco": (18.9085, -98.4317),
    "Bacalar": (18.6737, -88.3923),
    "Bernal": (20.7433, -99.9494),
    "Chiapa_de_Corzo": (16.7079, -93.0167),
    "Cholula": (19.0640, -98.3030),
    "Coatepec": (19.4513, -96.9617),
    "Creel": (27.7511, -107.6399),
    "Cuatro_Cienegas": (26.9860, -102.0570),
    "Cuetzalan": (20.0194, -97.5222),
    "Dolores_Hidalgo": (21.1561, -100.9340),
    "Huasca_de_Ocampo": (20.1964, -98.5753),
    "Isla_Mujeres": (21.2325, -86.7310),
    "Ixtapan_de_la_Sal": (18.8437, -99.6765),
    "Izamal": (20.9230, -89.0187),
    "Loreto": (26.0120, -111.3417),
    "Malinalco": (18.9580, -99.4960),
    "Mazunte": (15.6641, -96.5570),
    "Metepec": (19.2570, -99.6070),
    "Orizaba": (18.8510, -97.1000),
    "Palenque": (17.5090, -91.9830),
    "Parras": (25.4410, -102.1780),
    "Patzcuaro": (19.5144, -101.6090),
    "Real_de_Catorce": (23.6915, -101.0190),
    "San_Cristobal_de_las_Casas": (16.7370, -92.6376),
    "Sayulita": (20.8680, -105.4400),
    "Tapalpa": (19.9510, -103.7590),
    "Taxco": (18.5560, -99.6050),
    "Teotihuacan": (19.6925, -98.8439),
    "Tepotzotlan": (19.7139, -99.2216),
    "Tepoztlan": (18.9868, -99.0981),
    "Tequila": (20.8826, -103.8350),
    "Tequisquiapan": (20.5210, -99.8910),
    "Tlaquepaque": (20.6405, -103.2930),
    "TodosSantos": (23.4467, -110.2265),
    "Tulum": (20.2114, -87.4654),
    "Valladolid": (20.6894, -88.2013),
    "Valle_de_Bravo": (19.1950, -100.1330),
    "Xilitla": (21.3926, -98.9947),
    "Zacatlan": (19.9332, -97.9611)
}

# ---------------------------------------------------------
# 5. FUNCIONES PARA GRÁFICAS DE INDICADORES
# ---------------------------------------------------------
def crear_grafica_seguridad():
    """Gráfica 1: Pueblos con mayor percepción de seguridad"""
    seguridad_df = df_indicadores.nlargest(10, 'Percepcion_Seguridad')[['Town', 'Percepcion_Seguridad']]
    
    fig = px.bar(
        seguridad_df,
        x='Percepcion_Seguridad',
        y='Town',
        orientation='h',
        title="Top 10 Pueblos con Mayor Percepción de Seguridad",
        labels={'Percepcion_Seguridad': 'Puntuación de Seguridad', 'Town': 'Pueblo Mágico'},
        color_discrete_sequence=['#27ae60'] * len(seguridad_df)
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

def crear_grafica_hotelera():
    """Gráfica 2: Mejor satisfacción hotelera"""
    hotelera_df = df_indicadores.nlargest(10, 'Satisfaccion_Hotelera')[['Town', 'Satisfaccion_Hotelera']]
    
    fig = px.bar(
        hotelera_df,
        x='Satisfaccion_Hotelera',
        y='Town',
        orientation='h',
        title="Top 10 Pueblos con Mejor Satisfacción Hotelera",
        labels={'Satisfaccion_Hotelera': 'Puntuación Hotelera', 'Town': 'Pueblo Mágico'},
        color_discrete_sequence=['#2980b9'] * len(hotelera_df)
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

def crear_grafica_restaurantes():
    """Gráfica 3: Mejor satisfacción de restaurantes"""
    restaurantes_df = df_indicadores.nlargest(10, 'Satisfaccion_Restaurantes')[['Town', 'Satisfaccion_Restaurantes']]
    
    fig = px.bar(
        restaurantes_df,
        x='Satisfaccion_Restaurantes',
        y='Town',
        orientation='h',
        title="Top 10 Pueblos con Mejor Satisfacción de Restaurantes",
        labels={'Satisfaccion_Restaurantes': 'Puntuación Restaurantes', 'Town': 'Pueblo Mágico'},
        color_discrete_sequence=['#e74c3c'] * len(restaurantes_df)
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

def crear_grafica_resenas_por_pueblo():
    """Gráfica 4: Número de reseñas por pueblo"""
    pueblo_counts = df_resenas['Town'].value_counts().head(10)
    
    fig = px.bar(
        x=pueblo_counts.values,
        y=pueblo_counts.index,
        orientation='h',
        title="Top 10 Pueblos con Más Reseñas",
        labels={'x': 'Número de Reseñas', 'y': 'Pueblo Mágico'},
        color_discrete_sequence=['#8e44ad'] * len(pueblo_counts)
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

def crear_grafica_resenas_por_region():
    """Gráfica 5: Número de reseñas por región"""
    region_counts = df_resenas['Region'].value_counts().head(8)
    
    fig = px.bar(
        x=region_counts.index,
        y=region_counts.values,
        title="Top 8 Regiones con Más Reseñas",
        labels={'x': 'Región', 'y': 'Número de Reseñas'},
        color_discrete_sequence=['#f39c12'] * len(region_counts)
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        xaxis_tickangle=45,
        showlegend=False
    )
    return fig

def crear_grafica_tipos_establecimiento():
    """Gráfica 6: Distribución por tipo de establecimiento"""
    tipo_counts = df_resenas['Type'].value_counts()
    
    fig = px.pie(
        values=tipo_counts.values,
        names=tipo_counts.index,
        title="Distribución por Tipo de Establecimiento",
        hole=0.4,
        color_discrete_sequence=['#6D48E7', '#E67E22', '#27ae60']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=True
    )
    return fig

# ---------------------------------------------------------
# 6. FUNCIÓN PARA OBTENER RESEÑAS DEL PUEBLO SELECCIONADO
# ---------------------------------------------------------
def obtener_resenas_pueblo(pueblo):
    """Obtiene las primeras 10 reseñas del pueblo seleccionado"""
    reseñas_pueblo = df_resenas[df_resenas['Town'] == pueblo].head(10)
    
    # Seleccionar y renombrar columnas específicas
    columnas_mostrar = ['Title', 'Review', 'Polarity', 'Type', 'sentimiento_5']
    nombres_columnas = ['Título', 'Reseña', 'Calificación', 'Tipo', 'Score Sentimiento']
    
    if not reseñas_pueblo.empty:
        reseñas_filtradas = reseñas_pueblo[columnas_mostrar].copy()
        reseñas_filtradas.columns = nombres_columnas
        
        # Formatear columnas
        reseñas_filtradas['Score Sentimiento'] = reseñas_filtradas['Score Sentimiento'].round(4)
        reseñas_filtradas['Calificación'] = reseñas_filtradas['Calificación'].astype(int)
        
        return reseñas_filtradas
    else:
        return pd.DataFrame(columns=nombres_columnas)

# ---------------------------------------------------------
# 7. INDICADORES
# ---------------------------------------------------------
def obtener_indicadores(pueblo):
    row = df_indicadores[df_indicadores["Town"] == pueblo].iloc[0]
    return {
        "Hotelera": row["Satisfaccion_Hotelera"],
        "Restaurantes": row["Satisfaccion_Restaurantes"],
        "General": row["Satisfaccion_General_AtractivoTuristico"],
        "Seguridad": row["Percepcion_Seguridad"],
        "Clima": row["Percepcion_Clima"]
    }

# ---------------------------------------------------------
# 8. MAPA
# ---------------------------------------------------------
def mapa_mexico(pueblo_actual):
    df_map = pd.DataFrame([
        {"pueblo": p, "lat": coords[p][0], "lon": coords[p][1]}
        for p in coords
    ])

    df_map["selected"] = df_map["pueblo"] == pueblo_actual

    fig = px.scatter_map(
        df_map,
        lat="lat",
        lon="lon",
        hover_name="pueblo",
        color=df_map["selected"].map({True: "Seleccionado", False: "Otros"}),
        color_discrete_map={"Otros": "blue", "Seleccionado": "red"},
        size=df_map["selected"].map({True: 12, False: 6}),
        zoom=4,
        height=500,
        map_style="open-street-map"
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

# ---------------------------------------------------------
# 9. APP
# ---------------------------------------------------------
app = dash.Dash(__name__)
app.title = "Dashboard Pueblos Mágicos"

# Configuración del servidor para Render
server = app.server

app.layout = html.Div([

    # ---------------- HEADER ----------------
    html.Div([
        html.Img(src=turismo_src, style={
            "height": "70px", "objectFit": "contain"
        }),
        html.H1("Indicadores de Satisfacción – Pueblos Mágicos",
                style={
                    "flex": "1",
                    "textAlign": "center",
                    "color": "#2c3e50",
                    "fontWeight": "700",
                    "fontSize": "2rem"
                }),
        html.Img(src=pueblos_src, style={
            "height": "70px", "objectFit": "contain"
        }),
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "padding": "10px 40px",
        "borderBottom": "3px solid #6D48E7",
        "backgroundColor": "#f9f9fc"
    }),

    # ---------------- SELECTOR + ESTRELLAS ----------------
    html.Div([

        html.Label("Seleccione un Pueblo Mágico:",
                   style={"fontSize": "20px", "marginRight": "15px"}),

        dcc.Dropdown(
            id="pueblo-dropdown",
            options=[{"label": p, "value": p} for p in pueblos],
            value=primer_pueblo,
            clearable=False,
            style={"width": "300px"}
        ),

        html.Img(src=estrellas_src,
                 style={"height": "45px", "marginLeft": "20px"})
    ], style={
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "marginTop": "20px",
        "gap": "15px"
    }),

    # ---------------- HIGHLIGHTS ----------------
    html.Div(id="highlights-container", style={
        "display": "flex",
        "justifyContent": "space-around",
        "margin": "30px 0"
    }),

    # ---------------- IMAGEN + MAPA ----------------
    html.Div([
        html.Div(id="imagen-pueblo-container",
                 style={"width": "32%", "textAlign": "center"}),

        html.Div(dcc.Graph(id="mapa-mexico"),
                 style={"width": "66%"})
    ], style={
        "display": "flex",
        "justifyContent": "space-between",
        "marginTop": "20px"
    }),

    # ---------------- NUEVAS GRÁFICAS DE INDICADORES ----------------
    html.Div([
        html.H2("Análisis de Indicadores y Reseñas", 
                style={"textAlign": "center", "margin": "40px 0 20px 0", "color": "#2c3e50"})
    ]),

    # Primera fila de gráficas (3 gráficas)
    html.Div([
        html.Div([
            dcc.Graph(figure=crear_grafica_seguridad())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"}),
        
        html.Div([
            dcc.Graph(figure=crear_grafica_hotelera())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"}),
        
        html.Div([
            dcc.Graph(figure=crear_grafica_restaurantes())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"})
    ], style={"display": "flex", "justifyContent": "space-between"}),

    # Segunda fila de gráficas (3 gráficas)
    html.Div([
        html.Div([
            dcc.Graph(figure=crear_grafica_resenas_por_pueblo())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"}),
        
        html.Div([
            dcc.Graph(figure=crear_grafica_resenas_por_region())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"}),
        
        html.Div([
            dcc.Graph(figure=crear_grafica_tipos_establecimiento())
        ], style={"width": "32%", "display": "inline-block", "padding": "10px"})
    ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "40px"}),

    # ---------------- TABLA DE RESEÑAS DEL PUEBLO SELECCIONADO ----------------
    html.Div([
        html.H2("Últimas Reseñas del Pueblo Seleccionado", 
                style={"textAlign": "center", "margin": "40px 0 20px 0", "color": "#2c3e50"}),
        
        html.Div(id="tabla-resenas-container",
                 style={"margin": "20px", "padding": "20px", "backgroundColor": "white", "borderRadius": "10px"})
    ])
])

# ---------------------------------------------------------
# 10. CALLBACKS
# ---------------------------------------------------------
@app.callback(
    Output("imagen-pueblo-container", "children"),
    Input("pueblo-dropdown", "value")
)
def actualizar_imagen(pueblo):
    url = url_imgs.get(pueblo)
    if url:
        return html.Img(src=url, style={
            "width": "100%",
            "height": "500px",
            "objectFit": "cover",
            "borderRadius": "15px",
            "boxShadow": "0px 2px 8px rgba(0,0,0,0.2)"
        })
    return html.P("Imagen no disponible.",
                  style={"textAlign": "center", "fontSize": "18px"})

@app.callback(
    Output("mapa-mexico", "figure"),
    Input("pueblo-dropdown", "value")
)
def actualizar_mapa(pueblo):
    return mapa_mexico(pueblo)

@app.callback(
    Output("highlights-container", "children"),
    Input("pueblo-dropdown", "value")
)
def actualizar_highlights(pueblo):
    ind = obtener_indicadores(pueblo)

    def carta(titulo, valor, color):
        return html.Div([
            html.H4(titulo, style={"color": color}),
            html.P(f"{valor:.2f}", style={"fontSize": "26px", "fontWeight": "bold"})
        ], style={
            "width": "18%",
            "padding": "15px",
            "background": "#fff",
            "border": f"2px solid {color}",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
        })

    return [
        carta("Hotelera", ind["Hotelera"], "#6D48E7"),
        carta("Restaurantes", ind["Restaurantes"], "#E67E22"),
        carta("Atractivo Turístico", ind["General"], "#2980b9"),
        carta("Seguridad", ind["Seguridad"], "#27ae60"),
        carta("Clima", ind["Clima"], "#8e44ad"),
    ]

@app.callback(
    Output("tabla-resenas-container", "children"),
    Input("pueblo-dropdown", "value")
)
def actualizar_tabla_resenas(pueblo):
    reseñas_df = obtener_resenas_pueblo(pueblo)
    
    if not reseñas_df.empty:
        return dash_table.DataTable(
            data=reseñas_df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in reseñas_df.columns],
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial',
                'fontSize': '14px',
                'border': '1px solid #ddd'
            },
            style_header={
                'backgroundColor': '#6D48E7',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9fc'
                }
            ],
            page_size=10,
            style_table={
                'overflowX': 'auto',
                'borderRadius': '10px',
                'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'
            }
        )
    else:
        return html.P("No hay reseñas disponibles para este pueblo mágico.",
                     style={"textAlign": "center", "fontSize": "18px", "color": "#7f8c8d"})

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))

