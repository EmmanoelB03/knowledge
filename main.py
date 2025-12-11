import matplotlib.pyplot as plt
import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = {}
    
    def add(self, name, type, property=None):
        if property is None:
            property = {}
        if name not in self.graph:
            self.graph[name] = {
                "type": type,
                "props": property,
                "conections": []
            }
    
    def addRelations(self, origin, destination, relation_name):
        if origin not in self.graph or destination not in self.graph:
            return
        new_relation = {"destination": destination, "relation": relation_name}
        self.graph[origin]["conections"].append(new_relation)
    
    def removeNode(self, name):

        if name not in self.graph:
            print(f"Nó '{name}' não encontrado no grafo.")
            return False

        del self.graph[name]

        for node_name in self.graph:
            self.graph[node_name]["conections"] = [
                conn for conn in self.graph[node_name]["conections"]
                if conn["destination"] != name
            ]
        
        print(f"Nó '{name}' removido com sucesso!")
        return True
    
    def seeConections(self, name):
        if name not in self.graph:
            print("Nó não encontrado.")
            return
        node_data = self.graph[name] 
        print(f"--- Conexões de {name} ({node_data['type']}) ---")
        found = False
        for item in node_data["conections"]:
            print(f" -> [{item['relation']}] -> {item['destination']}")
            found = True  
        if not found:
            print(" -> Nenhuma conexão encontrada.")
    
    def exibir_visualizacao(self):
        G = nx.DiGraph()
        lista_santa = []
        lista_jogadores = []
        lista_clubes = []
        
        for origem, dados in self.graph.items():
            tipo = dados['type']
            if tipo == "Clube Origem":
                lista_santa.append(origem)
            elif tipo == "Jogador":
                lista_jogadores.append(origem)
            else:
                lista_clubes.append(origem)
            
            G.add_node(origem)
            
            for conexao in dados["conections"]:
                G.add_edge(origem, conexao["destination"], label=conexao["relation"])
        
        pos = nx.shell_layout(G, nlist=[lista_santa, lista_jogadores, lista_clubes])
        
        plt.figure(figsize=(15, 12))
        nx.draw_networkx_nodes(G, pos, nodelist=lista_santa, node_color='#ff0000', node_size=8000, label="Santa")
        nx.draw_networkx_nodes(G, pos, nodelist=lista_jogadores, node_color='#87CEFA', node_size=2000)
        nx.draw_networkx_nodes(G, pos, nodelist=lista_clubes, node_color='#90EE90', node_size=3000)
        
        pos_labels = {k: (v[0], v[1]) for k, v in pos.items()} 
        nx.draw_networkx_labels(G, pos_labels, font_size=9, font_weight="bold", 
                                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.4, 
                              arrows=True, arrowsize=20, 
                              connectionstyle='arc3, rad=0.1')
        
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                     font_size=7, label_pos=0.4,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))
        
        plt.title("Transferências do Santa Cruz (2016 -> 2017)", fontsize=16)
        plt.axis('off')
        print("Salvo como 'grafo_limpo.png'")
        plt.savefig("grafo_limpo.png", dpi=300, bbox_inches='tight')


kg = KnowledgeGraph()
kg.add("Santa Cruz", "Clube Origem")

transferencias = [
    ("Grafite", "Atacante", "Athletico-PR"),
    ("Keno", "Atacante", "Palmeiras"),
    ("João Paulo", "Meia", "Botafogo"),
    ("Léo Moura", "Lateral", "Grêmio"),
    ("Tiago Cardoso", "Goleiro", "Náutico"),
    ("Vítor", "Lateral", "Goiânia"),
    ("Neris", "Zagueiro", "Sport"),
    ("Uillian Correia", "Volante", "Vitória"),
    ("Arthur Caíke", "Atacante", "Chapecoense"),
    ("Allan Vieira", "Lateral", "Fortaleza")
]

for jogador, posicao, clube_destino in transferencias:
    kg.add(jogador, "Jogador")
    kg.add(clube_destino, "Clube Destino")
    kg.addRelations("Santa Cruz", jogador, "jogou") 
    kg.addRelations(jogador, clube_destino, "foi para")

kg.seeConections('Tiago Cardoso')

print("\n" + "="*50 + "\n")

print("\n" + "="*50 + "\n")

print("Tentando ver conexões após remoção:")
kg.seeConections('Tiago Cardoso')

print("\n" + "="*50 + "\n")

kg.exibir_visualizacao()