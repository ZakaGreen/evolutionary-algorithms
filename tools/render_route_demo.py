from pathlib import Path
import json
import os
import random
import runpy
import sys

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT / '.demo-cache'
ROOT.mkdir(exist_ok=True)
os.environ['MPLBACKEND'] = 'Agg'
os.environ['MPLCONFIGDIR'] = str(ROOT / 'mpl-cache')
sys.path.insert(0, str(PROJECT))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import io

random.seed(42)
np.random.seed(42)
plt.show = lambda: None
ns = runpy.run_path(str(PROJECT / 'Cv_3.py'), run_name='__main__')
plt.close('all')

routes = ns['best_jedinec']
history = ns['best_fit']
points = np.asarray(ns['B'])
assert routes.shape == (500, 25)
for route, cost in zip(routes, history):
    route = route.astype(int)
    assert np.array_equal(np.sort(route), np.arange(25))
    assert route[0] == 0 and route[-1] == 24
    length = np.linalg.norm(np.diff(points[route], axis=0), axis=1).sum()
    assert np.isclose(length, cost)
assert np.all(np.diff(history) <= 1e-7)

palette = {'bg': '#090d11', 'cream': '#f3e2c3', 'red': '#c2523a', 'muted': '#a39b8c', 'grid': '#282c2f'}
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'figure.facecolor': palette['bg'],
    'axes.facecolor': palette['bg'], 'text.color': palette['cream'],
    'axes.labelcolor': palette['muted'], 'xtick.color': palette['muted'],
    'ytick.color': palette['muted'], 'axes.edgecolor': palette['grid'],
    'font.size': 9,
})
frames = []
indices = np.unique(np.r_[np.linspace(0, 499, 44).astype(int), 499])
for frame, generation in enumerate(indices):
    fig, (ax, progress) = plt.subplots(1, 2, figsize=(8.8, 4.1), dpi=100,
                                      gridspec_kw={'width_ratios': [1.15, 1]})
    fig.subplots_adjust(left=.07, right=.96, bottom=.19, top=.77, wspace=.30)
    fig.text(.07, .92, 'A ROUTE, IMPROVED ONE GENERATION AT A TIME', fontsize=12,
             weight='bold', color=palette['cream'])
    fig.text(.07, .85, 'Genetic-algorithm coursework · Ilia Liubotin', fontsize=10, color=palette['muted'])
    route = routes[generation].astype(int)
    ax.plot(points[route, 0], points[route, 1], color=palette['red'], linewidth=1.7, zorder=1)
    ax.scatter(points[:-1, 0], points[:-1, 1], s=23, color=palette['cream'], edgecolor=palette['bg'], linewidth=.5, zorder=2)
    ax.scatter([0], [0], marker='s', s=45, color=palette['red'], edgecolor=palette['cream'], linewidth=1, zorder=3)
    ax.set_xlim(-8, 108)
    ax.set_ylim(-8, 108)
    ax.set_aspect('equal')
    ax.set_xticks([0, 50, 100])
    ax.set_yticks([0, 50, 100])
    ax.spines[['top', 'right']].set_visible(False)
    progress.plot(np.arange(1, generation + 2), history[:generation + 1], color=palette['red'], linewidth=2)
    progress.scatter([generation + 1], [history[generation]], color=palette['cream'], s=22, zorder=3)
    progress.set_xlim(1, 500)
    progress.set_ylim(history.min() * .94, history.max() * 1.05)
    progress.set_xlabel('Generation')
    progress.set_ylabel('Best route length')
    progress.spines[['top', 'right']].set_visible(False)
    progress.grid(axis='y', color=palette['grid'], linewidth=.5)
    fig.text(.07, .065, f'Generation {generation + 1:03d} / 500', fontsize=10, family='DejaVu Sans Mono')
    fig.text(.48, .065, f'Route length: {history[generation]:.1f}', fontsize=10, family='DejaVu Sans Mono')
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, facecolor=palette['bg'])
    buffer.seek(0)
    frames.append(Image.open(buffer).convert('RGB'))
    if generation == 499:
        fig.savefig(PROJECT / 'assets' / 'route-search-final.png', dpi=160, facecolor=palette['bg'])
    plt.close(fig)

durations = [150] * len(frames)
durations[-1] = 2500
frames[0].save(PROJECT / 'assets' / 'route-search.gif', save_all=True, append_images=frames[1:],
               duration=durations, loop=0, optimize=True)
metrics = {
    'seed': 42, 'python_random_and_numpy_seeded': True,
    'original_script_runs': 10, 'shown_run': 10, 'generations': 500, 'population': 100,
    'initial_length': float(history[0]), 'final_length': float(history[-1]),
    'route_validity': 'All 500 shown-generation routes checked against input points and fitness.',
    'note': 'Illustration of one deterministic demonstration run, not an optimality or benchmark claim.',
}
(PROJECT / 'assets' / 'demo-metadata.json').write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2), flush=True)
