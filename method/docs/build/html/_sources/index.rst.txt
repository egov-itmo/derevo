.. derevo documentation master file, created by
    sphinx-quickstart on Mon Jul 10 13:50:00 2023.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to **derevo**'s documentation!
======================================

Content:
========

**derevo** is a library that allows to generate plants compositions
based on the territory limitations and outer factors.

User defines available list of plants, including their planting restrictions
such as climate zone preferences, soil acidity/fertility/type preferences,
humidity preferences and genus (single form of genera).

Genera cohabitation matrix should also be defined to ensure that plants are in
the generated compositions cohabitate well.

The main method is presented with `get_compositions` function.

Source code is available at GitHub: https://github.com/egov-itmo/derevo.

.. toctree::
    :maxdepth: 1

    derevo/index
    components/index
