# PyECs
-- Python Module for Simple Elliptic Curve Manipulation --  
PyECs is primarily designed for educational purposes regarding elliptic curves and elliptic curve cryptography.  Current functionality revolves around addition and scalar multiplication of points on elliptic curves in projective space.  Future work will include more support for elliptic curve cryptographic functions and support for elliptic curves over different number sets (complex, real, etc.)
### Dependencies
- numpy
### Known Bugs/Limitations
- finitePoints (erroneously) generates using the Nagell-Lutz (N-L) theorem, which can sometimes produce points of infinite order
  - Test each point generated using N-L for "finiteness"
- Base point (O) is not handled very well.  It is represented by (inf, inf) (or some combination of +-inf) currently, and will give warnings
  - Create cases to catch whenever a point produced through addition is the base point (points of finite order need this particularly for obvious reasons)
- Points of finite order don't produce base point when multiplied by m except when m = 2
  - Testing required to figure out what is producing the problem
- ECCurves are over the real numbers only
  - Add functionality for the intersection of ECCurves and different fields (complex, real, rational, integers, and finite fields).
