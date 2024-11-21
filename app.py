from dash import Dash
from components.layout import create_layout
from components.callbacks import register_callbacks
from components.data_processing import load_and_prepare_data
import webbrowser
from threading import Timer

# Adatok betöltése
file_path = './stadat-jov0045-14.1.2.4-hu.csv'
data = load_and_prepare_data(file_path)

# Dash alkalmazás inicializálása
app = Dash(__name__)
app.title = "Jövedelem Alakulása"
app.layout = create_layout(data)

# Callback-ek regisztrálása
register_callbacks(app, data)

# Automatikus böngésző megnyitás funkció
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

# Alkalmazás futtatása
if __name__ == '__main__':
    # Flask újraindítás kikapcsolása és böngésző indítása
    Timer( 1,open_browser).start()
    app.run_server(debug=False)  # A debug kapcsoló kikapcsolása
