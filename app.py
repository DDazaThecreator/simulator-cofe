import streamlit as st
import pandas as pd
import random

noticias = {
    "☀️ Buen clima en zonas cafeteras": 0.04,
    "❄️ Heladas afectan la cosecha": -0.05,
    "📈 Aumento de la demanda internacional": 0.06,
    "📉 Caída del consumo mundial": -0.04,
    "🚢 Problemas en exportaciones": -0.03,
    "🏭 Mayor inversión en producción": 0.03
}

st.set_page_config(page_title="Simulador de Inversión en Café", layout="centered")

st.title("☕ CoFFEe Trade Pro")

# ---------------- ESTADO INICIAL ----------------
if "noticia_actual" not in st.session_state:
    st.session_state.noticia_actual = "Sin noticias hoy"

if "dia" not in st.session_state:
    st.session_state.dia = 1

if "precio" not in st.session_state:
    st.session_state.precio = 12000.0

if "capital" not in st.session_state:
    st.session_state.capital = 1_000_000.0

if "acciones" not in st.session_state:
    st.session_state.acciones = 0

if "precios" not in st.session_state:
    st.session_state.precios = [st.session_state.precio]

if "movimientos" not in st.session_state:
    st.session_state.movimientos = pd.DataFrame(
        columns=["Día", "Acción", "Precio", "Cantidad", "Capital restante"]
    )

# ---------------- INFORMACIÓN ----------------
st.markdown(f"""
### 📅 Día {st.session_state.dia}
**Precio actual del café:** ${st.session_state.precio:,.2f}
""")
st.info(f"📰 Noticia del día: {st.session_state.noticia_actual}")


# ---------------- CAPITAL EDITABLE ----------------
capital_input = st.number_input(
    "💰 Capital disponible",
    min_value=0.0,
    value=st.session_state.capital,
    step=10000.0
)

st.session_state.capital = capital_input

st.write(f"☕ Acciones en cartera: {st.session_state.acciones}")

# ---------------- OPERACIONES ----------------
st.subheader("📈 Operaciones")

cantidad = st.number_input("Cantidad de acciones", min_value=1, step=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("Comprar"):
        costo = cantidad * st.session_state.precio
        if costo <= st.session_state.capital:
            st.session_state.capital -= costo
            st.session_state.acciones += cantidad

            st.session_state.movimientos = pd.concat([
                st.session_state.movimientos,
                pd.DataFrame([{
                    "Día": st.session_state.dia,
                    "Acción": "Compra",
                    "Precio": st.session_state.precio,
                    "Cantidad": cantidad,
                    "Capital restante": st.session_state.capital
                }])
            ], ignore_index=True)
        else:
            st.error("Capital insuficiente")

with col2:
    if st.button("Vender"):
        if cantidad <= st.session_state.acciones:
            ingreso = cantidad * st.session_state.precio
            st.session_state.capital += ingreso
            st.session_state.acciones -= cantidad

            st.session_state.movimientos = pd.concat([
                st.session_state.movimientos,
                pd.DataFrame([{
                    "Día": st.session_state.dia,
                    "Acción": "Venta",
                    "Precio": st.session_state.precio,
                    "Cantidad": cantidad,
                    "Capital restante": st.session_state.capital
                }])
            ], ignore_index=True)
        else:
            st.error("No tienes suficientes acciones")

# ---------------- AVANZAR DÍA ----------------
if st.button("⏭ Avanzar día"):
    noticia, impacto = random.choice(list(noticias.items()))

    cambio_base = random.uniform(-0.02, 0.02)
    cambio_total = cambio_base + impacto

    st.session_state.precio *= (1 + cambio_total)
    st.session_state.dia += 1
    st.session_state.precios.append(st.session_state.precio)

    st.session_state.noticia_actual = noticia

# ---------------- GRÁFICA ----------------
st.subheader("📊 Precio del café en el tiempo")
st.line_chart(st.session_state.precios)

# ---------------- HISTORIAL ----------------
st.subheader("📋 Historial de movimientos")
st.dataframe(st.session_state.movimientos)

# ---------------- VALOR TOTAL ----------------
valor_total = st.session_state.capital + (
    st.session_state.acciones * st.session_state.precio
)

st.metric("📊 Valor total del portafolio", f"${valor_total:,.2f}")

# ---------------- REINICIO ----------------
if st.button("🔄 Reiniciar simulador"):
    st.session_state.clear()
    st.rerun()
