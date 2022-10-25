
import pandas as pd

def get_pokemon_data(pokemon : str, df_stats : pd.DataFrame, df_all_moves : pd.DataFrame):
    pokemon = pokemon[0] + pokemon[1:].lower()
    pokemon = pokemon.strip()
    df_current_pokemon = df_stats[df_stats.columns.difference(["Legendary", "Generation"])].loc[df_stats[df_stats["Name"] == pokemon].index[0]]
    return df_current_pokemon