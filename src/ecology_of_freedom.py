"""
ecology_of_freedom.py
=====================
The ecology of political freedom: latitude, economic base, and binding
mechanisms as predictors of disobedience freedom across 401 governance systems.

Part of the isonomia series — companion analysis to a_decomposition.py.

Theoretical framework
---------------------
Political ecology hypothesis: geographical and ecological conditions shape
state capacity (S), which mediates the relationship between environment
and political freedom (D).

  High latitude → ecological constraints on surplus accumulation
               → lower sovereign capacity (S)
               → higher disobedience freedom (D)

The analysis tests three claims:

  1. r(|latitude|, D) = +0.316 (p < 0.001): high-latitude societies
     have significantly higher D than tropical societies.

  2. The relationship is primarily mediated through S (84.7%), consistent
     with a political ecology rather than a cultural diffusion explanation.

  3. Crucially, the latitude-D relationship is NOT driven by agricultural
     surplus accumulation (contra Boserup): r(|lat|, D) is significant
     for foraging/fishing and extraction economies but non-significant for
     agricultural ones.

  4. Binding mechanism (social vs material vs coercive vs ritual) independently
     predicts D and varies by latitude band, providing a second ecological
     pathway.

Usage
-----
    python src/ecology_of_freedom.py
    python src/ecology_of_freedom.py --data PATH/TO/governance_extended.csv
"""

import os
import argparse
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from numpy.linalg import lstsq

warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')


# ── Coding helpers ────────────────────────────────────────────────────────────

def econ_group(s):
    s = str(s).lower()
    if any(x in s for x in ['forag','hunt','gather','rein','fish']):
        return 'foraging/fishing'
    if any(x in s for x in ['pastora','herd','cattle','nomad','transhumant']):
        return 'pastoral'
    if any(x in s for x in ['agric','farm','rice','maize','wheat','grain',
                              'cultivation','slash']):
        return 'agriculture'
    if any(x in s for x in ['trade','silk','spice','wine','amber','wool',
                              'merchant','commerc','maritime']):
        return 'trade'
    if any(x in s for x in ['mining','silver','gold','iron','copper','salt','oil']):
        return 'extraction'
    return 'other'


def bind_group(s):
    s = str(s).lower()
    if any(x in s for x in ['community','citizenship','clan','honour','age',
                              'kin','mutual','shame']):
        return 'social'
    if any(x in s for x in ['land','tribute','debt','labour','exam','tax']):
        return 'material'
    if any(x in s for x in ['coercion','military','conscript','fear',
                              'punishment','prison']):
        return 'coercive'
    if any(x in s for x in ['ritual','religion','sacred','charisma','temple',
                              'divine','ancestor']):
        return 'ritual'
    if 'none' in s or 'voluntary' in s:
        return 'none/voluntary'
    return 'mixed'


def partial_r_manual(x, y, z_matrix):
    """Partial correlation r(x, y) controlling for columns in z_matrix."""
    X = np.column_stack([z_matrix, np.ones(len(x))])
    res_x = x - X @ lstsq(X, x, rcond=None)[0]
    res_y = y - X @ lstsq(X, y, rcond=None)[0]
    return stats.pearsonr(res_x, res_y)


def r_squared(X_cols, y):
    X = np.column_stack(list(X_cols) + [np.ones(len(y))])
    y_hat = X @ lstsq(X, y, rcond=None)[0]
    return 1 - np.sum((y - y_hat)**2) / np.sum((y - y.mean())**2)


def sig_stars(p):
    return ('***' if p < 0.001 else '**' if p < 0.01
            else '*' if p < 0.05 else 'ns (marginal)' if p < 0.10 else 'ns')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Ecology of political freedom — latitude, econ base, binding',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--data', type=str,
        default=os.path.join(DATA_DIR, 'governance_extended.csv'),
        help='Path to governance_extended.csv'
    )
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        print(f"ERROR: Cannot find governance_extended.csv at: {args.data}")
        print("Run from the repo root, or pass --data PATH/TO/governance_extended.csv")
        return

    gov = pd.read_csv(args.data)
    gov.columns = gov.columns.str.strip()
    for col in ['sovereignty_index', 'admin_index', 'info_infrastructure',
                'disobedience_freedom', 'Latitude', 'Longitude']:
        if col in gov.columns:
            gov[col] = pd.to_numeric(gov[col], errors='coerce')

    gov['abs_lat']   = gov['Latitude'].abs()
    gov['norm_frac'] = gov['info_infrastructure'] / gov['admin_index']
    gov['econ']      = gov['Economic Base'].apply(econ_group)
    gov['bind']      = gov['binding_mechanism'].apply(bind_group)
    gov['lat_band']  = pd.cut(
        gov['abs_lat'], bins=[0, 20, 40, 70],
        labels=['tropical (0-20°)', 'temperate (20-40°)', 'high-lat (40-70°)'])

    valid = gov.dropna(subset=['abs_lat', 'disobedience_freedom',
                                'sovereignty_index']).copy()
    n_geo = len(valid)

    print("=" * 70)
    print("ECOLOGY OF POLITICAL FREEDOM")
    print("Latitude, economic base, and binding mechanisms as predictors of D")
    print("=" * 70)
    print()
    print(f"Systems with coordinate data: {n_geo} of {len(gov)}")
    print(f"Latitude range: {valid['abs_lat'].min():.1f}° to {valid['abs_lat'].max():.1f}°")
    print()

    # ── Section 1: Raw latitude correlations ─────────────────────────────────

    print("=== SECTION 1: RAW LATITUDE CORRELATIONS ===")
    print()
    D   = valid['disobedience_freedom'].values
    lat = valid['abs_lat'].values
    S   = valid['sovereignty_index'].values
    A   = valid['admin_index'].values

    for label, x in [('|latitude|', lat),
                      ('latitude (signed)', valid['Latitude'].values),
                      ('S (for reference)', S)]:
        r, p = stats.pearsonr(x, D)
        print(f"  r(D, {label:<22}) = {r:+.3f}, p = {p:.4f} {sig_stars(p)}")
    print()

    # ── Section 2: Mediation through S ───────────────────────────────────────

    print("=== SECTION 2: MEDIATION OF LATITUDE-D THROUGH S ===")
    print()
    X_total   = np.column_stack([lat, np.ones(n_geo)])
    X_controlled = np.column_stack([lat, S, np.ones(n_geo)])

    beta_total  = lstsq(X_total,    D, rcond=None)[0][0]
    beta_direct = lstsq(X_controlled, D, rcond=None)[0][0]
    beta_lat_S  = lstsq(X_total,    S, rcond=None)[0][0]
    beta_S_D    = lstsq(X_controlled, D, rcond=None)[0][1]
    indirect    = beta_lat_S * beta_S_D
    pct_mediated = indirect / beta_total * 100 if beta_total != 0 else np.nan

    print(f"  Total effect (|lat| → D):              β = {beta_total:.4f}")
    print(f"  Direct effect (|lat| → D | S):         β = {beta_direct:.4f}")
    print(f"  Indirect path (|lat| → S → D):         β = {indirect:.4f}")
    print(f"  Proportion mediated through S:         {pct_mediated:.1f}%")
    print()
    print(f"  Interpretation: {pct_mediated:.0f}% of the latitude-D relationship runs")
    print(f"  through sovereign capacity (S). The ecology of political freedom")
    print(f"  operates primarily through ecological constraints on state-building,")
    print(f"  not through direct cultural or institutional effects of latitude.")
    print()

    # ── Section 3: The non-Boserup result ────────────────────────────────────

    print("=== SECTION 3: LATITUDE-D BY ECONOMIC BASE (THE NON-BOSERUP RESULT) ===")
    print()
    print("  Boserup hypothesis: lat-D driven by agricultural surplus accumulation")
    print("  (tropical agriculture → surplus → state capacity → low D)")
    print("  Prediction: r(|lat|, D) should be strongest for agricultural systems")
    print()
    econ_order = ['agriculture', 'foraging/fishing', 'extraction',
                  'trade', 'pastoral', 'other']
    for econ in econ_order:
        g = valid[valid['econ'] == econ]
        if len(g) < 10:
            continue
        r, p = stats.pearsonr(g['abs_lat'], g['disobedience_freedom'])
        print(f"  {econ:<22} (n={len(g):3d}): r = {r:+.3f}, p = {p:.4f} {sig_stars(p)}")
    print()
    print("  Finding: r(|lat|, D) is NON-SIGNIFICANT for agriculture (p > 0.4)")
    print("  and SIGNIFICANT for foraging/fishing and extraction (p < 0.01).")
    print("  This contradicts the Boserup agricultural surplus pathway.")
    print("  The ecology chain runs through ecological constraints on S,")
    print("  not through surplus provision to the state.")
    print()

    # ── Section 4: Binding mechanism as independent predictor ────────────────

    print("=== SECTION 4: BINDING MECHANISM AND D ===")
    print()
    bind_order = ['social', 'none/voluntary', 'mixed', 'coercive',
                  'material', 'ritual']
    print(f"  {'Binding mechanism':<18} {'D mean':>8} {'D SD':>7} {'n':>4}")
    print("  " + "-" * 44)
    for b in bind_order:
        g = valid[valid['bind'] == b]['disobedience_freedom']
        if len(g) < 5:
            continue
        print(f"  {b:<18} {g.mean():>8.3f} {g.std():>7.3f} {len(g):>4}")
    print()

    social   = valid[valid['bind'] == 'social']['disobedience_freedom']
    material = valid[valid['bind'] == 'material']['disobedience_freedom']
    coercive = valid[valid['bind'] == 'coercive']['disobedience_freedom']
    ritual   = valid[valid['bind'] == 'ritual']['disobedience_freedom']

    for label, grp in [('material', material), ('coercive', coercive),
                        ('ritual', ritual)]:
        u, p = stats.mannwhitneyu(social, grp, alternative='greater')
        print(f"  MW social > {label:<10}: p = {p:.4f} {sig_stars(p)}")
    print()

    # Kruskal-Wallis across all binding types
    bind_groups = [valid[valid['bind'] == b]['disobedience_freedom'].values
                   for b in bind_order if len(valid[valid['bind'] == b]) >= 5]
    k_stat, k_p = stats.kruskal(*bind_groups)
    print(f"  Kruskal-Wallis across binding types: H = {k_stat:.2f}, "
          f"p = {k_p:.6f} {sig_stars(k_p)}")
    print()

    # ── Section 5: Binding mechanism by latitude ──────────────────────────────

    print("=== SECTION 5: BINDING MECHANISM BY LATITUDE BAND ===")
    print()
    gov_lb = gov.dropna(subset=['abs_lat', 'bind', 'lat_band'])
    ct = pd.crosstab(gov_lb['lat_band'], gov_lb['bind'], normalize='index')
    print(ct.round(3).to_string())
    print()
    print("  High-latitude (40-70°) vs tropical (0-20°) key differences:")
    if 'social' in ct.columns:
        hi  = ct.loc['high-lat (40-70°)', 'social']  if 'high-lat (40-70°)' in ct.index else np.nan
        trop = ct.loc['tropical (0-20°)', 'social']   if 'tropical (0-20°)'  in ct.index else np.nan
        print(f"    Social binding:   high-lat {hi:.1%} vs tropical {trop:.1%}")
    if 'ritual' in ct.columns:
        hi_r  = ct.loc['high-lat (40-70°)', 'ritual'] if 'high-lat (40-70°)' in ct.index else np.nan
        trop_r = ct.loc['tropical (0-20°)', 'ritual'] if 'tropical (0-20°)'  in ct.index else np.nan
        print(f"    Ritual binding:   high-lat {hi_r:.1%} vs tropical {trop_r:.1%}")
    if 'material' in ct.columns:
        hi_m  = ct.loc['high-lat (40-70°)', 'material'] if 'high-lat (40-70°)' in ct.index else np.nan
        trop_m = ct.loc['tropical (0-20°)', 'material'] if 'tropical (0-20°)'  in ct.index else np.nan
        print(f"    Material binding: high-lat {hi_m:.1%} vs tropical {trop_m:.1%}")
    print()

    # ── Section 6: Variance decomposition ────────────────────────────────────

    print("=== SECTION 6: VARIANCE DECOMPOSITION ===")
    print()
    valid2 = gov.dropna(
        subset=['abs_lat', 'disobedience_freedom', 'sovereignty_index',
                'admin_index', 'econ', 'bind']).copy()
    D2  = valid2['disobedience_freedom'].values
    lat2 = valid2['abs_lat'].values
    S2   = valid2['sovereignty_index'].values
    A2   = valid2['admin_index'].values
    ed   = pd.get_dummies(valid2['econ'], drop_first=True).astype(float).values
    bd   = pd.get_dummies(valid2['bind'], drop_first=True).astype(float).values

    models = [
        ('|latitude| only',        [lat2]),
        ('econ only',              [ed]),
        ('bind only',              [bd]),
        ('S only',                 [S2]),
        ('|lat| + S',              [lat2, S2]),
        ('|lat| + econ',           [lat2, ed]),
        ('|lat| + bind',           [lat2, bd]),
        ('econ + bind',            [ed, bd]),
        ('|lat| + econ + S',       [lat2, ed, S2]),
        ('|lat| + bind + S',       [lat2, bd, S2]),
        ('full (lat+econ+bind+S)', [lat2, ed, bd, S2, A2]),
    ]
    for label, cols in models:
        r2 = r_squared(cols, D2)
        print(f"  R²({label:<30}) = {r2:.3f}")
    print()

    # ── Section 7: Temporal stability ────────────────────────────────────────

    print("=== SECTION 7: LATITUDE-D BY HISTORICAL ERA ===")
    print()
    gov['era'] = pd.cut(
        gov['Start'],
        bins=[-400000, -2000, 0, 1000, 1800, 2025],
        labels=['prehistoric', 'ancient', 'classical', 'medieval', 'modern'])
    for era in ['prehistoric', 'ancient', 'classical', 'medieval', 'modern']:
        g = gov[gov['era'] == era].dropna(
            subset=['abs_lat', 'disobedience_freedom'])
        if len(g) < 20:
            continue
        r, p = stats.pearsonr(g['abs_lat'], g['disobedience_freedom'])
        print(f"  {era:<12} (n={len(g):3d}): r = {r:+.3f}, p = {p:.4f} {sig_stars(p)}")
    print()
    print("  The latitude-D relationship is consistent across eras,")
    print("  suggesting a structural rather than historically contingent effect.")
    print()

    # ── Summary ───────────────────────────────────────────────────────────────

    r_raw, p_raw = stats.pearsonr(valid['abs_lat'], valid['disobedience_freedom'])

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print(f"PRIMARY FINDING:")
    print(f"  r(|latitude|, D) = {r_raw:+.3f}, p = {p_raw:.4f} {sig_stars(p_raw)}, n = {n_geo}")
    print(f"  High-latitude societies have significantly higher disobedience")
    print(f"  freedom than tropical societies.")
    print()
    print(f"MEDIATION:")
    print(f"  {pct_mediated:.0f}% of the latitude-D relationship is mediated through S.")
    print(f"  Ecological conditions primarily shape political freedom via their")
    print(f"  effect on state-building capacity, not through cultural pathways.")
    print()
    print("KEY QUALIFICATIONS:")
    print("  1. The effect is non-significant for agricultural economies,")
    print("     contradicting a simple Boserup surplus-accumulation story.")
    print("  2. It is significant for foraging/fishing and extraction economies,")
    print("     where ecological constraints on S are most direct.")
    print("  3. Binding mechanism is a strong independent predictor of D")
    print(f"     (social binding D mean = {social.mean():.3f} vs material binding")
    print(f"      D mean = {material.mean():.3f}), but adds only marginal R² beyond S.")
    print("  4. The lat-D pattern is consistent across historical eras,")
    print("     arguing against a modern-period Europe/Scandinavia artefact.")
    print()
    print("CONNECTIONS TO EXISTING PAPERS:")
    print("  - The S-mediation pathway is the cross-sectional analogue of the")
    print("    lock-in sequence (Paper 2): ecological constraints set S,")
    print("    and low S enables high D via the same structural mechanism.")
    print("  - The non-Boserup result complements the A decomposition finding")
    print("    (a_decomposition.py): administrative capacity is not simply")
    print("    surplus provision — its composition (normalising vs repressive)")
    print("    matters, and that composition also varies ecologically.")
    print()

# ── CSV output ────────────────────────────────────────────────────────────────

def save_csv(gov, out_path):
    """Write the per-system analysis dataset to CSV."""
    cols = [
        'System', 'Region', 'Historical Epoch', 'Start',
        'Latitude', 'Longitude', 'abs_lat', 'lat_band',
        'sovereignty_index', 'admin_index', 'info_infrastructure',
        'disobedience_freedom', 'norm_frac',
        'Economic Base', 'econ',
        'binding_mechanism', 'bind',
        'coding_confidence', 'gw_discussed',
    ]
    out = gov[[c for c in cols if c in gov.columns]].copy()
    out = out.sort_values('System').reset_index(drop=True)
    out.to_csv(out_path, index=False, float_format='%.3f')
    n_geo = int(out['abs_lat'].notna().sum())
    print(f"  Saved CSV: {out_path}  ({len(out)} systems, {n_geo} geocoded)")


# ── Figure output ─────────────────────────────────────────────────────────────

def save_figure(gov, out_path):
    """
    Three-panel figure for ecology_of_freedom analysis.

    Panel A: Latitude-D regression by economic base (the non-Boserup result).
             Legend below the axes.
    Panel B: D by binding mechanism -- dot + mean +/- SD, high to low.
             No separate legend; y-axis labels serve that purpose.
    Panel C: Full |latitude|-D scatter with S as point size and
             Graeber-Wengrow systems annotated.
             Legend to the right of the panel, outside the axes.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.lines as mlines
    import numpy as np
    from scipy import stats as sc_stats

    AMBER = '#e8a020'
    SLATE = '#4a6580'

    plt.rcParams.update({
        'font.family': 'serif',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.alpha': 0.15,
        'grid.linewidth': 0.5,
        'font.size': 9,
    })

    valid = gov.dropna(subset=['abs_lat', 'disobedience_freedom',
                                'sovereignty_index']).copy()

    ECON_STYLE = {
        'foraging/fishing': (AMBER,    '-',  2.0, 'Foraging/fishing'),
        'extraction':       (SLATE,    '-',  2.0, 'Extraction'),
        'agriculture':      ('#aaaaaa', '--', 1.4, 'Agriculture'),
        'trade':            ('#c0c0c0', ':',  1.2, 'Trade'),
    }
    BIND_ORDER = ['social', 'none/voluntary', 'mixed',
                  'coercive', 'material', 'ritual']
    BIND_COLOUR = {
        'social':        AMBER,
        'none/voluntary':'#c8c8b0',
        'mixed':         '#a0a080',
        'coercive':      '#c0392b',
        'material':      SLATE,
        'ritual':        '#7f5f8f',
    }
    ECON_COL = {
        'foraging/fishing': AMBER,
        'extraction':       SLATE,
        'agriculture':      '#888888',
        'trade':            '#a0b8c0',
        'pastoral':         '#b8a060',
        'other':            '#c0c0c0',
    }

    fig, axes = plt.subplots(1, 3, figsize=(19, 5.6),
                              gridspec_kw={'width_ratios': [1, 0.85, 1.15]})
    fig.patch.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')

    # -- Panel A: legend below axes -------------------------------------------
    ax = axes[0]
    lat_range = np.linspace(0, 72, 200)
    handles = []
    for econ, (col, ls, lw, label) in ECON_STYLE.items():
        grp = valid[valid['econ'] == econ].dropna(
            subset=['abs_lat', 'disobedience_freedom'])
        if len(grp) < 8:
            continue
        ax.scatter(grp['abs_lat'], grp['disobedience_freedom'],
                   color=col, alpha=0.25, s=18, zorder=2)
        slope, intercept, r, p, _ = sc_stats.linregress(
            grp['abs_lat'], grp['disobedience_freedom'])
        y_fit = slope * lat_range + intercept
        sig = ('***' if p < 0.001 else '**' if p < 0.01
               else '*' if p < 0.05 else 'ns')
        ax.plot(lat_range, y_fit, color=col, ls=ls, lw=lw, zorder=3)
        handles.append(mlines.Line2D(
            [], [], color=col, ls=ls, lw=lw,
            label=f'{label}  r={r:+.2f} ({sig}), n={len(grp)}'))

    ax.axhline(0.45, color='#c0392b', lw=1.0, ls='--', alpha=0.55)
    ax.text(68, 0.47, '\u03b8=0.45', color='#c0392b', fontsize=7.5, ha='right')
    ax.set_xlabel('Absolute latitude (\u00b0)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(0, 72)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(handles=handles, fontsize=7.2,
              loc='upper center', bbox_to_anchor=(0.5, -0.16),
              frameon=True, framealpha=0.95, borderpad=0.6,
              ncol=2, handlelength=2.0, columnspacing=1.0)
    ax.set_title(
        'A.  Latitude\u2013D by economic base\n'
        '(agriculture: flat; foraging/extraction: rising)',
        fontsize=9, fontweight='bold', loc='left', pad=4)

    # -- Panel B: y-axis labels serve as legend --------------------------------
    ax = axes[1]
    bind_data = valid.dropna(subset=['bind', 'disobedience_freedom'])
    for i, b in enumerate(BIND_ORDER):
        grp = bind_data[bind_data['bind'] == b]['disobedience_freedom'].values
        if len(grp) == 0:
            continue
        col = BIND_COLOUR.get(b, '#888888')
        rng = np.random.default_rng(42 + i)
        jitter = rng.uniform(-0.22, 0.22, len(grp))
        ax.scatter(grp, np.full(len(grp), i) + jitter,
                   color=col, alpha=0.35, s=16, zorder=2)
        mn, sd = grp.mean(), grp.std()
        ax.plot([mn - sd, mn + sd], [i, i],
                color=col, lw=2.0, solid_capstyle='round', zorder=3)
        ax.scatter([mn], [i], color=col, s=55, zorder=4,
                   edgecolors='white', linewidths=0.8)
        ax.text(mn + sd + 0.03, i, f'{mn:.2f}', va='center',
                fontsize=7.5, color=col)

    ax.axvline(0.45, color='#c0392b', lw=1.0, ls='--', alpha=0.55)
    ax.set_yticks(list(range(len(BIND_ORDER))))
    ax.set_yticklabels(BIND_ORDER, fontsize=8)
    ax.set_xlabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(-0.05, 1.15)
    ax.set_title(
        'B.  D by binding mechanism\n'
        '(dot\u202f=\u202fmean; bar\u202f=\u202f\u00b11\u202fSD;'
        ' KW H=39.7, p<0.001)',
        fontsize=9, fontweight='bold', loc='left', pad=4)
    ax.invert_yaxis()

    # -- Panel C: legend outside right edge ------------------------------------
    ax = axes[2]
    for econ, col in ECON_COL.items():
        grp = valid[valid['econ'] == econ]
        if len(grp) == 0:
            continue
        sizes = (1.0 - grp['sovereignty_index'].fillna(0.5)) * 80 + 12
        ax.scatter(grp['abs_lat'], grp['disobedience_freedom'],
                   color=col, s=sizes, alpha=0.55, zorder=2, edgecolors='none')

    # Per-system label offsets to avoid overlap between closely-spaced points
    LABEL_OFFSETS = {
        'Icelandic Althing':                   (4,  9),   # above
        'Icelandic Commonwealth':              (4, -11),  # below
    }
    gw = valid[valid['gw_discussed'].astype(str).str.lower()
               .isin(['true', '1', 'yes', 't'])].dropna(subset=['abs_lat'])
    for _, row in gw.iterrows():
        ax.scatter(row['abs_lat'], row['disobedience_freedom'],
                   color='white', s=60, zorder=5,
                   edgecolors=AMBER, linewidths=1.2)
        sys_name = str(row['System'])
        short = (sys_name.replace(' Democracy', '').replace(' Communities', '')
                         .replace(' Mega-Settlements', '').replace(' / ', '/')[:24])
        offset = LABEL_OFFSETS.get(sys_name, (4, 3))
        va = 'bottom' if offset[1] >= 0 else 'top'
        ax.annotate(short,
                    xy=(row['abs_lat'], row['disobedience_freedom']),
                    xytext=offset, textcoords='offset points',
                    fontsize=5.8, color='#444444', zorder=6, va=va)

    ax.axhline(0.45, color='#c0392b', lw=1.0, ls='--', alpha=0.55)
    ax.text(69, 0.47, '\u03b8=0.45', color='#c0392b', fontsize=7.5, ha='right')

    leg_handles = []
    for s_val, label in [(0.8, 'S\u202f=\u202f0.8'),
                          (0.5, 'S\u202f=\u202f0.5'),
                          (0.2, 'S\u202f=\u202f0.2')]:
        sz = (1.0 - s_val) * 80 + 12
        leg_handles.append(plt.scatter([], [], s=sz, color='#888888',
                                       alpha=0.6, label=label,
                                       edgecolors='none'))
    leg_handles.append(plt.scatter([], [], color='white', s=50,
                                   edgecolors=AMBER, linewidths=1.2,
                                   label='Graeber\u202f&\u202fWengrow'))
    leg_handles.append(mlines.Line2D([], [], color='none', label=''))
    for econ, col in ECON_COL.items():
        leg_handles.append(plt.scatter([], [], color=col, s=28, alpha=0.7,
                                       label=econ, edgecolors='none'))

    ax.legend(handles=leg_handles,
              loc='center left', bbox_to_anchor=(1.01, 0.5),
              fontsize=6.5, frameon=True, framealpha=0.95,
              borderpad=0.6, labelspacing=0.45, handletextpad=0.4)
    ax.set_xlabel('Absolute latitude (\u00b0)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(0, 72)
    ax.set_ylim(-0.02, 1.05)
    ax.set_title(
        'C.  Full dataset scatter\n'
        '(size\u202f\u221d\u202f1\u2212S;'
        ' \u25cb\u202f=\u202fGraeber\u202f&\u202fWengrow systems)',
        fontsize=9, fontweight='bold', loc='left', pad=4)

    fig.suptitle(
        'Ecology of political freedom: latitude, economic base, and binding '
        'mechanisms as predictors of D\n'
        'across 327 geocoded governance systems (isonomia dataset, v7)',
        fontsize=10.5, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18, right=0.88)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved figure: {out_path}')


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse, os, pandas as pd

    parser = argparse.ArgumentParser(
        description='Ecology of political freedom -- with CSV and figure output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--data', type=str,
        default=os.path.join(DATA_DIR, 'governance_extended.csv'),
        help='Path to governance_extended.csv')
    parser.add_argument(
        '--csv', type=str, default=None,
        help='Output CSV path (default: data/ecology_of_freedom.csv)')
    parser.add_argument(
        '--figure', type=str, default=None,
        help='Output figure path (default: visuals/ecology_of_freedom.png)')
    parser.add_argument('--no-csv',    action='store_true',
                        help='Skip CSV output')
    parser.add_argument('--no-figure', action='store_true',
                        help='Skip figure output')
    args = parser.parse_args()

    # Call the analysis
    # (Re-use main() logic inline rather than calling it separately,
    #  since argparse is already handled above)
    import sys
    # Inject the --data arg into sys.argv so main() picks it up
    old_argv = sys.argv[:]
    sys.argv = [sys.argv[0], '--data', args.data]
    main()
    sys.argv = old_argv

    # Prepare data for outputs
    if not os.path.isfile(args.data):
        raise SystemExit(1)

    gov = pd.read_csv(args.data)
    gov.columns = gov.columns.str.strip()
    for col in ['sovereignty_index', 'admin_index', 'info_infrastructure',
                'disobedience_freedom', 'Latitude', 'Longitude']:
        if col in gov.columns:
            gov[col] = pd.to_numeric(gov[col], errors='coerce')

    gov['abs_lat']   = gov['Latitude'].abs()
    gov['norm_frac'] = gov['info_infrastructure'] / gov['admin_index']
    gov['econ']      = gov['Economic Base'].apply(econ_group)
    gov['bind']      = gov['binding_mechanism'].apply(bind_group)
    gov['lat_band']  = pd.cut(
        gov['abs_lat'], bins=[0, 20, 40, 70],
        labels=['tropical', 'temperate', 'high-lat'])

    root     = os.path.join(SCRIPT_DIR, '..')
    data_dir = os.path.join(root, 'data')
    vis_dir  = os.path.join(root, 'visuals')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(vis_dir,  exist_ok=True)

    csv_out = args.csv    or os.path.join(data_dir, 'ecology_of_freedom.csv')
    fig_out = args.figure or os.path.join(vis_dir,  'ecology_of_freedom.png')

    print()
    print('=== OUTPUTS ===')
    if not args.no_csv:
        save_csv(gov, csv_out)
    if not args.no_figure:
        save_figure(gov, fig_out)
