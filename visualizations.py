import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Carrega de dades
# ---------------------------------------------------------------------

# Carreguem les tres taules a partir dels fitxers CSV generats.
histogram_df = pd.read_csv("histogram_data.csv")
radar_df = pd.read_csv("radar_data.csv")
marimekko_df = pd.read_csv("marimekko_data.csv")


# ---------------------------------------------------------------------
# a) HISTOGRAMA DE NOTES D'EXAMEN
# ---------------------------------------------------------------------

# L'objectiu és veure la distribució de les notes dels estudiants.
scores = histogram_df["score"]

plt.figure(figsize=(8, 5))
# Definim un nombre de bins suficientment fi per veure la forma
# de la distribució sense que sigui massa sorollosa.
plt.hist(scores, bins=15, color="#4C72B0", edgecolor="white")

plt.title("Distribució de les notes d'examen")
plt.xlabel("Puntuació")
plt.ylabel("Nombre d'estudiants")
plt.tight_layout()
plt.show()


# ---------------------------------------------------------------------
# b) DIAGRAMA RADAR (HABILITATS DE PERSONES EMPLEADES)
# ---------------------------------------------------------------------

# El radar representa diverses dimensions (habilitats) per a cada persona,
# utilitzant coordenades polars.

# La primera columna és la categoria (empleat) i la resta són variables numèriques.
categories = list(radar_df.columns[1:])
num_vars = len(categories)

# Calculem els angles per a cada eix del radar en radians.
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
# Tanquem el cercle afegint el primer angle al final.
angles += angles[:1]

plt.figure(figsize=(7, 7))
ax = plt.subplot(111, polar=True)

# Dibuixem un radar per a cada empleat.
for _, row in radar_df.iterrows():
    values = row[categories].tolist()
    # Tanquem el polígon repetint el primer valor.
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=row["employee"])
    ax.fill(angles, values, alpha=0.15)

# Configurem les etiquetes dels eixos i el títol.
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_yticklabels([])  # Eliminem etiquetes radials per simplificar la lectura.

plt.title("Avaluació d'habilitats per empleat")
plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.show()


# ---------------------------------------------------------------------
# c) DIAGRAMA MARIMEKKO (VENDES PER REGIÓ I PRODUCTE)
# ---------------------------------------------------------------------

# Un Marimekko combina l'amplada de les barres (pes de la regió)
# i l'alçada apilada (repartiment de productes dins de la regió).

# Calculem les vendes totals i el pes de cada regió.
marimekko_df["sales"] = marimekko_df["sales"].astype(float)

total_sales = marimekko_df["sales"].sum()
region_totals = marimekko_df.groupby("region")["sales"].sum()
products = marimekko_df["product"].unique()

# Amplades relatives per a cada regió (suma = 1).
region_widths = region_totals / total_sales

# Assignem una posició horitzontal acumulada a cada regió.
region_left = {}
current_left = 0.0
for region, width in region_widths.items():
    region_left[region] = current_left
    current_left += width

# Preparem colors diferents per a cada producte.
colors = plt.cm.Set2(np.linspace(0, 1, len(products)))
product_colors = dict(zip(products, colors))

plt.figure(figsize=(10, 6))

# Per a cada regió, apilem barres pels diferents productes.
for region in region_totals.index:
    subset = marimekko_df[marimekko_df["region"] == region]
    region_total = region_totals[region]

    bottom = 0.0
    for _, row in subset.iterrows():
        product = row["product"]
        value = row["sales"]

        # Alçada relativa dins de la regió.
        height = value / region_total
        plt.bar(
            x=region_left[region],
            height=height,
            width=region_widths[region],
            bottom=bottom,
            color=product_colors[product],
            edgecolor="white",
            align="edge",
            label=product if region == region_totals.index[0] else None,
        )
        bottom += height

# Configurem eixos i etiquetes.
plt.title("Vendes per regió i categoria de producte (Marimekko)")
plt.xlabel("Pes relatiu de cada regió en el total de vendes")
plt.ylabel("Distribució relativa de productes dins de la regió")

# Etiquetes de les regions centrades a cada barra.
for region, left in region_left.items():
    width = region_widths[region]
    plt.text(
        left + width / 2,
        1.02,
        region,
        ha="center",
        va="bottom",
    )

plt.ylim(0, 1.1)
plt.xlim(0, 1)
plt.legend(title="Producte", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
