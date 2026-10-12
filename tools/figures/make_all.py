"""Regenerate every figure:  python tools/figures/make_all.py
Requires: matplotlib, numpy.   Output: static/img/fig/*.svg
"""
import fig_a, fig_b, fig_c, fig_d, fig_e

for m in (fig_a, fig_b, fig_c, fig_d, fig_e):
    m.run()
print("done")
