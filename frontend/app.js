const API_URL = "http://localhost:8000";

const seccionCorreo = document.getElementById("seccion-correo");
const seccionCodigo = document.getElementById("seccion-codigo");
const seccionRegistro = document.getElementById("seccion-registro");
const seccionLogin = document.getElementById("seccion-login");

const inputEmail = document.getElementById("email");
const inputCodigo = document.getElementById("codigo");
const inputUsername = document.getElementById("username");

const btnEnviarCorreo = document.getElementById("btn-enviar-correo");
const btnVerificarCodigo = document.getElementById("btn-verificar-codigo");
const btnRegistrar = document.getElementById("btn-registrar");
const btnLogin = document.getElementById("btn-login");

const mensajeEstado = document.getElementById("mensaje-estado");
const instrucciones = document.getElementById("instrucciones");

let emailUsuario = ""; 

// 1. SOLICITAR CÓDIGO
btnEnviarCorreo.addEventListener("click", async () => {
    emailUsuario = inputEmail.value.trim();
    if (!emailUsuario) {
        mostrarMensaje("Por favor, introduce un correo válido.", "error");
        return;
    }
    mostrarMensaje("Enviando código...", "exito");

    try {
        const respuesta = await fetch(`${API_URL}/auth/request-code`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: emailUsuario })
        });
        const data = await respuesta.json();

        if (respuesta.ok) {
            seccionCorreo.classList.add("hidden");
            seccionCodigo.classList.remove("hidden");
            instrucciones.innerText = `Código enviado a ${emailUsuario}. Revisa la terminal de Docker.`;
            mostrarMensaje(data.mensaje, "exito");
        } else {
            mostrarMensaje(data.detail || "Error.", "error");
        }
    } catch (error) {
        mostrarMensaje("No se pudo conectar con el backend.", "error");
    }
});

// 2. VERIFICAR CÓDIGO (DECISIÓN INTELIGENTE)
btnVerificarCodigo.addEventListener("click", async () => {
    const codigoUsuario = inputCodigo.value.trim();
    if (codigoUsuario.length !== 6) {
        mostrarMensaje("El código debe tener 6 dígitos.", "error");
        return;
    }

    try {
        const respuesta = await fetch(`${API_URL}/auth/verify-code`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: emailUsuario, codigo: codigoUsuario })
        });
        const data = await respuesta.json();

        if (respuesta.ok) {
            seccionCodigo.classList.add("hidden");
            
            // Si el backend dice que el usuario YA existe en PostgreSQL
            if (data.existe) {
                seccionLogin.classList.remove("hidden");
                instrucciones.innerText = `¡Hola de nuevo, ${data.username}! Tu código es correcto.`;
                mostrarMensaje("Haz clic abajo para iniciar sesión.", "exito");
            } else {
                // Si el usuario NO existe en PostgreSQL
                seccionRegistro.classList.remove("hidden");
                instrucciones.innerText = "Código correcto. Veo que eres nuevo, elige tu nombre de usuario:";
                mostrarMensaje("Por favor regístrate.", "exito");
            }
        } else {
            mostrarMensaje(data.detail || "Código incorrecto.", "error");
        }
    } catch (error) {
        mostrarMensaje("No se pudo conectar con el backend.", "error");
    }
});

// 3. REGISTRO (Para usuarios nuevos)
btnRegistrar.addEventListener("click", async () => {
    const usernameUsuario = inputUsername.value.trim();
    if (!usernameUsuario) {
        mostrarMensaje("Introduce un nombre de usuario.", "error");
        return;
    }

    try {
        const respuesta = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: emailUsuario, username: usernameUsuario })
        });
        const data = await respuesta.json();

        if (respuesta.ok) {
            seccionRegistro.classList.add("hidden");
            instrucciones.innerText = `¡Cuenta creada con éxito, bienvenido ${data.usuario.username}!`;
            mostrarMensaje(data.mensaje, "exito");
        } else {
            mostrarMensaje(data.detail || "Error en el registro.", "error");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión.", "error");
    }
});

// 4. LOGIN DIRECTO (Para usuarios existentes)
btnLogin.addEventListener("click", async () => {
    try {
        const respuesta = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: emailUsuario })
        });
        const data = await respuesta.json();

        if (respuesta.ok) {
            seccionLogin.classList.add("hidden");
            instrucciones.innerText = `¡Sesión Iniciada correctamente! Token simulado guardado.`;
            mostrarMensaje(data.mensaje, "exito");
            console.log("Token JWT simulado recibido:", data.token_simulado);
        } else {
            mostrarMensaje(data.detail || "Error al iniciar sesión.", "error");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión.", "error");
    }
});

function mostrarMensaje(texto, tipo) {
    mensajeEstado.innerText = texto;
    mensajeEstado.className = tipo;
}