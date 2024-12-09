```                        +----------------------------------------------------------+
                          |                       AWS Cloud                           |
                          |                                                           |
                          |                                                           |
    +------------------------+                            +---------------------------+
    |    EC2 Instance 1       |                           |     EC2 Instance 2         |
    |    Backend System       |                           |     PokeAPI Game           |
    |                         |                           |                            |
    |   +------------------+  |                           |   +-------------------+    |
    |   | Docker Container  | |                           |   | PokeAPI Game App  |    |
    |   |    Flask API      | | <------------------------>|   |      Python       |    |
    |   +------------------+  | HTTP Request              |    +-------------------+   |
    |           ^             |                           |                            |
    |           |             |                           |                            |
    |   +------------------+  |                           |                            |
    |   | Docker Container  | |                           |                            |
    |   |    MongoDB        | |                           |                            |
    |   +------------------+  |                            +---------------------------+
    |                         |                           |
    +-------------------------+
                               ---------+-----------------
                                        |
                                        |
                   +----------------------+--------------------+
                   |  AWS Security Group (allows HTTP traffic) |
                   +-------------------------------------------+

