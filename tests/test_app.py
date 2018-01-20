import pytest
import os, sys, shutil

import tozti
import tozti.__main__
import tozti.app

from enum import Enum


@pytest.mark.parametrize("params, expected", 
        [
            ([("a", ["b"], ["c"])], ({"a": ["b"]}, {"a": ["c"]})),
            ([("a", [], ["c"])], ({"a": []}, {"a": ["c"]})),
            ([("a", [], ["c"]), ("b", ["b"], ["c"])], ({"a": [], "b": ["b"]}, {"a": ["c"], "b": ["c"]}))
        ]
        )
def test_dependencygraph_add_node(params, expected):
    """Test for method add_node of class DependencyGraph
    """
    dg = tozti.app.DependencyGraph()
    for name, dep, v in params:
        dg.add_node(name, dep, v)
    expected_deps, expected_values = expected
    assert(dg._dependencies == expected_deps)
    assert(dg._node_value == expected_values)



@pytest.mark.parametrize("dependencies, expected_no_cycle", [
    ({"a": [], "b": []}, True),
    ({"a": ["a"]}, False),
    ({"a": ["b"], "b": ["a"]}, False),
    ({"a": [], "b": ["a"], "c": ["b"]}, True),
    ({"a": [], "b": ["c"], "c": ["b"]}, False),
    ({"a": ["b"], "b": ["c"], "c": ["a"]}, False),
    ({"a": [], "b": ["a"], "c": ["a"]}, True),
    ({"a": [], "b": [], "c": ["a", "b"]}, True),
    ({"a": ["b"], "b": ["a"], "c": ["b", "d"], "d": []}, False),
    ])
def test_dependencygraph_topo_sort(dependencies, expected_no_cycle):
    """Test for method toposort of class DependencyGraph

    Params: 
        dependencies: a graph of dependencies
        expected_no_cycle: True if a toposort exists, False otherwise
    """
    dg = tozti.app.DependencyGraph() 
    for name in dependencies:
        dg.add_node(name, dependencies[name], [name])
    if expected_no_cycle:
        topo_is_correct = True
        order = list(dg.toposort())
        for i, o in enumerate(order):
            for dep in dependencies[o]:
                if order.index(dep) > i:
                    topo_is_correct = False
        assert(topo_is_correct)
    else:
        with pytest.raises(tozti.app.DependencyCycle):
            order = list(dg.toposort())

