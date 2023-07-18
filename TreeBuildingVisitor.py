from antlr4.tree.Tree import TerminalNode
from graphviz import Digraph
from dist.yaplVisitor import yaplVisitor

class TreeBuildingVisitor(yaplVisitor):
    def __init__(self):
        super().__init__()
        self.graph = Digraph()
        self.node_id = 0

    def visit(self, tree):
        node_label = self.getNodeLabel(tree)
        self.graph.node(str(self.node_id), node_label)
        parent_id = self.node_id
        self.node_id += 1

        if not isinstance(tree, TerminalNode):  # Check if node is not terminal
            for child in tree.children:  # Now we can safely access children
                self.graph.edge(str(parent_id), str(self.node_id))
                self.visit(child)

    def getNodeLabel(self, node):
        if isinstance(node, TerminalNode):
            return node.getText()
        else:
            class_name = type(node).__name__
            # Assume class_name is in the format GrammarNameParser.RuleNameContext
            rule_name = class_name.split('.')[1] if '.' in class_name else class_name
            # Remove the trailing 'Context' from the rule name
            rule_name = rule_name[:-7] if rule_name.endswith('Context') else rule_name
            return rule_name

    def getDotGraph(self):
        return self.graph

