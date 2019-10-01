# PyECs
Python Module for Simple Elliptic Curve Manipulation
### Dependencies
- numpy
### Known Bugs
- finitePoints generates using the Nagell-Lutz theorem, which can sometimes produce points of infinite order
- Base point (O) is not handled very well in general currently
- Points of finite order don't produce base point when multiplied by m except when m = 2
