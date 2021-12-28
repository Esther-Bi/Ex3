import json
from typing import List

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import queue
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: DiGraph = DiGraph()) -> None:
        self.graph = graph
        self.connected = None

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.graph = DiGraph(file_name)
            self.connected = self.is_connected()
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph.return_dict(), fp=f, indent=4)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        try:
            x = self.graph.nodes[id1]
            y = self.graph.nodes[id1]
            self.dijkstra(id1)
            ans = []
            length = 0
            ans.insert(0, id2)
            while ans[0] != id1:
                key = self.graph.nodes[ans[0]].father
                if key is None:
                    return float('inf'), []
                length += self.graph.all_out_edges_of_node(key).get(ans[0])
                ans.insert(0, key)
            return length, ans
        except:
            return float('inf'), []

    def plot_graph(self) -> None:
        for node_id, node_data in self.graph.nodes.items():
            plt.plot(node_data.x, node_data.y, markersize=6, marker="o", color="red")
            plt.text(node_data.x, node_data.y, str(node_id), color="black", fontsize=10)
        for node_id, node_data in self.graph.nodes.items():
            for dest_node_id, edge_weight in self.graph.nodes[node_id].edge_out.items():
                srcX = self.graph.nodes[node_id].x
                srcY = self.graph.nodes[node_id].y
                destX = self.graph.nodes[dest_node_id].x
                destY = self.graph.nodes[dest_node_id].y
                plt.annotate("", xy=(float(srcX), float(srcY)), xytext=(float(destX), float(destY)),
                            arrowprops=dict(arrowstyle="<-", edgecolor="blue", lw=1.0))
        plt.show()

    def restart(self):
        for n in self.graph.nodes:
            self.graph.nodes[n].father = None
            self.graph.nodes[n].visited = False
            self.graph.nodes[n].weight = float('inf')

    def dijkstra(self, src: int):
        q = queue.PriorityQueue()
        self.restart()
        self.graph.nodes[src].weight = 0
        q.put(self.graph.nodes[src])
        while not q.empty():
            u = q.get()
            if self.graph.all_out_edges_of_node(u.id):
                for node_id, edge_weight in self.graph.all_out_edges_of_node(u.id).items():
                    if not self.graph.nodes[node_id].visited:
                        self.relax(node_id, u)
                        q.put(self.graph.nodes[node_id])
                u.visited = True

    def relax(self, node_id: int, u: int):
        new_weight = u.weight + self.graph.all_out_edges_of_node(u.id).get(node_id)
        if self.graph.nodes[node_id].weight > new_weight:
            self.graph.nodes[node_id].weight = new_weight
            self.graph.nodes[node_id].father = u.id

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if self.graph.mc > 0:
            self.connected = self.is_connected()
        if self.connected:
            ans = []
            dist_all = 0
            i_was_changed = False
            node_i = node_lst[0]
            next = -1
            while node_lst:
                short_path = float('inf')
                next = -1
                dist = 0
                for node_j in node_lst:
                    if node_j != node_i:
                        if not i_was_changed:
                            self.dijkstra(node_i)
                            i_was_changed = True
                        dist = self.graph.nodes[node_j].weight
                        if short_path >= dist:
                            short_path = dist
                            next = node_j
                dist_all = dist_all + dist

                path = []
                path.insert(0, self.graph.nodes[next].father)
                while path[0] != node_i:
                    key = self.graph.nodes[path[0]].father
                    path.insert(0, key)

                ans.extend(path)
                node_lst.remove(node_i)
                node_i = next
                i_was_changed = False
            ans.append(next)
            return ans, dist_all

        if not self.connected:
            return self.tsp_not_connected(node_lst)

    # def TSP(self, node_lst: List[int]) -> (List[int], float):
    #     if self.graph.mc > 0:
    #         self.connected = self.is_connected()
    #     if not self.connected:
    #         for node_i1 in node_lst:
    #             self.dijkstra(node_i1)
    #             for node_i2 in node_lst:
    #                 if self.graph.nodes[node_i2].father is float('inf'):
    #                     return [], float('inf')
    #
    #     ans = []
    #     dist_all = 0
    #     i_was_changed = False
    #     node_i = node_lst[0]
    #     next = -1
    #     while node_lst:
    #         short_path = float('inf')
    #         next = -1
    #         dist = 0
    #         for node_j in node_lst:
    #             if node_j != node_i:
    #                 if not i_was_changed:
    #                     self.dijkstra(node_i)
    #                     i_was_changed = True
    #                 dist = self.graph.nodes[node_j].weight
    #                 if short_path >= dist:
    #                     short_path = dist
    #                     next = node_j
    #         dist_all = dist_all + dist
    #
    #         path = []
    #         path.insert(0, self.graph.nodes[next].father)
    #         while path[0] != node_i:
    #             key = self.graph.nodes[path[0]].father
    #             path.insert(0, key)
    #
    #         ans.extend(path)
    #         node_lst.remove(node_i)
    #         node_i = next
    #         i_was_changed = False
    #     ans.append(next)
    #     return ans, dist_all

    def tsp_not_connected(self, node_lst: List[int]) -> (List[int], float):
        for node_i in node_lst:
            self.dijkstra(node_i)
            for node_i in node_lst:
                if self.graph.nodes[node_i].father is float('inf'):
                    return [], float('inf')
        return [], float('inf')

    def centerPoint(self) -> (int, float):
        if self.graph.mc > 0:
            self.connected = self.is_connected()
        if not self.connected:
            return
        ans = None
        min_num = float('inf')
        for node in self.graph.nodes:
            center = self.center_of_node(node)
            if center < min_num:
                min_num = center
                ans = node
        return ans, min_num

    def center_of_node(self, node_id: int) -> float:
        max_num = float('-inf')
        self.dijkstra(node_id)
        for node in self.graph.nodes:
            if node != node_id:
                temp = self.graph.nodes[node].weight
                if temp >= max_num:
                    max_num = temp
        return max_num

    def is_connected(self) -> bool:
        visited = {}
        k = 0
        for node_id, node_data in self.graph.nodes.items():
            visited[node_id] = False
            k = node_id

        self.BFS(k, visited)
        for node_id, value in visited.items():
            if not value:
                return False

        gr = self.get_transpose()
        graph_transpose = GraphAlgo(gr)
        visited.clear()
        for node_id, node_data in self.graph.nodes.items():
            visited[node_id] = False

        graph_transpose.BFS(k, visited)
        for node_id, value in visited.items():
            if not value:
                return False

        self.graph.mc = 0
        return True

    def BFS(self, node_id: int, visited: dict):
        my_queue = []
        visited.pop(node_id)
        visited[node_id] = True
        my_queue.append(node_id)
        while len(my_queue) != 0:
            node_id = my_queue.pop()
            if self.graph.all_out_edges_of_node(node_id) is not None:
                for key, edge_weight in self.graph.all_out_edges_of_node(node_id).items():
                    if not visited.get(key):
                        visited.pop(key)
                        visited[key] = True
                        my_queue.append(key)

    def get_transpose(self) -> GraphAlgoInterface:
        g = DiGraph()
        for node_id, node_data in self.graph.nodes.items():
            g.add_node(node_id, (node_data.x, node_data.y))
        for node_id, node_data in self.graph.nodes.items():
            for other_node, weight in self.graph.all_out_edges_of_node(node_id).items():
                g.add_edge(other_node, node_id, weight)
        return g
