import unittest
from src.Node import Node
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):
    global g_algo
    g_algo = GraphAlgo()
    for n in range(5):
        g_algo.get_graph().add_node(n)
    g_algo.get_graph().add_edge(0, 2, 1)
    g_algo.get_graph().add_edge(0, 1, 0.3)
    g_algo.get_graph().add_edge(1, 0, 1.1)
    g_algo.get_graph().add_edge(1, 2, 1.3)
    g_algo.get_graph().add_edge(2, 1, 1.3)
    g_algo.get_graph().add_edge(3, 2, 0.1)
    g_algo.get_graph().add_edge(2, 3, 1.1)
    g_algo.get_graph().add_edge(1, 3, 0.2)
    g_algo.get_graph().add_edge(1, 4, 1.9)

    global g_algo_2
    g_algo_2 = GraphAlgo()

    def test_shortest_path(self):
        self.assertEqual(g_algo.shortest_path(0, 2), (0.6000000000000001, [0, 1, 3, 2]))

    def test_get_graph(self):
        self.assertEqual(g_algo.get_graph(), g_algo.graph)

    def test_dijkstra(self):
        g_algo.dijkstra(0)
        self.assertEqual(g_algo.get_graph().nodes[2].father, 3)
        self.assertEqual(g_algo.get_graph().nodes[4].father, 1)

    def test_centerPoint(self):
        g_algo_2.load_from_json('../data/A0.json')
        self.assertEqual(g_algo_2.centerPoint(), (7, 6.806805834715163))
        g_algo_2.load_from_json('../data/A1.json')
        self.assertEqual(g_algo_2.centerPoint(), (8, 9.925289024973141))
        g_algo_2.load_from_json('../data/A2.json')
        self.assertEqual(g_algo_2.centerPoint(), (0, 7.819910602212574))
        g_algo_2.load_from_json('../data/A3.json')
        self.assertEqual(g_algo_2.centerPoint(), (2, 8.182236568942237))
        g_algo_2.load_from_json('../data/A4.json')
        self.assertEqual(g_algo_2.centerPoint(), (6, 8.071366078651435))
        g_algo_2.load_from_json('../data/A5.json')
        self.assertEqual(g_algo_2.centerPoint(), (40, 9.291743173960954))

    def test_is_connected(self):
        g_algo_2.load_from_json('../data/A0.json')
        self.assertEqual(g_algo_2.is_connected(), True)
        g_algo_2.get_graph().remove_edge(1, 0)
        g_algo_2.get_graph().remove_edge(1, 2)
        g_algo_2.get_graph().remove_edge(1, 3)
        g_algo_2.get_graph().remove_edge(1, 4)
        g_algo_2.get_graph().remove_edge(1, 5)
        g_algo_2.get_graph().remove_edge(1, 6)
        g_algo_2.get_graph().remove_edge(1, 7)
        g_algo_2.get_graph().remove_edge(1, 8)
        g_algo_2.get_graph().remove_edge(1, 9)
        g_algo_2.get_graph().remove_edge(1, 10)
        self.assertEqual(g_algo_2.is_connected(), False)
        g_algo_2.load_from_json('../data/A1.json')
        self.assertEqual(g_algo_2.is_connected(), True)
        g_algo_2.load_from_json('../data/A2.json')
        self.assertEqual(g_algo_2.is_connected(), True)
        g_algo_2.load_from_json('../data/A3.json')
        self.assertEqual(g_algo_2.is_connected(), True)
        g_algo_2.load_from_json('../data/A4.json')
        self.assertEqual(g_algo_2.is_connected(), True)
        g_algo_2.load_from_json('../data/A5.json')
        self.assertEqual(g_algo_2.is_connected(), True)

    def test_BFS(self):
        g_algo_2.load_from_json('../data/A0.json')
        visited = {}
        k = 0
        for node_id, node_data in g_algo_2.graph.nodes.items():
            visited[node_id] = False
            k = node_id
        g_algo_2.BFS(k, visited)
        self.assertEqual(visited[1], True)
        g_algo_2.get_graph().remove_edge(1, 0)
        g_algo_2.get_graph().remove_edge(1, 2)
        g_algo_2.get_graph().remove_edge(1, 3)
        g_algo_2.get_graph().remove_edge(1, 4)
        g_algo_2.get_graph().remove_edge(1, 5)
        g_algo_2.get_graph().remove_edge(1, 6)
        g_algo_2.get_graph().remove_edge(1, 7)
        g_algo_2.get_graph().remove_edge(1, 8)
        g_algo_2.get_graph().remove_edge(1, 9)
        g_algo_2.get_graph().remove_edge(1, 10)
        g_algo_2.get_graph().remove_edge(10, 1)
        g_algo_2.get_graph().remove_edge(9, 1)
        g_algo_2.get_graph().remove_edge(8, 1)
        g_algo_2.get_graph().remove_edge(7, 1)
        g_algo_2.get_graph().remove_edge(6, 1)
        g_algo_2.get_graph().remove_edge(5, 1)
        g_algo_2.get_graph().remove_edge(4, 1)
        g_algo_2.get_graph().remove_edge(3, 1)
        g_algo_2.get_graph().remove_edge(2, 1)
        g_algo_2.get_graph().remove_edge(0, 1)
        visited = {}
        for node_id, node_data in g_algo_2.graph.nodes.items():
            visited[node_id] = False
        g_algo_2.BFS(3, visited)
        self.assertEqual(visited[1], False)

    def test_TSP(self):
        self.assertEqual(g_algo.TSP([2, 1, 4, 0]), [0, 2, 1, 4], 7)

if __name__ == '__main__':
    unittest.main()
