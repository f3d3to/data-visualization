import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pyvis.network import Network
import re
import networkx as nx

class Database:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.column_names = self.df.columns.tolist()
        self.db_name = self._get_database_name(csv_file)
        self.objects = self._create_objects()

    def __repr__(self):
        return f"DB(name='{self.db_name}', columns={self.column_names}, rows={len(self.df)})"

    def _get_database_name(self, csv_file):
        """
        Método privado para obtener el nombre de la base de datos desde el nombre del archivo CSV.
        """
        file_name = csv_file.split('/')[-1].split('.')[0].replace("_", " ")
        return file_name

    def _create_objects(self):
        """
        Método privado para crear instancias de objetos basados en los datos del DataFrame.
        Retorna una lista de instancias de DatabaseObject.
        """
        objects = []

        for index, row in self.df.iterrows():
            # Crear un diccionario con los datos de la fila
            row_data = {col: row[col] for col in self.column_names}

            # Crear una instancia de DatabaseObject usando kwargs dinámicos
            obj = DatabaseObject(**row_data)
            objects.append(obj)

        return objects

    def filter_objects(self, **filters):
        """
        Método para filtrar las instancias de DatabaseObject basado en los filtros especificados.
        Utiliza los objetos previamente creados y almacenados en self.objects.
        """
        filtered_objects = []

        for obj in self.objects:
            matches = all(getattr(obj, key) == value for key, value in filters.items())
            if matches:
                filtered_objects.append(obj)

        return filtered_objects

    def visualize_dataframe(self):
        """
        Método para visualizar las filas y columnas del DataFrame.
        Utiliza Plotly para mostrar una tabla interactiva.
        """
        column_names = self.column_names

        fig = go.Figure(data=[go.Table(
            header=dict(values=column_names,
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[self.df[col].tolist() for col in column_names],
                       fill_color='lavender',
                       align='left')
        )])

        fig.update_layout(title='Visualización de Filas y Columnas del DataFrame',
                          title_font_size=24)
        fig.show()

    def plot_interactive_graph(self):
        """
        Método para visualizar un grafo interactivo utilizando Pyvis.
        Los nodos representan las columnas y sus datos de las instancias DatabaseObject.
        Las conexiones se establecen entre los nodos basados en los valores de las instancias DatabaseObject.
        """
        # Crear un grafo NetworkX
        nx_graph = nx.Graph()

        # Agregar nodos al grafo para cada columna y sus valores únicos
        for column in self.column_names:
            nx_graph.add_node(column, label=column)

        # Agregar conexiones entre nodos basadas en los valores de las instancias DatabaseObject
        for obj in self.objects:
            for attr in self.column_names:
                if hasattr(obj, attr):
                    # Obtener el valor del atributo y limpiarlo para evitar errores de Pyvis
                    value = getattr(obj, attr)
                    if isinstance(value, str):
                        value = re.sub(r'[^\x00-\x7F]+', '', value)  # Eliminar caracteres no ASCII

                    # Conectar nodo de la columna con el valor del atributo correspondiente en DatabaseObject
                    nx_graph.add_edge(attr, value)

        # Crear un objeto Network de Pyvis
        graph = Network(filter_menu=True)
        graph.show_buttons()
        # Añadir nodos y bordes desde el grafo NetworkX al objeto Network de Pyvis
        graph.from_nx(nx_graph)

        # Mostrar el grafo interactivo
        graph.show("interactive_graph.html", notebook=False)


class DatabaseObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attributes = ', '.join([f"{attr}={getattr(self, attr)}" for attr in self.__dict__])
        return f"Instancia({attributes})"

    def matches_filters(self, **kwargs):
        """
        Método para verificar si el objeto coincide con los filtros especificados.
        """
        for key, value in kwargs.items():
            if getattr(self, key) != value:
                return False
        return True

def visualize_country_map(csv_file):
    df = pd.read_csv(csv_file)
    countries = df['Country'].unique()
    country_data = pd.DataFrame({'Country': countries})
    fig = px.choropleth(locations=country_data['Country'],
                        locationmode='country names',
                        color=country_data['Country'],
                        hover_name=country_data['Country'],
                        title='Mapa de países mencionados en el dataset')
    fig.update_geos(projection_type="orthographic", showcoastlines=True, coastlinecolor="DarkBlue", showland=True, landcolor="LightGreen")
    fig.show()


def visualize_maturity_level_map(csv_file):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(csv_file)
    relevant_columns = ['Country', 'Nivel_de_madurez_texto_EN']
    df = df[relevant_columns]
    fig = px.choropleth(df,
                        locations='Country',
                        locationmode='country names',
                        color='Nivel_de_madurez_texto_EN',
                        hover_name='Country',
                        title='Mapa de Nivel de Madurez por País',
                        category_orders={'Nivel_de_madurez_texto_EN': ['startup', 'formative', 'established']},
                        color_discrete_map={'startup': 'yellow', 'formative': 'orange', 'established': 'green'})

    fig.update_geos(projection_type="orthographic", showcoastlines=True, coastlinecolor="DarkBlue", showland=True, landcolor="LightGreen")
    fig.show()

if __name__ == "__main__":
    # csv_file = "Advanced_Experiences_in_Cybersecurity_Policies_and_Practices_Data_Set_20240627.csv"
    csv_file = "2016_Cybersecurity_Report_Data_Set_20240627.csv"
    database = Database(csv_file)
    ##database.visualize_dataframe()
    database.plot_interactive_graph()

    #df = pd.read_csv(csv_file)
    # visualize_country_map(csv_file)
    # visualize_maturity_level_map(csv_file)