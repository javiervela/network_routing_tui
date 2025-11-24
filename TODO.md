### TODOs
| Filename | line # | TODO |
|:------|:------:|:------|
| [README.md](README.md#L98) | 98 | run with `uv` or just python |
| [README.md](README.md#L293) | 293 | Write implementation details... |
| [README.md](README.md#L294) | 294 | describe extreme cases |
| [README.md](README.md#L295) | 295 | how to handle "if they cross each other" (?) |
| [src/network_routing_tui/cli.py](src/network_routing_tui/cli.py#L71) | 71 | fail if file not found |
| [src/network_routing_tui/cli.py](src/network_routing_tui/cli.py#L72) | 72 | raise errors from network_routing and catch here to print user-friendly messages |
| [src/network_routing_tui/error.py](src/network_routing_tui/error.py#L1) | 1 | remove |
| [src/network_routing_tui/error.py](src/network_routing_tui/error.py#L2) | 2 | or use this class to pass warnings and erros from network_routing to cli or tui |
| [src/network_routing_tui/graph.py](src/network_routing_tui/graph.py#L18) | 18 | remove |
| [src/network_routing_tui/graph.py](src/network_routing_tui/graph.py#L19) | 19 | handle this errors better using the TUI or CLI |
| [src/network_routing_tui/graph.py](src/network_routing_tui/graph.py#L52) | 52 | our DV does not count-to-infinity ????? |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L88) | 88 | do something about this method |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L97) | 97 | do something about this method |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L105) | 105 | implement |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L155) | 155 | save and load methods for graph and routing tables |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L156) | 156 | add file autocompletion |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L159) | 159 | check edge cases: adding existing edges, removing non-existing edges, or applying algorithms on non-existing nodes |
| [src/network_routing_tui/network_routing.py](src/network_routing_tui/network_routing.py#L160) | 160 | add warnings and errors: when the nodes do not exist from CLI or TUI |
| [src/network_routing_tui/routing_table.py](src/network_routing_tui/routing_table.py#L17) | 17 | change show naming |
| [src/network_routing_tui/tui.py](src/network_routing_tui/tui.py#L128) | 128 | implement save routing table button |
| [src/network_routing_tui/tui.py](src/network_routing_tui/tui.py#L193) | 193 | how to ask for both node and filename? |
| [src/network_routing_tui/tui.py](src/network_routing_tui/tui.py#L266) | 266 | implement print routing table command? |

### REMOVEs
| Filename | line # | REMOVE |
|:------|:------:|:------|
| [src/network_routing_tui/graph.py](src/network_routing_tui/graph.py#L14) | 14 | edge if exists, else warn |
| [src/network_routing_tui/graph.py](src/network_routing_tui/graph.py#L21) | 21 | nodes if they have no remaining edges |
