from dash import Dash
from components.layout import create_layout
from components.callbacks import register_callbacks
from components.data_processing import load_and_prepare_data
import webbrowser
from threading import Timer

# Adatok betöltése
# A jövedelmi adatokat tartalmazó CSV fájl betöltése és előkészítése a "load_and_prepare_data" függvénnyel.
# A "file_path" változó tartalmazza az adatok forrásfájl elérési útját.
file_path = 'forras.csv'
data = load_and_prepare_data(file_path)

# Dash alkalmazás inicializálása
# Egy új Dash alkalmazás létrehozása. A cím és az elrendezés is konfigurálva van.
app = Dash(__name__)  # Az alkalmazás fő objektuma
app.title = "Jövedelem Alakulása"  # Az alkalmazás böngésző címe
app.layout = create_layout(data)  # Az elrendezést létrehozó függvény a betöltött adatok alapján állítja be a kinézetet
print("1")

# Callback-ek regisztrálása
# A felhasználói interakciók kezeléséhez szükséges callback függvények regisztrálása.
# Ezek a függvények az alkalmazás működését szabályozzák (pl. grafikonok frissítése).
register_callbacks(app, data)

# Automatikus böngésző megnyitás funkció
# Egy funkció, amely automatikusan megnyitja a böngészőt az alkalmazás URL-jével.
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")  # Az alkalmazás helyi URL-jének megnyitása

# Alkalmazás futtatása
# A program belépési pontja. Ha a fájl közvetlenül futtatva van:
if __name__ == 'KSH':
    # Timer indítása az automatikus böngésző megnyitásához.
    # Ez 1 másodperces késleltetéssel meghívja az "open_browser" függvényt.
    Timer(1, open_browser).start()

    # A Dash alkalmazás szerverének futtatása.
    # A debug módot kikapcsoljuk, hogy a hibák ne jelenjenek meg a végfelhasználóknak.
    app.run_server(debug=False)
