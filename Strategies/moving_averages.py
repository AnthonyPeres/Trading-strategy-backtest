import numpy as np
import hvplot.pandas

def sma(stock_symbol, data, short_window=50, long_window=100, make_entry_exit=True):
    """
    Fonction qui calcule les moyennes mobiles arithmétique (non exponentielle) avec
    comme période short_window et long_window sur un DataFrame possédant une colonne 'Close'.

    Si make_entry_exit = True, la fonction va calculer les points d'entrées et de sorties
    en rapport avec la position relative des deux SMA.

    TODO: Faire une exception si on peut pas faire les 2 sma (taille du df trop courte
    """

    # On crée les 2 colonnes SMA[short_window] et SMA[long_window]
    column_short_window = 'SMA' + str(short_window)
    column_long_window = 'SMA' + str(long_window)
    data[column_short_window] = data['Close'].rolling(window=short_window).mean()
    data[column_long_window] = data['Close'].rolling(window=long_window).mean()

    if make_entry_exit:
        # On crée le signal
        # SMA50 < SMA100: 0
        # SMA50 >= SMA100: 1
        data['Signal'] = 0.0
        data['Signal'][short_window:] = np.where(
            data[column_short_window][short_window:] > data[column_long_window][short_window:], 1.0, 0.0
        )

        # On calcul les points d'entrée et de sortie
        # Entry: 1.0
        # Exit: -1.0
        data['Entree/Sortie'] = data['Signal'].diff()
    
    # PLOT
    moving_avgs = data[[column_short_window, column_long_window]].hvplot(ylabel='Price in $', width=1000, height=400)
    security_close = data[['Close']].hvplot(line_color='lightgray', ylabel='Price in $', width=1000, height=400)

    if make_entry_exit:
        entry = data[data['Entree/Sortie'] == 1.0]['Close'].hvplot.scatter(color='green', legend=False, ylabel='Price in $', width=1000, height=400)
        exit = data[data['Entree/Sortie'] == -1.0]['Close'].hvplot.scatter(color='red', legend=False, ylabel='Price in $', width=1000, height=400)
        entry_exit_plot = security_close * moving_avgs * entry * exit
    else:
        entry_exit_plot = security_close * moving_avgs
    
    if stock_symbol:
        entry_exit_plot.opts(title=stock_symbol)  
    else:
        entry_exit_plot.opts(xaxis=None)  
    hvplot.show(entry_exit_plot)