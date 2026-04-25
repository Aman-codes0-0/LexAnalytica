import networkx as nx

class GraphEngine:
    def __init__(self):
        # We use a directed graph to represent knowledge
        self.graph = nx.DiGraph()
    
    def add_document_entities(self, doc_id: str, entities: dict):
        """
        Ingest extracted entities from a document into the Knowledge Graph.
        """
        # Create a central node for the Document
        self.graph.add_node(doc_id, type="DOCUMENT", label=f"Doc: {doc_id}")

        for entity_type, entity_list in entities.items():
            if not isinstance(entity_list, list):
                continue
            
            for entity in entity_list:
                # Use entity name as node ID for deduplication across documents
                node_id = f"{entity_type}:{entity}"
                
                # Add or update the entity node
                if not self.graph.has_node(node_id):
                    self.graph.add_node(node_id, type=entity_type.upper(), label=entity)
                
                # Connect Document to Entity
                # We can deduce relationships based on type
                if entity_type == 'persons':
                    rel = "MENTIONS_PERSON"
                elif entity_type == 'organizations':
                    rel = "MENTIONS_ORG"
                elif entity_type == 'locations':
                    rel = "MENTIONS_LOC"
                elif entity_type == 'case_numbers':
                    rel = "CITES_CASE"
                elif entity_type == 'law_sections':
                    rel = "REFERENCES_LAW"
                else:
                    rel = "MENTIONS"
                
                self.graph.add_edge(doc_id, node_id, relation=rel)
                
                # In a more advanced setup, Legal-BERT relationship extraction would
                # dictate edges between two entities (e.g., PERSON -(CEO_OF)-> ORG).
                # For this baseline, we connect everything through the Document.

    def query_graph(self, query: str) -> dict:
        """
        Retrieval augmented generation using Graph Traversal.
        For example, find all documents citing a specific law section.
        """
        # This is a simplified Graph retrieval.
        # In reality, you would map the natural language query to a graph node.
        # Here we do a basic keyword search on node labels.
        query_lower = query.lower()
        matched_nodes = []
        
        for node, data in self.graph.nodes(data=True):
            if query_lower in data.get('label', '').lower():
                matched_nodes.append(node)

        results = {}
        for node in matched_nodes:
            # Find neighbors (e.g., what documents mention this entity?)
            neighbors = list(self.graph.neighbors(node))
            predecessors = list(self.graph.predecessors(node))
            
            connected_docs = []
            for pred in predecessors:
                pred_data = self.graph.nodes[pred]
                if pred_data.get('type') == 'DOCUMENT':
                    connected_docs.append(pred)

            results[node] = {
                "node_data": self.graph.nodes[node],
                "mentioned_in": connected_docs,
                "connections_count": len(neighbors) + len(predecessors)
            }
            
        return results

    def get_graph_summary(self) -> dict:
        """Return basic statistics about the Knowledge Graph."""
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges()
        }

# Global singleton for in-memory graph
global_graph = GraphEngine()
