"""Tic-Tac-Toe directed graph with symmetry, outcome weights, and a move bot.

Internal boards are 9-element lists containing 'X', 'O', or '.'.
The human-facing board displays empty squares as 1 through 9.

An edge represents one legal move. Different parents can share the same child.
The weights count *complete move sequences* (not unique terminal nodes).
Each node stores its board in the orientation first encountered when building.
"""

import json
import random
from pathlib import Path
from collections import deque

EMPTY = "."
LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def gStatus(board):
    """Return 'X', 'O', 'Draw', or 'No winner'."""
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return f"{board[a]} wins" 
    return "Draw" if EMPTY not in board else "No winner"


def print_board(board):
    """Show positions 1..9 for empty cells; storage remains '.' internally."""
    visible = [v if v != EMPTY else str(i + 1) for i, v in enumerate(board)]
    for row in range(3):
        print(" | ".join(visible[3 * row:3 * row + 3]))
        if row != 2:
            print("--+---+--")


def rotate_board(board):
    """Return a board rotated 90 degrees clockwise."""
    return [board[i] for i in (6, 3, 0, 7, 4, 1, 8, 5, 2)]


def reflect_board(board):
    """Return the horizontal mirror image of a board."""
    return [board[i] for i in (2, 1, 0, 5, 4, 3, 8, 7, 6)]


def transform_board(board, rotations=0, flips=0):
    """Reflect first (if needed), then rotate clockwise."""
    result = list(board)
    if flips % 2:
        result = reflect_board(result)
    for _ in range(rotations % 4):
        result = rotate_board(result)
    return result


def restore_board(board, rotations, flips):
    """Undo transform_board for a board."""
    result = list(board)
    for _ in range((-rotations) % 4):
        result = rotate_board(result)
    if flips % 2:
        result = reflect_board(result)
    return result


def restore_move(position, rotations, flips):
    """Convert a position on a STORED board to a position on the player's board."""
    return transform_board(list(range(9)), rotations, flips).index(position)


def winning_moves(board, player):
    """Find empty positions at which player would immediately win.

    This also works hypothetically when it is not currently player's turn.
    """
    winning = []
    if gStatus(board) != "No winner":
        return winning
    for i, cell in enumerate(board):
        if cell != EMPTY:
            continue
        test = list(board)
        test[i] = player
        if gStatus(test) == player:
            winning.append(i)
    return winning


def fork_moves(board, player):
    """Return moves creating two or more distinct immediate winning squares."""
    forks = []
    if gStatus(board) != "No winner":
        return forks

    for i, cell in enumerate(board):

        if cell != ".":
            continue

        trial = board.copy()
        trial[i] = player

        if gStatus(trial) != "No winner":
            continue

        if len(winning_moves(trial, player)) >= 2:
            forks.append(i)

    return forks


class TicGraph:
    def __init__(self):
        self.nodes = {}        # node ID -> board/turn/result/children/weights/policy
        self.board_index = {}  # ANY board orientation + turn -> (id, rotation, flip)
        self.next_id = 0

    def key(self, board, turn):
        return "".join(board) + ":" + turn

    def find(self, board, turn):
        """One dictionary lookup: (node ID, rotation, flip) or None."""
        return self.board_index.get(self.key(board, turn))

    def get_or_add(self, board, turn):
        """Reuse an existing symmetric node, otherwise create a new one."""
        match = self.find(board, turn)
        if match is not None:
            return match[0], False

        node_id = str(self.next_id)
        self.next_id += 1
        self.nodes[node_id] = {
            "board": list(board),
            "turn": turn,                   # Player to move NEXT (not last mover)
            "result": gStatus(board),
            "children": {},                 # stored-board move index -> child node ID
        }

        # First board encountered is the stored orientation. Every symmetric
        # variant points to that same node; no runtime rotation search needed.
        for flips in range(2):
            for rotations in range(4):
                variant = transform_board(board, rotations, flips)
                key = self.key(variant, turn)
                self.board_index.setdefault(key, (node_id, rotations, flips))
        return node_id, True

    def expand(self, node_id):
        """Create all legal outgoing edges; reuse children if they exist."""
        node = self.nodes[node_id]
        created_ids = []
        if node["result"] != "No winner":
            return created_ids

        next_turn = "O" if node["turn"] == "X" else "X"
        for position, cell in enumerate(node["board"]):
            if cell != EMPTY:
                continue
            next_board = node["board"].copy()
            next_board[position] = node["turn"]
            child_id, created = self.get_or_add(next_board, next_turn)
            node["children"][str(position)] = child_id
            if created:
                created_ids.append(child_id)
        return created_ids

    def build(self):
        """Build the complete graph and precompute all weights / best moves."""
        root_id, _ = self.get_or_add([EMPTY] * 9, "X")
        queue = deque([root_id])
        visited = set()
        while queue:
            node_id = queue.popleft()
            if node_id in visited:
                continue
            visited.add(node_id)
            self.expand(node_id)
            queue.extend(self.nodes[node_id]["children"].values())
        self.calculate_weights()
        return root_id

    def calculate_weights(self):
        """Count every possible ending from each node and solve minimax.

        Weights are always from X's perspective: X wins, draws, O wins.
        Every move edge is counted, even if two edges reach a shared node.
        Minimax value is +1 if X can force a win, 0 for draw, -1 for O win.
        """
        # Nodes with fewer remaining squares come first: children before parents.
        order = sorted(self.nodes, key=lambda i: self.nodes[i]["board"].count(EMPTY))
        for node_id in order:
            node = self.nodes[node_id]
            outcome = node["result"]
            if outcome != "No winner":
                node["weights"] = {
                    "X": int(outcome == "X"),
                    "Draw": int(outcome == "Draw"),
                    "O": int(outcome == "O"),
                }
                node["value"] = {"X": 1, "O": -1, "Draw": 0}[outcome]
                node["distance"] = 0
                node["best_move"] = None
                node["best_win_move"] = None
                node["reason"] = "game over"
                continue

            if len(node["children"]) != node["board"].count(EMPTY):
                raise ValueError("Incomplete graph: expand all positions before weighting")

            children = [self.nodes[cid] for cid in node["children"].values()]
            node["weights"] = {
                result: sum(child["weights"][result] for child in children)
                for result in ("X", "Draw", "O")
            }
            child_values = [child["value"] for child in children]
            node["value"] = (max if node["turn"] == "X" else min)(child_values)
            distances = [c["distance"] for c in children if c["value"] == node["value"]]
            perspective = node["value"] if node["turn"] == "X" else -node["value"]
            node["distance"] = 1 + (max(distances) if perspective < 0 else min(distances))

        # Once all child outcomes are known, calculate a stored-board policy.
        for node in self.nodes.values():
            if node["result"] == "No winner":
                node["best_move"], node["reason"] = self._select_move(node, 2)
                node["best_win_move"], _ = self._select_move(node, 1)

    def _select_move(self, node, level):
        """Select in stored orientation; level 1 counts paths, level 2 plays safely."""
        player = node["turn"]
        opponent = "O" if player == "X" else "X"
        board = node["board"]
        options = [int(i) for i in node["children"]]

        def child_at(i):
            return self.nodes[node["children"][str(i)]]

        def counts(i):
            w = child_at(i)["weights"]
            return (w[player], -w[opponent], w["Draw"], -i)

        if level == 1:
            return max(options, key=counts), "most winning paths"

        immediate = winning_moves(board, player)
        if immediate:
            return immediate[0], "immediate win"
        threats = winning_moves(board, opponent)
        safe = []
        for i in options:
            trial = board.copy()
            trial[i] = player
            if not winning_moves(trial, opponent):
                safe.append(i)
        if safe:
            options = safe

        def score(i):
            child = child_at(i)
            outcome = child["value"] if player == "X" else -child["value"]
            trial = board.copy()
            trial[i] = player
            own_threats = len(winning_moves(trial, player))
            # Check every opponent reply, not just hypothetical fork squares.
            # A reply is dangerous only if its fork cannot be answered by
            # our immediate win, and the reply does not already end the game.
            dangerous = 0
            for j, cell in enumerate(trial):
                if cell != EMPTY:
                    continue
                reply = trial.copy()
                reply[j] = opponent
                if gStatus(reply) == "No winner" and not winning_moves(reply, player):
                    if len(winning_moves(reply, opponent)) >= 2:
                        dangerous += 1
            timing = -child["distance"] if outcome > 0 else child["distance"] if outcome < 0 else 0
            # Minimax prevents sacrificing a guaranteed win/draw for a threat.
            return (outcome, timing, -dangerous, min(own_threats, 2), *counts(i))

        move = max(options, key=score)
        if threats:
            reason = "block immediate loss" if safe else "no complete block available"
        else:
            trial = board.copy()
            trial[move] = player
            reason = "safe double threat" if len(winning_moves(trial, player)) >= 2 and not winning_moves(trial, opponent) else "optimal outcome / fork safety"
        return move, reason

    def child_from_move(self, board, turn, position):
        """Get the child node reached by playing index 0..8 on THIS board."""
        match = self.find(board, turn)
        if match is None:
            raise ValueError("Board/turn is invalid, unreachable, or not in the graph")
        if not 0 <= position < 9 or board[position] != EMPTY:
            raise ValueError("Choose an empty square (index 0..8)")
        node_id, rotations, flips = match
        # Query orientation -> stored orientation for edge lookup.
        stored_positions = transform_board(list(range(9)), rotations, flips)
        return self.nodes[node_id]["children"].get(str(stored_positions[position]))

    def choose_move(self, board, player, level=2):
        """Return a legal index 0..8, or None if the game has ended.

        0: random; 1: most winning paths; 2: optimal with fork safety.
        Player is case insensitive. Board cells are X/O/.
        """
        if type(level) is not int or level not in (0, 1, 2):
            raise ValueError("Level must be 0, 1 or 2")
        if not isinstance(player, str) or player.upper() not in ("X", "O"):
            raise ValueError("Player must be X or O")
        player = player.upper()
        if len(board) != 9 or any(c not in ("X", "O", EMPTY) for c in board):
            raise ValueError("Board must have exactly nine X/O/. cells")
        match = self.find(board, player)
        if match is None:
            raise ValueError("Board and player are not reachable from a legal game")
        node_id, rotations, flips = match
        node = self.nodes[node_id]
        if node["result"] != "No winner":
            return None
        if level == 0:
            return random.choice([i for i, cell in enumerate(board) if cell == EMPTY])
        field = "best_move" if level == 2 else "best_win_move"
        return restore_move(node[field], rotations, flips)

    def describe_move(self, board, player, level=2):
        """Return structured information about one chosen move."""
        move = self.choose_move(board, player, level)
        player = player.upper()
        node_id, _, _ = self.find(board, player)
        node = self.nodes[node_id]
        if move is None:
            return {"move": None, "status": node["result"]}
        child_id = self.child_from_move(board, player, move)
        child = self.nodes[child_id]
        return {
            "move": move,
            "square": move + 1,
            "reason": node["reason"] if level == 2 else "most winning paths" if level == 1 else "random move",
            "outcomes_after_move": child["weights"].copy(),
            "guaranteed_outcome": {1: "X", 0: "Draw", -1: "O"}[child["value"]],
            "moves_to_outcome": child["distance"] + 1,
            "child_id": child_id,
        }

    def save(self, path="tic_graph.json"):
        """Persist the built graph (including scores/policies) to JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"nodes": self.nodes,
                       "board_index": self.board_index,
                       "next_id": self.next_id, "policy_version": 2}, f, separators=(",", ":"))

    @classmethod
    def load(cls, path="tic_graph.json"):
        """Load the ready-to-use graph; upgrade older unweighted files in RAM."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        graph = cls()
        graph.nodes = data["nodes"]
        graph.board_index = data["board_index"]
        graph.next_id = data["next_id"]
        if graph.nodes and data.get("policy_version") != 2:
            graph.calculate_weights()
        return graph


_graph = None


def bot(board, player, level=2):
    """Convenience entry point: load the saved graph once and return a move."""
    global _graph
    if _graph is None:
        path = Path(__file__).with_name("tic_graph.json")
        if path.exists():
            _graph = TicGraph.load(path)
        else:
            _graph = TicGraph()
            _graph.build()
    return _graph.choose_move(board, player, level)


if __name__ == "__main__":
    graph = TicGraph()
    root = graph.build()
    graph.save(Path(__file__).with_name("tic_graph.json"))
    print("Nodes:", len(graph.nodes), "Indexed orientations:", len(graph.board_index))
    print("X wins / Draws / O wins:", graph.nodes[root]["weights"])
    board = ["X", "X", ".", ".", "O", ".", ".", ".", "."]
    print_board(board)
    print("O to move:", graph.describe_move(board, "O"))
