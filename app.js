const selectProductos = document.getElementById("productos");
const carritoHTML = document.getElementById("carrito");
const btnAgregar = document.getElementById("btn-agregar");
const btnComprar = document.getElementById("btn-comprar");
const totalHTML = document.getElementById("total");
const tablaCarrito = document.getElementById("tabla-carrito");

let productos = [
  { id: 101, nombre: "Arroz", precio: 25 },
  { id: 102, nombre: "Frijoles", precio: 30 },
  { id: 103, nombre: "Leche", precio: 22 },
  { id: 104, nombre: "Pan", precio: 18 },
  { id: 105, nombre: "Huevos (12 pzas)", precio: 45 }
];
let carrito = [];

fetch("http://127.0.0.1:5000/productos")
  .then(res => res.json())
  .then(data => {
    data.forEach(prod => {
      const option = document.createElement("option");
      option.value = prod.id;
      option.textContent = `${prod.nombre} - $${prod.precio}`;
      selectProductos.appendChild(option);
      productos.push(prod);
    });
  })
  .catch(() => console.warn("Backend no disponible, usando productos locales."));

btnAgregar.addEventListener("click", () => {
  const idSeleccionado = selectProductos.value;
  if (!idSeleccionado) {
    Swal.fire("Atención", "Por favor selecciona un producto", "warning");
    return;
  }

  const producto = productos.find(p => p.id == idSeleccionado);
  const item = carrito.find(p => p.id == producto.id);

  if (item) {
    item.cantidad += 1;
  } else {
    carrito.push({ ...producto, cantidad: 1 });
  }
  renderCarrito();
});

function renderCarrito() {
  carritoHTML.innerHTML = "";
  let total = 0;

  if (carrito.length === 0) {
    tablaCarrito.style.display = "none";
    totalHTML.style.display = "none";
    btnComprar.style.display = "none";
    return;
  } else {
    tablaCarrito.style.display = "table";
    totalHTML.style.display = "block";
    btnComprar.style.display = "block";
  }

  carrito.forEach((item, index) => {
    const subtotal = item.precio * item.cantidad;
    total += subtotal;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.nombre}</td>
      <td>
        <button class="cantidad-btn" onclick="cambiarCantidad(${index}, -1)">➖</button>
        ${item.cantidad}
        <button class="cantidad-btn" onclick="cambiarCantidad(${index}, 1)">➕</button>
      </td>
      <td>$${item.precio}</td>
      <td>$${subtotal}</td>
      <td><button onclick="eliminarDelCarrito(${index})" class="btn btn-danger">❌</button></td>
    `;
    carritoHTML.appendChild(tr);
  });

  totalHTML.textContent = `Total de la compra: $${total}`;
}

function cambiarCantidad(index, cambio) {
  carrito[index].cantidad += cambio;
  if (carrito[index].cantidad <= 0) {
    carrito.splice(index, 1);
  }
  renderCarrito();
}

function eliminarDelCarrito(index) {
  carrito.splice(index, 1);
  renderCarrito();
}

btnComprar.addEventListener("click", () => {
  if (carrito.length === 0) {
    Swal.fire("Carrito vacío", "Agrega productos antes de comprar", "warning");
    return;
  }

  Swal.fire({
    title: "Pago con tarjeta",
    html: `
      <input type="text" id="tarjeta" class="swal2-input" placeholder="Número de tarjeta" maxlength="16">
      <input type="text" id="fecha" class="swal2-input" placeholder="MM/AA" maxlength="5">
      <input type="text" id="cvv" class="swal2-input" placeholder="CVV" maxlength="3">
      <label style="display:flex;align-items:center;justify-content:center;margin-top:10px;">
        <input type="checkbox" id="guardarDatos"> Guardar datos de tarjeta
      </label>
    `,
    confirmButtonText: "Pagar",
    showCancelButton: true,
    preConfirm: () => {
      const tarjeta = document.getElementById("tarjeta").value.trim();
      const fecha = document.getElementById("fecha").value.trim();
      const cvv = document.getElementById("cvv").value.trim();
      const guardar = document.getElementById("guardarDatos").checked;

      if (!tarjeta || !fecha || !cvv) {
        Swal.showValidationMessage("Todos los campos son obligatorios");
        return false;
      }

      return { tarjeta, fecha, cvv, guardar };
    }
  }).then(result => {
    if (result.isConfirmed) {
      carrito.forEach(item => {
        fetch("http://127.0.0.1:5000/ventas", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            producto_id: item.id,
            cantidad: item.cantidad,
            cliente: "ClienteDemo"
          })
        }).catch(err => console.error("Error registrando venta:", err));
      });

      Swal.fire("Éxito", "Compra realizada con éxito ✅", "success");
      carrito = [];
      renderCarrito();
    }
  });
});
