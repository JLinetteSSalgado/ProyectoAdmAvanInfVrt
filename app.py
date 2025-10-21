# Importamos las herramientas necesarias de Flask
from flask import Flask, render_template, request

# Inicializa la aplicación Flask
app = Flask(__name__)

# --- DICCIONARIO DE CATEGORÍAS ---
# Mapea nombre de categoría -> (Título, Archivo HTML)
CATEGORIES = {
    'frutas': ('Frutas Frescas', 'frutas.html'),
    'verduras': ('Verduras Frescas', 'verduras.html'),
    'deportes': ('Deportes', 'deportes.html'),
    'tecnologia': ('Tecnología', 'tecnologia.html'),
    'higiene': ('Higiene y Cuidado Personal', 'higiene.html'), # Asumiendo que farmacia e higiene están juntas o usa este
    'vinos': ('Vinos y Licores', 'vinos.html'),
    'carnes': ('Carnes, Pescados y Mariscos', 'carnes.html'),
    'lacteos': ('Lácteos y Huevos', 'lacteos.html'),
    'abarrotes': ('Abarrotes', 'abarrotes.html'),
    'cocina': ('Cocina y Hogar', 'cocina.html'),
    'mascotas': ('Mascotas', 'mascotas.html'),
    'farmacia': ('Farmacia', 'farmacia.html'), # O tal vez 'higiene.html'? Ajusta según tu archivo
    'belleza': ('Belleza', 'belleza.html'),
    'videojuegos': ('Videojuegos', 'videojuegos.html')
}

# --- LISTA DE TODOS LOS PRODUCTOS PARA BÚSQUEDA ---
# ¡IMPORTANTE! Debes completar esta lista con TODOS los productos
# de TODOS tus archivos HTML (frutas, verduras, carnes, etc.)
# Asegúrate de que 'id', 'name', 'price', y 'image' sean correctos.
ALL_PRODUCTS = [
    # Frutas
    {'id': 'f-01', 'name': 'Coco', 'price': 25.00, 'image': 'images/frutas/Coco.png'},
    {'id': 'f-02', 'name': 'Durazno', 'price': 10.00, 'image': 'images/frutas/Durazno.png'},
    {'id': 'f-03', 'name': 'Fresa', 'price': 8.00, 'image': 'images/frutas/fresa.png'},
    {'id': 'f-04', 'name': 'Kiwi', 'price': 12.00, 'image': 'images/frutas/Kiwi.png'},
    {'id': 'f-05', 'name': 'Lechuga', 'price': 18.00, 'image': 'images/frutas/lechuga.jpg'}, # Nota: imagen es .jpg
    {'id': 'f-06', 'name': 'Mango', 'price': 15.00, 'image': 'images/frutas/mango.png'},
    {'id': 'f-07', 'name': 'Manzana', 'price': 9.00, 'image': 'images/frutas/manzana.jpg'}, # Nota: imagen es .jpg
    {'id': 'f-08', 'name': 'Naranja', 'price': 6.00, 'image': 'images/frutas/Naranja.png'},
    {'id': 'f-09', 'name': 'Piña', 'price': 35.00, 'image': 'images/frutas/Piña.jpg'}, # Nota: imagen es .jpg
    {'id': 'f-10', 'name': 'Plátano', 'price': 5.00, 'image': 'images/frutas/platano.png'},
    # Verduras
    {'id': 'v-01', 'name': 'Brócoli', 'price': 25.00, 'image': 'images/verduras/Brocoli.png'},
    {'id': 'v-02', 'name': 'Cebolla Blanca', 'price': 10.00, 'image': 'images/verduras/CebollaBlanca.png'},
    {'id': 'v-03', 'name': 'Cebolla Morada', 'price': 12.00, 'image': 'images/verduras/CebollaMorada.png'},
    {'id': 'v-04', 'name': 'Champiñones', 'price': 18.00, 'image': 'images/verduras/Champiñones.png'},
    {'id': 'v-05', 'name': 'Chile de Árbol', 'price': 6.00, 'image': 'images/verduras/ChileArbol.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-06', 'name': 'Elote', 'price': 8.00, 'image': 'images/verduras/Elote.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-07', 'name': 'Papa', 'price': 9.00, 'image': 'images/verduras/papa.png'},
    {'id': 'v-08', 'name': 'Tomate Rojo', 'price': 7.00, 'image': 'images/verduras/Tomate Rojo.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-09', 'name': 'Tomate Verde', 'price': 6.50, 'image': 'images/verduras/TomateVerde.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-10', 'name': 'Zanahoria', 'price': 5.00, 'image': 'images/verduras/Zanahoria.png'},
    # Deportes
    {'id': 'dpt-01', 'name': 'Balón de Fútbol No. 5', 'price': 349.00, 'image': 'images/deportes/balon.png'},
    {'id': 'dpt-02', 'name': 'Balón de Americano', 'price': 420.00, 'image': 'images/deportes/balonamericano.png'},
    {'id': 'dpt-03', 'name': 'Banco Press', 'price': 1899.00, 'image': 'images/deportes/BancoPres.png'},
    {'id': 'dpt-04', 'name': 'Guantes Portero Futbol', 'price': 299.00, 'image': 'images/deportes/guantesFurbol.png'}, # Nombre corregido
    {'id': 'dpt-05', 'name': 'Juego de Pesas 20kg', 'price': 999.00, 'image': 'images/deportes/JuegoPesas.png'}, # Nombre corregido
    {'id': 'dpt-06', 'name': 'Ligas de Ejercicio', 'price': 250.00, 'image': 'images/deportes/LigasEjercicio.png'},
    {'id': 'dpt-07', 'name': 'Pelota Grande Yoga', 'price': 320.00, 'image': 'images/deportes/PelotaGrande.png'}, # Nombre corregido
    {'id': 'dpt-08', 'name': 'Raqueta de Tenis', 'price': 750.00, 'image': 'images/deportes/RaquetaTenis.png'},
    # Tecnologia
    {'id': 't-01', 'name': 'Audífonos Bluetooth', 'price': 299.00, 'image': 'images/tecnologias/AudifonosBluetooth.png'},
    {'id': 't-02', 'name': 'Bocina Bluetooth', 'price': 450.00, 'image': 'images/tecnologias/BocinaBluetooth.png'},
    {'id': 't-03', 'name': 'Cargador USB', 'price': 120.00, 'image': 'images/tecnologias/CargadorUSB.png'},
    {'id': 't-04', 'name': 'Disco Duro Externo', 'price': 950.00, 'image': 'images/tecnologias/DiscoDuroExterno.jpg'}, # Nota: imagen es .jpg
    {'id': 't-05', 'name': 'Laptop HP', 'price': 9500.00, 'image': 'images/tecnologias/LaptopHP.png'},
    {'id': 't-06', 'name': 'Memoria USB', 'price': 85.00, 'image': 'images/tecnologias/MemoriaUSB.png'},
    {'id': 't-07', 'name': 'Monitor Samsung', 'price': 2200.00, 'image': 'images/tecnologias/MonitorSamsung.png'},
    {'id': 't-08', 'name': 'Mouse Inalámbrico', 'price': 180.00, 'image': 'images/tecnologias/MouseInalambrico.png'},
    {'id': 't-09', 'name': 'Smartwatch', 'price': 699.00, 'image': 'images/tecnologias/Smartwatch.png'},
    {'id': 't-10', 'name': 'Teclado Mecánico', 'price': 350.00, 'image': 'images/tecnologias/TecladoMecanico.png'},
    # Vinos
    {'id': 'v-01', 'name': 'Alcohol Azul', 'price': 95.00, 'image': 'images/vinos/AlcoholAzulpng.png'},
    {'id': 'v-02', 'name': 'Alcohol Rojo', 'price': 90.00, 'image': 'images/vinos/AlcoholRojo.png'},
    {'id': 'v-03', 'name': 'Bacardi', 'price': 280.00, 'image': 'images/vinos/Bacardi.png'},
    {'id': 'v-04', 'name': 'Blue Label', 'price': 1650.00, 'image': 'images/vinos/blueLabel.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-05', 'name': 'Carta Blanca', 'price': 50.00, 'image': 'images/vinos/CartaBlancajpg.jpg'}, # Nota: imagen es .jpg
    {'id': 'v-06', 'name': 'José Cuervo', 'price': 320.00, 'image': 'images/vinos/JoseCuervo.png'},
    {'id': 'v-07', 'name': 'Oso Negro', 'price': 180.00, 'image': 'images/vinos/OsoNegrol.png'},
    {'id': 'v-08', 'name': 'Red Label', 'price': 950.00, 'image': 'images/vinos/RedLabel.png'},
    {'id': 'v-09', 'name': 'Tonayán', 'price': 45.00, 'image': 'images/vinos/Tonayan.png'},
    {'id': 'v-10', 'name': 'Victoria Media', 'price': 55.00, 'image': 'images/vinos/VictoriaMedia.png'},
    # Cocina
    {'id': 'co-01', 'name': 'Bowls', 'price': 93.73, 'image': 'images/cocina/bowls.jpg'},
    {'id': 'co-02', 'name': 'Cuchillo', 'price': 121.90, 'image': 'images/cocina/cuchillo.jpg'},
    {'id': 'co-03', 'name': 'Espatula', 'price': 21.25, 'image': 'images/cocina/espatula.jpg'},
    {'id': 'co-04', 'name': 'Licuadora', 'price': 35.05, 'image': 'images/cocina/licuadora.jpg'},
    {'id': 'co-05', 'name': 'Olla', 'price': 33.76, 'image': 'images/cocina/olla.jpg'},
    {'id': 'co-06', 'name': 'Pelador', 'price': 193.23, 'image': 'images/cocina/pelador.jpg'},
    {'id': 'co-07', 'name': 'Sarten', 'price': 139.38, 'image': 'images/cocina/sarten.jpg'},
    {'id': 'co-08', 'name': 'Tablapicar', 'price': 100.35, 'image': 'images/cocina/tablapicar.jpg'},
    {'id': 'co-09', 'name': 'Tazas', 'price': 94.59, 'image': 'images/cocina/tazas.jpg'},
    {'id': 'co-10', 'name': 'Tostador', 'price': 176.51, 'image': 'images/cocina/tostador.jpg'},
    {'id': 'co-11', 'name': 'Utensilios', 'price': 64.75, 'image': 'images/cocina/utensilios.jpg'},
    # Belleza
    {'id': 'be-01', 'name': 'Basemaquillaje', 'price': 120.43, 'image': 'images/belleza/basemaquillaje.jpg'},
    {'id': 'be-02', 'name': 'Contorno', 'price': 164.64, 'image': 'images/belleza/contorno.jpg'},
    {'id': 'be-03', 'name': 'Gloss', 'price': 50.95, 'image': 'images/belleza/gloss.jpg'},
    {'id': 'be-04', 'name': 'Iluminador', 'price': 103.91, 'image': 'images/belleza/iluminador.jpg'},
    {'id': 'be-05', 'name': 'Labial', 'price': 186.88, 'image': 'images/belleza/labial.jpg'},
    {'id': 'be-06', 'name': 'Paleta', 'price': 158.39, 'image': 'images/belleza/paleta.jpg'},
    {'id': 'be-07', 'name': 'Polvocompacto', 'price': 168.22, 'image': 'images/belleza/polvocompacto.jpg'},
    {'id': 'be-08', 'name': 'Polvotranslucido', 'price': 175.07, 'image': 'images/belleza/polvotranslucido.jpg'},
    {'id': 'be-09', 'name': 'Rimel', 'price': 43.02, 'image': 'images/belleza/rimel.jpg'},
    {'id': 'be-10', 'name': 'Rubor', 'price': 122.62, 'image': 'images/belleza/rubor.jpg'},
    # Farmacia
    {'id': 'fa-01', 'name': 'Analgésico CafiAspirina', 'price': 155.00, 'image': 'images/farmacia/Analgésicos.jpg'},
    {'id': 'fa-02', 'name': 'Jarabe VICK 44', 'price': 98.50, 'image': 'images/farmacia/jarabetos.jpg'},
    {'id': 'fa-03', 'name': 'Agua Oxigenada JALOMA', 'price': 35.00, 'image': 'images/farmacia/AguaOxigenada.jpg'},
    {'id': 'fa-04', 'name': 'Venda Elástica Quirurgical', 'price': 45.99, 'image': 'images/farmacia/vendas.jpg'},
    {'id': 'fa-05', 'name': 'Cepillo Dental Colgate 360°', 'price': 79.90, 'image': 'images/farmacia/cepillodientes.jgp.jpg'}, # Cuidado con la extensión
    {'id': 'fa-06', 'name': 'Pasta Dental Fluorada', 'price': 42.50, 'image': 'images/farmacia/pastadientes.jpg'},
    {'id': 'fa-07', 'name': 'Hilo Dental G·U·M', 'price': 65.00, 'image': 'images/farmacia/hilodental.jpg'},
    {'id': 'fa-08', 'name': 'Protector Solar Avène SPF 50+', 'price': 499.00, 'image': 'images/farmacia/protectorsolar.jpg'},
    {'id': 'fa-09', 'name': 'Crema Hidratante Neutrogena', 'price': 230.75, 'image': 'images/farmacia/cremahidratante.jpg'},
    {'id': 'fa-10', 'name': 'Suplemento Proteína WHEY', 'price': 899.90, 'image': 'images/farmacia/Suplementos.jpg'},
    # Mascotas
    {'id': 'm-01', 'name': 'Torre Rascadora Multi-Nivel', 'price': 950.00, 'image': 'images/mascotas/casagatos.jpg'},
    {'id': 'm-02', 'name': 'Cama Cueva Afelpada', 'price': 280.00, 'image': 'images/mascotas/camagato.jpg'},
    {'id': 'm-03', 'name': 'Cepillo Doble Púas y Cerdas', 'price': 85.00, 'image': 'images/mascotas/cepillo.jpg'},
    {'id': 'm-04', 'name': 'Correa Retráctil Extensible', 'price': 150.00, 'image': 'images/mascotas/correa.jpg'},
    {'id': 'm-05', 'name': 'NUPEC Croquetas Senior Razas Pequeñas', 'price': 390.00, 'image': 'images/mascotas/croquetas.jpg'},
    {'id': 'm-06', 'name': 'Shampoo FANCY PETS Essentials Gato', 'price': 75.00, 'image': 'images/mascotas/shampogato.jpg'},
    {'id': 'm-07', 'name': 'Rascador de Cartón Reforzado', 'price': 190.00, 'image': 'images/mascotas/rascadorgatos.jpg'},
    {'id': 'm-08', 'name': 'Comedero Doble Elevado Acero Inoxidable', 'price': 310.00, 'image': 'images/mascotas/comedorperro.jpg'},
    {'id': 'm-09', 'name': 'Transportadora Rígida Talla Mediana', 'price': 650.00, 'image': 'images/mascotas/transportadora.jpg'},
    {'id': 'm-10', 'name': 'Jaula Grande para Aves con Ruedas', 'price': 1800.00, 'image': 'images/mascotas/jaulapajaro.jpg'},

    # Videojuegos (Basado en nuevos nombres de archivo)
    {'id': 'vg-01', 'name': 'Audífonos Gamer', 'price': 750.00, 'image': 'images/videojuegos/AudifonosGamer.png'},
    {'id': 'vg-02', 'name': 'Consola PlayStation 5', 'price': 12500.00, 'image': 'images/videojuegos/ConsolaPlayStation5.png'},
    {'id': 'vg-03', 'name': 'Control DualSense (PS5)', 'price': 1599.00, 'image': 'images/videojuegos/ControlDualSense.png'},
    {'id': 'vg-04', 'name': 'Control Xbox Wireless', 'price': 1399.00, 'image': 'images/videojuegos/ControlXboxWireless.jpg'}, # Nota: .jpg
    {'id': 'vg-05', 'name': 'Halo Infinite', 'price': 1199.00, 'image': 'images/videojuegos/HaloInfinite.jpg'}, # Nota: .jpg
    {'id': 'vg-06', 'name': 'Mouse Gamer RGB', 'price': 450.00, 'image': 'images/videojuegos/MouseGamerRGB.png'},
    {'id': 'vg-07', 'name': 'Nintendo Switch OLED', 'price': 7499.00, 'image': 'images/videojuegos/NintendoSwitchOLED.png'},
    {'id': 'vg-08', 'name': 'Silla Gamer', 'price': 3200.00, 'image': 'images/videojuegos/SillaGamer.png'},
    {'id': 'vg-09', 'name': 'Teclado Mecánico LED', 'price': 899.00, 'image': 'images/videojuegos/TecladoMecanicoLED.png'},
    {'id': 'vg-10', 'name': 'Xbox Series X', 'price': 11500.00, 'image': 'images/videojuegos/XboxSeriesX.png'},

    # Higiene
    {'id': 'hg-01', 'name': 'Acondicionador', 'price': 50.00, 'image': 'images/Higiene/Acondicionador.png'},
    {'id': 'hg-02', 'name': 'Cepillo Dientes OralB', 'price': 35.00, 'image': 'images/Higiene/CepilloDientesOralB.png'},
    {'id': 'hg-03', 'name': 'Desodorante Barra Hombre', 'price': 45.00, 'image': 'images/Higiene/DesodoranteBarraHombre.png'},
    {'id': 'hg-04', 'name': 'Desodorante Spray Hombre', 'price': 60.00, 'image': 'images/Higiene/DesodoranteSprayHombre.png'},
    {'id': 'hg-05', 'name': 'Desodorante Dove', 'price': 55.00, 'image': 'images/Higiene/DoveDesodorante.jpg'}, # Nota: .jpg
    {'id': 'hg-06', 'name': 'Enjuague Bucal', 'price': 70.00, 'image': 'images/Higiene/EnjuagueBucal.png'},
    {'id': 'hg-07', 'name': 'Gel Antibacterial', 'price': 25.00, 'image': 'images/Higiene/GelAntibacterial.png'},
    {'id': 'hg-08', 'name': 'Jabón en Barra', 'price': 20.00, 'image': 'images/Higiene/JabonBarra.png'},
    {'id': 'hg-09', 'name': 'Pasta Dental', 'price': 40.00, 'image': 'images/Higiene/PastaDental.png'},
    {'id': 'hg-10', 'name': 'Shampoo', 'price': 50.00, 'image': 'images/Higiene/Shampoo.png'},


    # --- >>> ¡¡¡AÑADE AQUÍ LOS PRODUCTOS DE LAS DEMÁS CATEGORÍAS!!! <<< ---
    # (Carnes, Lacteos, Abarrotes, Videojuegos, Higiene si es diferente a farmacia)
]


# --- RUTAS DE LA APLICACIÓN ---

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para Iniciar Sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Intento de inicio de sesión con Email: {email}")
        # Aquí iría la lógica de validación
    return render_template('login.html')

# --- RUTAS FIJAS (PÁGINAS ESPECIALES) ---
@app.route('/promociones')
def promociones():
    return render_template('Promociones.html')

# @app.route('/tiendas-oficiales') # Comentada porque no existe el HTML
# def tiendas_oficiales():
#     return render_template('tiendas_oficiales.html')

@app.route('/sucursales')
def sucursales():
    return render_template('sucursales.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/opciones')
def opciones():
    # Asumiendo que opciones.html existe
    return render_template('opciones.html') # Asegúrate que este archivo exista

# --- RUTA DINÁMICA PARA TODAS LAS CATEGORÍAS DE PRODUCTOS ---
@app.route('/categoria/<category_name>')
def category_page(category_name):
    category_data = CATEGORIES.get(category_name)
    if category_data:
        page_title, include_file = category_data
    else:
        page_title = 'Categoría no encontrada'
        include_file = None
    return render_template('category_page.html',
                           title=page_title,
                           content_to_include=include_file)

# --- RUTA PARA PAGO ---
@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        tarjeta = request.form.get('tarjeta', '') # Default a '' si no viene
        cart_data = request.form.get('cart_data')

        print("-" * 70)
        print(f" Nuevo Pedido Recibido:")
        print(f" Nombre: {nombre}, Email: {email}")
        print(f" Dirección: {direccion}")
        if tarjeta and len(tarjeta) >= 4:
             print(f" Tarjeta (últimos 4): {tarjeta[-4:]}")
        else:
             print(" Tarjeta: (inválida o no provista)")
        print(f" Datos del Carrito (JSON): {cart_data[:100]}...")
        print("-" * 70)

        # Simulación de pago exitoso
        # Asegúrate de tener 'pago_exitoso.html' en templates
        return render_template('pago_exitoso.html', nombre=nombre)

    # Si es GET
    return render_template('pago.html')

# --- ¡NUEVA RUTA DE BÚSQUEDA! ---
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    results = []
    if query:
        search_term = query.lower()
        results = [
            product for product in ALL_PRODUCTS
            if search_term in product['name'].lower()
        ]
    # Asegúrate de tener 'search_results.html' en templates
    return render_template('search_results.html',
                           query=query,
                           results=results)

# --- INICIA EL SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)