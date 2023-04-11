# pylint: disable=wrong-import-position
"""
Compositioner module helps to create optimal plants compositions taking into an account their
cohabitations and possible limitation factors
"""
import os
if "USE_PYGEOS" not in os.environ:
    os.environ["USE_PYGEOS"] = "0" # remove this if some Shapely 2.0 incompatibility is found

from .get_combined import get_adjacency_graph, write_combined_graph_gexf
from .get_compatability import (
    get_compatability_for_species,
    get_compatability_graph,
    write_compatability_for_species_gexf,
    write_compatability_graph_gexf,
)
from .get_composition import (
    get_composition_unknown,
    get_recommended_composition,
    get_species_composition_old,
    get_updated_composition,
    write_composition_unknown_gfsx,
    write_recommended_composition_gexf,
    write_updated_composition_gexf,
)
from .get_optimal_resolution import get_best_resolution
