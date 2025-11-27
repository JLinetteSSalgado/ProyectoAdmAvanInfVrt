# Importamos las herramientas necesarias de Flask
# AGREGAMOS 'jsonify' para poder responderle a PayPal
from flask import Flask, render_template, request, jsonify
import json
# Inicializa la aplicación Flask
application = app = Flask(__name__)
# ==========================================
# ⚠️ CONFIGURACIÓN DE AWS (OBLIGATORIO) ⚠️
# ==========================================
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Tus datos reales (los saqué de tus mensajes anteriores)
AWS_DB_ENDPOINT = "tienda-db.cbgmg8ssyk5d.us-east-2.rds.amazonaws.com"
AWS_DB_USER = "admin"
AWS_DB_PASS = "Tienda2025AWS"  # <-- CONFIRMA QUE ESTA SEA TU CONTRASEÑA
AWS_DB_NAME = "tienda_online"

# Configurar la conexión
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{AWS_DB_USER}:{AWS_DB_PASS}@{AWS_DB_ENDPOINT}/{AWS_DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# --- MODELO DE BASE DE DATOS (TABLA DE VENTAS) ---
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    total_pagado = db.Column(db.Float, nullable=False)
    paypal_order_id = db.Column(db.String(100), unique=True, nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    detalles_productos = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Venta {self.paypal_order_id}>'

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
    {'id': 'f-01', 'name': 'Coco', 'price': 25.00, 'image': 'images/frutas/coco.png'},
    {'id': 'f-02', 'name': 'Durazno', 'price': 10.00, 'image': 'images/frutas/durazno.png'},
    {'id': 'f-03', 'name': 'Fresa', 'price': 8.00, 'image': 'images/frutas/fresa.png'},
    {'id': 'f-04', 'name': 'Kiwi', 'price': 12.00, 'image': 'images/frutas/kiwi.png'},
    {'id': 'f-05', 'name': 'Lechuga', 'price': 18.00, 'image': 'images/frutas/lechuga.jpg'},
    {'id': 'f-06', 'name': 'Mango', 'price': 15.00, 'image': 'images/frutas/mango.png'},
    {'id': 'f-07', 'name': 'Manzana', 'price': 9.00, 'image': 'images/frutas/manzana.jpg'},
    {'id': 'f-08', 'name': 'Naranja', 'price': 6.00, 'image': 'images/frutas/naranja.png'},
    {'id': 'f-09', 'name': 'Piña', 'price': 35.00, 'image': 'images/frutas/piña.jpg'},
    {'id': 'f-10', 'name': 'Plátano', 'price': 5.00, 'image': 'images/frutas/platano.png'},
    # Verduras
    {'id': 'v-01', 'name': 'Brócoli', 'price': 25.00, 'image': 'images/verduras/brocoli.png'},
    {'id': 'v-02', 'name': 'Cebolla Blanca', 'price': 10.00, 'image': 'images/verduras/cebollablanca.png'},
    {'id': 'v-03', 'name': 'Cebolla Morada', 'price': 12.00, 'image': 'images/verduras/cebollamorada.png'},
    {'id': 'v-04', 'name': 'Champiñones', 'price': 18.00, 'image': 'images/verduras/champiñones.png'},
    {'id': 'v-05', 'name': 'Chile de Árbol', 'price': 6.00, 'image': 'images/verduras/chilearbol.jpg'},
    {'id': 'v-06', 'name': 'Elote', 'price': 8.00, 'image': 'images/verduras/elote.jpg'},
    {'id': 'v-07', 'name': 'Papa', 'price': 9.00, 'image': 'images/verduras/papa.png'},
    {'id': 'v-08', 'name': 'Tomate Rojo', 'price': 7.00, 'image': 'images/verduras/tomate rojo.jpg'},
    {'id': 'v-09', 'name': 'Tomate Verde', 'price': 6.50, 'image': 'images/verduras/tomateverde.jpg'},
    {'id': 'v-10', 'name': 'Zanahoria', 'price': 5.00, 'image': 'images/verduras/zanahoria.png'},
    # Deportes
    {'id': 'dpt-01', 'name': 'Balón de Fútbol No. 5', 'price': 349.00, 'image': 'images/deportes/balon.png'},
    {'id': 'dpt-02', 'name': 'Balón de Americano', 'price': 420.00, 'image': 'images/deportes/balonamericano.png'},
    {'id': 'dpt-03', 'name': 'Banco Press', 'price': 1899.00, 'image': 'images/deportes/bancopres.png'},
    {'id': 'dpt-04', 'name': 'Guantes Portero Futbol', 'price': 299.00, 'image': 'images/deportes/guantesfurbol.png'},
    {'id': 'dpt-05', 'name': 'Juego de Pesas 20kg', 'price': 999.00, 'image': 'images/deportes/juegopesas.png'},
    {'id': 'dpt-06', 'name': 'Ligas de Ejercicio', 'price': 250.00, 'image': 'images/deportes/ligasejercicio.png'},
    {'id': 'dpt-07', 'name': 'Pelota Grande Yoga', 'price': 320.00, 'image': 'images/deportes/pelotagrande.png'},
    {'id': 'dpt-08', 'name': 'Raqueta de Tenis', 'price': 750.00, 'image': 'images/deportes/raquetatenis.png'},
    # Tecnologia
    {'id': 't-01', 'name': 'Audífonos Bluetooth', 'price': 299.00, 'image': 'images/tecnologias/audifonosbluetooth.png'},
    {'id': 't-02', 'name': 'Bocina Bluetooth', 'price': 450.00, 'image': 'images/tecnologias/bocinabluetooth.png'},
    {'id': 't-03', 'name': 'Cargador USB', 'price': 120.00, 'image': 'images/tecnologias/cargadorusb.png'},
    {'id': 't-04', 'name': 'Disco Duro Externo', 'price': 950.00, 'image': 'images/tecnologias/discoduroexterno.jpg'},
    {'id': 't-05', 'name': 'Laptop HP', 'price': 9500.00, 'image': 'images/tecnologias/laptophp.png'},
    {'id': 't-06', 'name': 'Memoria USB', 'price': 85.00, 'image': 'images/tecnologias/memoriausb.png'},
    {'id': 't-07', 'name': 'Monitor Samsung', 'price': 2200.00, 'image': 'images/tecnologias/monitorsamsung.png'},
    {'id': 't-08', 'name': 'Mouse Inalámbrico', 'price': 180.00, 'image': 'images/tecnologias/mouseinalambrico.png'},
    {'id': 't-09', 'name': 'Smartwatch', 'price': 699.00, 'image': 'images/tecnologias/smartwatch.png'},
    {'id': 't-10', 'name': 'Teclado Mecánico', 'price': 350.00, 'image': 'images/tecnologias/tecladomecanico.png'},
    # Vinos
    {'id': 'v-01', 'name': 'Alcohol Azul', 'price': 95.00, 'image': 'images/vinos/alcoholazulpng.png'},
    {'id': 'v-02', 'name': 'Alcohol Rojo', 'price': 90.00, 'image': 'images/vinos/alcoholrojo.png'},
    {'id': 'v-03', 'name': 'Bacardi', 'price': 280.00, 'image': 'images/vinos/bacardi.png'},
    {'id': 'v-04', 'name': 'Blue Label', 'price': 1650.00, 'image': 'images/vinos/bluelabel.jpg'},
    {'id': 'v-05', 'name': 'Carta Blanca', 'price': 50.00, 'image': 'images/vinos/cartablancajpg.jpg'},
    {'id': 'v-06', 'name': 'José Cuervo', 'price': 320.00, 'image': 'images/vinos/josecuervo.png'},
    {'id': 'v-07', 'name': 'Oso Negro', 'price': 180.00, 'image': 'images/vinos/osonegrol.png'},
    {'id': 'v-08', 'name': 'Red Label', 'price': 950.00, 'image': 'images/vinos/redlabel.png'},
    {'id': 'v-09', 'name': 'Tonayán', 'price': 45.00, 'image': 'images/vinos/tonayan.png'},
    {'id': 'v-10', 'name': 'Victoria Media', 'price': 55.00, 'image': 'images/vinos/victoriamedia.png'},
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
    {'id': 'fa-01', 'name': 'Analgésico CafiAspirina', 'price': 155.00, 'image': 'images/farmacia/analgésicos.jpg'},
    {'id': 'fa-02', 'name': 'Jarabe VICK 44', 'price': 98.50, 'image': 'images/farmacia/jarabetos.jpg'},
    {'id': 'fa-03', 'name': 'Agua Oxigenada JALOMA', 'price': 35.00, 'image': 'images/farmacia/aguaoxigenada.jpg'},
    {'id': 'fa-04', 'name': 'Venda Elástica Quirurgical', 'price': 45.99, 'image': 'images/farmacia/vendas.jpg'},
    {'id': 'fa-05', 'name': 'Cepillo Dental Colgate 360°', 'price': 79.90, 'image': 'images/farmacia/cepillodientes.jgp.jpg'},
    {'id': 'fa-06', 'name': 'Pasta Dental Fluorada', 'price': 42.50, 'image': 'images/farmacia/pastadientes.jpg'},
    {'id': 'fa-07', 'name': 'Hilo Dental G·U·M', 'price': 65.00, 'image': 'images/farmacia/hilodental.jpg'},
    {'id': 'fa-08', 'name': 'Protector Solar Avène SPF 50+', 'price': 499.00, 'image': 'images/farmacia/protectorsolar.jpg'},
    {'id': 'fa-09', 'name': 'Crema Hidratante Neutrogena', 'price': 230.75, 'image': 'images/farmacia/cremahidratante.jpg'},
    {'id': 'fa-10', 'name': 'Suplemento Proteína WHEY', 'price': 899.90, 'image': 'images/farmacia/suplementos.jpg'},
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
    # Videojuegos
    {'id': 'vg-01', 'name': 'Audífonos Gamer', 'price': 750.00, 'image': 'images/videojuegos/audifonosgamer.png'},
    {'id': 'vg-02', 'name': 'Consola PlayStation 5', 'price': 12500.00, 'image': 'images/videojuegos/consolaplaystation5.png'},
    {'id': 'vg-03', 'name': 'Control DualSense (PS5)', 'price': 1599.00, 'image': 'images/videojuegos/controldualsense.png'},
    {'id': 'vg-04', 'name': 'Control Xbox Wireless', 'price': 1399.00, 'image': 'images/videojuegos/controlxboxwireless.jpg'},
    {'id': 'vg-05', 'name': 'Halo Infinite', 'price': 1199.00, 'image': 'images/videojuegos/haloinfinite.jpg'},
    {'id': 'vg-06', 'name': 'Mouse Gamer RGB', 'price': 450.00, 'image': 'images/videojuegos/mousegamerrgb.png'},
    {'id': 'vg-07', 'name': 'Nintendo Switch OLED', 'price': 7499.00, 'image': 'images/videojuegos/nintendoswitcholed.png'},
    {'id': 'vg-08', 'name': 'Silla Gamer', 'price': 3200.00, 'image': 'images/videojuegos/sillagamer.png'},
    {'id': 'vg-09', 'name': 'Teclado Mecánico LED', 'price': 899.00, 'image': 'images/videojuegos/tecladomecanicoled.png'},
    {'id': 'vg-10', 'name': 'Xbox Series X', 'price': 11500.00, 'image': 'images/videojuegos/xboxseriesx.png'},
    # Higiene
    {'id': 'hg-01', 'name': 'Acondicionador', 'price': 50.00, 'image': 'images/higiene/acondicionador.png'},
    {'id': 'hg-02', 'name': 'Cepillo Dientes OralB', 'price': 35.00, 'image': 'images/higiene/cepillodientesoralb.png'},
    {'id': 'hg-03', 'name': 'Desodorante Barra Hombre', 'price': 45.00, 'image': 'images/higiene/desodorantebarrahombre.png'},
    {'id': 'hg-04', 'name': 'Desodorante Spray Hombre', 'price': 60.00, 'image': 'images/higiene/desodorantesprayhombre.png'},
    {'id': 'hg-05', 'name': 'Desodorante Dove', 'price': 55.00, 'image': 'images/higiene/dovedesodorante.jpg'},
    {'id': 'hg-06', 'name': 'Enjuague Bucal', 'price': 70.00, 'image': 'images/higiene/enjuaguebucal.png'},
    {'id': 'hg-07', 'name': 'Gel Antibacterial', 'price': 25.00, 'image': 'images/higiene/gelantibacterial.png'},
    {'id': 'hg-08', 'name': 'Jabón en Barra', 'price': 20.00, 'image': 'images/higiene/jabonbarra.png'},
    {'id': 'hg-09', 'name': 'Pasta Dental', 'price': 40.00, 'image': 'images/higiene/pastadental.png'},
    {'id': 'hg-10', 'name': 'Shampoo', 'price': 50.00, 'image': 'images/higiene/shampoo.png'},
]


# --- RUTAS DE LA APLICACIÓN ---

# --- RUTAS PRINCIPALES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de login simulada
        return render_template('index.html')
    return render_template('login.html')

@app.route('/promociones')
def promociones():
    return render_template('Promociones.html')

@app.route('/sucursales')
def sucursales():
    return render_template('Sucursales.html')

@app.route('/ayuda')
def ayuda():
    return render_template('Ayuda.html')

@app.route('/opciones')
def opciones():
    # Si no tienes un opciones.html, redirige a home o login
    return render_template('login.html') 

# --- RUTA DINÁMICA PARA CATEGORÍAS ---
@app.route('/categoria/<category_name>')
def category_page(category_name):
    category_data = CATEGORIES.get(category_name)
    
    if category_data:
        title, template_name = category_data
        # Renderizamos una plantilla base (por ejemplo category_page.html) 
        # y le pasamos qué contenido incluir
        return render_template('category_page.html', 
                             title=title, 
                             content_to_include=template_name,
                             current_category=category_name)
    else:
        return render_template('index.html') # O una página 404

# --- RUTA DE PAGO (Visualización) ---
@app.route('/pago')
def pago():
    # Solo renderiza la página, el procesamiento se hará vía API para PayPal
    return render_template('pago.html')

# --- ¡NUEVA INTEGRACIÓN! API PARA PROCESAR PAGO DE PAYPAL ---
# --- ¡NUEVA INTEGRACIÓN! API PARA PROCESAR PAGO DE PAYPAL ---
@app.route('/api/procesar_pago', methods=['POST'])
def procesar_pago():
    try:
        # 1. Recibir los datos JSON que envía el JavaScript (PayPal)
        data = request.get_json()
        
        order_id = data.get('orderID')
        details = data.get('details')
        carrito = data.get('cart')
        total = data.get('total')

        # Extraer datos del cliente para la BD
        cliente_nombre = f"{details.get('payer', {}).get('name', {}).get('given_name')} {details.get('payer', {}).get('name', {}).get('surname')}"
        
        # Formatear el carrito a una cadena JSON para guardarlo en la columna 'detalles_productos'
        # Usamos json.dumps() para convertir el diccionario de Python a una cadena JSON
        detalles_json = json.dumps(carrito) 
        
        # 2. VALIDACIÓN: Verificar si esta orden ya existe para evitar duplicados
        venta_existente = Venta.query.filter_by(paypal_order_id=order_id).first()
        if venta_existente:
             # Si ya existe, simplemente retorna éxito sin hacer nada.
             print(f"⚠️ Venta {order_id} ya registrada. Omitiendo inserción.")
             return jsonify({'status': 'success', 'message': 'Venta ya registrada'})


        # 3. CREAR Y GUARDAR LA VENTA EN LA BASE DE DATOS AWS
        nueva_venta = Venta(
            cliente_nombre=cliente_nombre,
            total_pagado=total,
            paypal_order_id=order_id,
            detalles_productos=detalles_json
        )
        
        db.session.add(nueva_venta)
        db.session.commit()
        
        # 4. Mensajes de confirmación
        print("-" * 70)
        print(f"✅ VENTA REGISTRADA EN AWS")
        print(f"   ID de Transacción: {order_id}")
        print(f"   Cliente: {cliente_nombre}")
        print(f"   Total Pagado: ${total}")
        print("-" * 70)

        # 5. Responder a la página web que todo salió bien
        return jsonify({'status': 'success', 'message': 'Pago recibido y registrado correctamente'})

    except Exception as e:
        # Revertir cualquier cambio si algo falla
        db.session.rollback() 
        print(f"❌ Error al procesar o guardar el pago: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# --- RUTA PARA PAGO EXITOSO ---
@app.route('/pago_exitoso')
def pago_exitoso():
    # Recibimos el nombre para mostrarlo en el mensaje de agradecimiento
    nombre = request.args.get('nombre', 'Cliente') 
    return render_template('pago_exitoso.html', nombre=nombre)

# --- RUTA DE BÚSQUEDA ---
@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    results = []

    if query:
        # Buscar coincidencias dentro del nombre del producto
        results = [
            p for p in ALL_PRODUCTS 
            if query in p['name'].lower()
        ]

    return render_template('search_results.html', query=query, results=results)


# --- RUTA SECRETA PARA CREAR LA BASE DE DATOS DESDE EL NAVEGADOR ---
@app.route('/crear-tablas')
def crear_tablas_manual():
    try:
        db.create_all()
        return "<h1>✅ ¡Tablas creadas exitosamente en AWS!</h1><p>Ya puedes usar la tienda.</p>"
    except Exception as e:
        return f"<h1>❌ Error:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)