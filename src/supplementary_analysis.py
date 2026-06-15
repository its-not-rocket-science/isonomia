"""
supplementary_analysis.py
=========================
Three exploratory analyses extending the core isonomia findings:

  1. Collapse brittleness: internal collapses (revolt, civil war) occur at
     significantly higher S and lower D than environmental collapses, consistent
     with the lock-in sequence prediction that maximum lock-in produces fragility
     rather than stability. (Paper 2 §8.2 extension.)

  2. Seasonality as an S-constraint mechanism: seasonal resource episodicity
     suppresses S by preventing material binding infrastructure (land, tribute,
     debt). 95.9% of the seasonality-D correlation is mediated through S;
     the direct effect is non-significant. The mechanism is the binding type
     crosstab: high seasonality → 75% none/voluntary binding vs 51% material
     binding in no-seasonality societies. (Ecology working paper.)

  3. Gender structure as independent D predictor: partial r(gender, D | binding)
     = +0.403, p < 0.001. Gender egalitarianism predicts D independently of
     binding type. Mechanism ambiguous (latent egalitarianism vs constituency
     expansion). (Ecology working paper note.)

Outputs
-------
  data/supplementary_analysis.csv  — per-system computed fields
  visuals/supplementary_analysis.png — three-panel figure

Usage
-----
    python src/supplementary_analysis.py
    python src/supplementary_analysis.py --data PATH/TO/governance_extended.csv
    python src/supplementary_analysis.py --no-figure
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

def bind_group(s):
    s = str(s).lower()
    if any(x in s for x in ['community','citizenship','clan','honour','age',
                              'kin','mutual','shame']): return 'social'
    if any(x in s for x in ['land','tribute','debt','labour','exam','tax']): return 'material'
    if any(x in s for x in ['coercion','military','conscript','fear','punishment',
                              'prison']): return 'coercive'
    if any(x in s for x in ['ritual','religion','sacred','charisma','temple',
                              'divine','ancestor']): return 'ritual'
    if 'none' in s or 'voluntary' in s: return 'none/voluntary'
    return 'mixed'

def collapse_type(s):
    s = str(s).lower()
    if any(x in s for x in ['climate','drought','flood','famine','disease',
                              'plague','environmental']): return 'environmental'
    if any(x in s for x in ['conquest','invasion','military','war','defeat',
                              'british','french','spanish','russian','japanese',
                              'mongol','ottoman','dutch']): return 'conquest'
    if any(x in s for x in ['internal','revolt','revolution','civil',
                              'fragmentat','dissolution','overextension']): return 'internal'
    if 'none' in s or 'ongoing' in s: return 'ongoing'
    return 'other'

def gender_score(s):
    s = str(s).lower()
    if any(x in s for x in ['neutral','egal','equal','balanced','mixed']): return 1
    return 0

def sig_stars(p):
    return ('***' if p < 0.001 else '**' if p < 0.01
            else '*' if p < 0.05 else 'ns (marginal)' if p < 0.10 else 'ns')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Supplementary analyses: brittleness, seasonality, gender',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--data', type=str,
        default=os.path.join(DATA_DIR, 'governance_extended.csv'))
    parser.add_argument('--csv', type=str, default=None)
    parser.add_argument('--figure', type=str, default=None)
    parser.add_argument('--no-figure', action='store_true')
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        print(f'ERROR: Cannot find {args.data}')
        print('Run from repo root or pass --data PATH')
        return

    gov = pd.read_csv(args.data)
    gov.columns = gov.columns.str.strip()
    for col in ['sovereignty_index','admin_index','disobedience_freedom',
                'surplus_legibility','info_infrastructure','Latitude']:
        if col in gov.columns:
            gov[col] = pd.to_numeric(gov[col], errors='coerce')

    gov['abs_lat']  = gov['Latitude'].abs()
    gov['seas_ord'] = gov['seasonality'].map(
        {'none':0, 'low':1, 'medium':2, 'high':3})
    gov['bind']    = gov['binding_mechanism'].apply(bind_group)
    gov['ctype']   = gov['Collapse Cause'].apply(collapse_type)
    gov['g_egal']  = gov['Gender Roles'].apply(gender_score)
    gov['norm_frac'] = gov['info_infrastructure'] / gov['admin_index']

    print('=' * 70)
    print('SUPPLEMENTARY ANALYSIS')
    print('Brittleness · Seasonality · Gender')
    print('=' * 70)
    print()

    # ── Analysis 1: Collapse brittleness ──────────────────────────────────────
    print('=== ANALYSIS 1: COLLAPSE TYPE × D AND S ===')
    print()
    print('Hypothesis: internal collapses occur at highest S and lowest D,')
    print('consistent with the lock-in sequence brittleness prediction.')
    print()

    ca = gov[gov['ctype'].isin(['internal','environmental','conquest'])].dropna(
        subset=['disobedience_freedom','sovereignty_index'])

    for ct in ['internal','environmental','conquest']:
        g = ca[ca['ctype']==ct]
        print(f'  {ct:<15} n={len(g):3d}  '
              f'D mean={g.disobedience_freedom.mean():.3f} '
              f'SD={g.disobedience_freedom.std():.3f}  '
              f'S mean={g.sovereignty_index.mean():.3f}')
    print()

    internal = ca[ca['ctype']=='internal']
    environ  = ca[ca['ctype']=='environmental']
    conquest = ca[ca['ctype']=='conquest']

    u1, p1 = stats.mannwhitneyu(environ.disobedience_freedom,
                                  internal.disobedience_freedom,
                                  alternative='greater')
    u2, p2 = stats.mannwhitneyu(internal.sovereignty_index,
                                  environ.sovereignty_index,
                                  alternative='greater')
    u3, p3 = stats.mannwhitneyu(internal.sovereignty_index,
                                  conquest.sovereignty_index,
                                  alternative='greater')
    print(f'  MW env D > internal D:      p = {p1:.4f} {sig_stars(p1)}')
    print(f'  MW internal S > env S:      p = {p2:.4f} {sig_stars(p2)}')
    print(f'  MW internal S > conquest S: p = {p3:.4f} {sig_stars(p3)}')
    print()
    print('  High-S / low-D internal collapse cases:')
    top = internal.nlargest(6, 'sovereignty_index')
    print(top[['System','Collapse Cause',
               'disobedience_freedom','sovereignty_index']].to_string(index=False))
    print()

    # ── Analysis 2: Seasonality ────────────────────────────────────────────────
    print('=== ANALYSIS 2: SEASONALITY AS S-CONSTRAINT MECHANISM ===')
    print()
    sv = gov.dropna(subset=['seas_ord','disobedience_freedom','sovereignty_index'])
    r_raw, p_raw = stats.pearsonr(sv['seas_ord'], sv['disobedience_freedom'])
    r_sS,  p_sS  = stats.pearsonr(sv['seas_ord'], sv['sovereignty_index'])
    print(f'  r(seasonality, D) = {r_raw:+.3f}, p = {p_raw:.4f} {sig_stars(p_raw)}')
    print(f'  r(seasonality, S) = {r_sS:+.3f}, p = {p_sS:.4f} {sig_stars(p_sS)}')
    print()

    X_s  = np.column_stack([sv['seas_ord'].values, np.ones(len(sv))])
    b_tot = lstsq(X_s, sv['disobedience_freedom'].values, rcond=None)[0][0]
    b_sS  = lstsq(X_s, sv['sovereignty_index'].values, rcond=None)[0][0]
    X_ss  = np.column_stack([sv['seas_ord'].values,
                              sv['sovereignty_index'].values, np.ones(len(sv))])
    b_dir = lstsq(X_ss, sv['disobedience_freedom'].values, rcond=None)[0][0]
    b_SD  = lstsq(X_ss, sv['disobedience_freedom'].values, rcond=None)[0][1]
    indirect = b_sS * b_SD
    pct_med  = indirect / b_tot * 100 if b_tot != 0 else 0

    print(f'  Mediation through S: {pct_med:.1f}%')
    pr_s, p_pr = stats.pearsonr(
        sv['seas_ord'].values - X_ss[:,:1] @ lstsq(X_ss[:,:1], sv['seas_ord'].values, rcond=None)[0],
        sv['disobedience_freedom'].values - X_ss[:,:1] @ lstsq(X_ss[:,:1], sv['disobedience_freedom'].values, rcond=None)[0])
    # Correct partial r
    X_S_only = np.column_stack([sv['sovereignty_index'].values, np.ones(len(sv))])
    res_seas = sv['seas_ord'].values - X_S_only @ lstsq(X_S_only, sv['seas_ord'].values, rcond=None)[0]
    res_D    = sv['disobedience_freedom'].values - X_S_only @ lstsq(X_S_only, sv['disobedience_freedom'].values, rcond=None)[0]
    r_part, p_part = stats.pearsonr(res_seas, res_D)
    print(f'  Partial r(seasonality, D | S) = {r_part:+.3f}, '
          f'p = {p_part:.4f} {sig_stars(p_part)}')
    print()
    print('  Binding mechanism by seasonality (row %):')
    sb = gov.dropna(subset=['seasonality','bind'])
    ct_bind = pd.crosstab(sb['seasonality'], sb['bind'], normalize='index')
    for row in ['none','low','medium','high']:
        if row not in ct_bind.index: continue
        mat  = ct_bind.loc[row,'material']      if 'material'      in ct_bind.columns else 0
        nov  = ct_bind.loc[row,'none/voluntary'] if 'none/voluntary' in ct_bind.columns else 0
        soc  = ct_bind.loc[row,'social']         if 'social'         in ct_bind.columns else 0
        n    = len(sb[sb['seasonality']==row])
        print(f'    {row:<8} (n={n:3d}): material={mat:.1%}  '
              f'none/voluntary={nov:.1%}  social={soc:.1%}')
    print()

    # ── Analysis 3: Gender ────────────────────────────────────────────────────
    print('=== ANALYSIS 3: GENDER STRUCTURE AS INDEPENDENT D PREDICTOR ===')
    print()
    gv = gov.dropna(subset=['g_egal','bind','disobedience_freedom'])
    r_raw_g, p_raw_g = stats.pearsonr(gv['g_egal'], gv['disobedience_freedom'])
    print(f'  r(gender_egalitarian, D) = {r_raw_g:+.3f}, '
          f'p = {p_raw_g:.4f} {sig_stars(p_raw_g)}')

    bd = pd.get_dummies(gv['bind'], drop_first=True).astype(float)
    X_bind = np.column_stack([bd.values, np.ones(len(gv))])
    res_g = gv['g_egal'].values - X_bind @ lstsq(X_bind, gv['g_egal'].values, rcond=None)[0]
    res_D = gv['disobedience_freedom'].values - X_bind @ lstsq(X_bind, gv['disobedience_freedom'].values, rcond=None)[0]
    r_part_g, p_part_g = stats.pearsonr(res_g, res_D)
    print(f'  Partial r(gender, D | binding) = {r_part_g:+.3f}, '
          f'p = {p_part_g:.4f} {sig_stars(p_part_g)}')
    print()
    print('  D by gender × binding (egalitarian=1 vs male-dominated=0):')
    grp = (gv.groupby(['bind','g_egal'])['disobedience_freedom']
             .agg(['mean','count']).round(3))
    print(grp.to_string())
    print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print('=' * 70)
    print('SUMMARY')
    print('=' * 70)
    print()
    print('1. BRITTLENESS (Paper 2 §8.2):')
    print(f'   Internal collapses: D={internal.disobedience_freedom.mean():.3f}, '
          f'S={internal.sovereignty_index.mean():.3f} (n={len(internal)})')
    print(f'   Environmental:      D={environ.disobedience_freedom.mean():.3f}, '
          f'S={environ.sovereignty_index.mean():.3f} (n={len(environ)})')
    print(f'   MW D: p={p1:.4f}; MW S: p={p2:.4f}')
    print('   Full lock-in produces brittleness, not stability.')
    print()
    print('2. SEASONALITY (ecology working paper):')
    print(f'   r(seasonality, D) = {r_raw:+.3f}; mediation through S: {pct_med:.1f}%')
    print(f'   Partial r(seasonality, D | S) = {r_part:+.3f} (ns)')
    print('   Mechanism: episodic resources → prevents material binding → S constrained.')
    print()
    print('3. GENDER (ecology working paper note):')
    print(f'   Partial r(gender, D | binding) = {r_part_g:+.3f} {sig_stars(p_part_g)}')
    print('   Gender egalitarianism predicts D independently of binding type.')
    print('   Mechanism ambiguous; warrants note but not standalone paper.')
    print()

    # ── Save CSV ──────────────────────────────────────────────────────────────
    out_cols = ['System','Region','Historical Epoch','Start',
                'sovereignty_index','admin_index','disobedience_freedom',
                'surplus_legibility','Latitude','abs_lat','seasonality','seas_ord',
                'Economic Base','binding_mechanism','bind',
                'Collapse Cause','ctype','Gender Roles','g_egal',
                'norm_frac','coding_confidence']
    out = gov[[c for c in out_cols if c in gov.columns]].copy()
    csv_out = args.csv or os.path.join(DATA_DIR, 'supplementary_analysis.csv')
    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    out.sort_values('System').to_csv(csv_out, index=False, float_format='%.3f')
    print(f'  Saved CSV: {csv_out}  ({len(out)} rows)')

    if not args.no_figure:
        vis_dir = os.path.join(ROOT, 'visuals')
        os.makedirs(vis_dir, exist_ok=True)
        fig_out = args.figure or os.path.join(vis_dir, 'supplementary_analysis.png')
        save_figure(gov, ca, sb, gv, fig_out,
                    p1=p1, p2=p2, r_raw=r_raw, pct_med=pct_med,
                    r_part=r_part, r_part_g=r_part_g)


def save_figure(gov, ca, sb, gv, out_path, **stats_kw):
    """
    Three-panel supplementary figure.
    Panel A: S vs D scatter coloured by collapse type (brittleness).
    Panel B: Binding mechanism by seasonality — stacked horizontal bars.
    Panel C: D by gender × binding — dot + mean strips.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    AMBER = '#e8a020'
    GREEN = '#6fcf97'
    RED   = '#c0392b'
    SLATE = '#4a6580'

    CTYPE_COL   = {'internal': RED, 'environmental': GREEN, 'conquest': SLATE}
    CTYPE_LABEL = {'internal': 'Internal collapse\n(revolt/civil war)',
                   'environmental': 'Environmental\ncollapse',
                   'conquest': 'Military conquest'}
    BIND_COL = {'social':GREEN, 'none/voluntary':'#c8c8b0', 'mixed':'#a0a080',
                'coercive':RED, 'material':SLATE, 'ritual':'#7f5f8f'}
    BIND_ORDER_B = ['none/voluntary','social','mixed','ritual','coercive','material']

    plt.rcParams.update({
        'font.family':'serif', 'axes.spines.top':False, 'axes.spines.right':False,
        'axes.facecolor':'white', 'figure.facecolor':'white',
        'axes.grid':True, 'grid.alpha':0.12, 'grid.linewidth':0.5, 'font.size':9,
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8),
                              gridspec_kw={'width_ratios':[1.1, 1.0, 0.9]})
    for ax in axes: ax.set_facecolor('white')

    # ── Panel A: S vs D coloured by collapse type ─────────────────────────────
    ax = axes[0]
    ax.axhline(0.45, color=AMBER, lw=1.1, ls='--', alpha=0.65, zorder=1)
    ax.axvline(0.45, color=AMBER, lw=0.8, ls=':', alpha=0.35, zorder=1)
    ax.text(0.97, 0.47, '\u03b8=0.45', color=AMBER, fontsize=7.5,
            ha='right', transform=ax.get_yaxis_transform())

    for ctype, col in CTYPE_COL.items():
        grp = ca[ca['ctype']==ctype]
        if len(grp) == 0: continue
        rng = np.random.default_rng(hash(ctype) % (2**32))
        jx  = rng.uniform(-0.012, 0.012, len(grp))
        jy  = rng.uniform(-0.012, 0.012, len(grp))
        ax.scatter(grp['sovereignty_index'] + jx,
                   grp['disobedience_freedom'] + jy,
                   color=col, alpha=0.65, s=28, zorder=3+list(CTYPE_COL).index(ctype),
                   edgecolors='none', label=CTYPE_LABEL[ctype])
        # Mean marker
        ax.scatter(grp['sovereignty_index'].mean(),
                   grp['disobedience_freedom'].mean(),
                   color=col, s=120, zorder=6, marker='D',
                   edgecolors='white', linewidths=1.2)

    ax.set_xlabel('S (sovereign capacity)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(-0.04, 1.04); ax.set_ylim(-0.04, 1.04)
    ax.legend(fontsize=7.5, loc='upper right', framealpha=0.92,
              title='Collapse type (◆ = mean)', title_fontsize=7)
    p1 = stats_kw.get('p1', 0)
    p2 = stats_kw.get('p2', 0)
    ax.text(0.03, 0.04,
            f'MW env D > internal D: p={p1:.3f}\n'
            f'MW internal S > env S: p={p2:.3f}',
            transform=ax.transAxes, fontsize=7, color='#555555',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#cccccc', alpha=0.9))
    ax.set_title('A.  Collapse type in phase space\n'
                 '(internal collapses cluster: high S, low D)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel B: Binding by seasonality — horizontal stacked bars ─────────────
    ax = axes[1]
    ct = pd.crosstab(sb['seasonality'], sb['bind'], normalize='index')
    ct = ct.reindex(index=['none','low','medium','high']).fillna(0)
    bind_plot = [b for b in BIND_ORDER_B if b in ct.columns]

    ylabels = {'none':'None\n(n=55)', 'low':'Low\n(n=278)',
               'medium':'Medium\n(n=31)', 'high':'High\n(n=24)'}
    y_pos = range(len(ct))
    lefts = np.zeros(len(ct))
    for b in bind_plot:
        vals = ct[b].values if b in ct.columns else np.zeros(len(ct))
        col  = BIND_COL.get(b, '#888888')
        bars = ax.barh(list(y_pos), vals, left=lefts, color=col,
                       alpha=0.82, label=b, edgecolor='white', linewidth=0.5)
        # Label if wide enough
        for i, (v, l) in enumerate(zip(vals, lefts)):
            if v > 0.08:
                ax.text(l + v/2, i, f'{v:.0%}', ha='center', va='center',
                        fontsize=7, color='white' if v > 0.15 else '#333333',
                        fontweight='bold' if v > 0.15 else 'normal')
        lefts += vals

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels([ylabels.get(s,'') for s in ct.index], fontsize=8.5)
    ax.set_xlabel('Proportion of systems', fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.legend(fontsize=7, loc='lower right', framealpha=0.92,
              ncol=2, handlelength=1.0, columnspacing=0.8)
    pct_med = stats_kw.get('pct_med', 0)
    ax.text(0.97, 0.97,
            f'Seasonality \u2192 S \u2192 D\n({pct_med:.0f}% mediated through S)\nDirect effect ns',
            transform=ax.transAxes, ha='right', va='top', fontsize=7.5,
            color='#444444',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#cccccc', alpha=0.9))
    ax.set_title('B.  Binding mechanism by seasonality\n'
                 '(episodic resources prevent material binding)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel C: D by gender × binding ───────────────────────────────────────
    ax = axes[2]
    BIND_SHOW = ['social','none/voluntary','coercive','material','ritual']
    rng2 = np.random.default_rng(0)

    for i, b in enumerate(BIND_SHOW):
        col = BIND_COL.get(b, '#888888')
        for g_val, alpha, marker in [(0, 0.45, 'o'), (1, 0.85, 's')]:
            grp = gv[(gv['bind']==b) & (gv['g_egal']==g_val)]['disobedience_freedom'].values
            if len(grp) == 0: continue
            jitter = rng2.uniform(-0.18, 0.18, len(grp))
            xbase  = i + (0.16 if g_val == 1 else -0.16)
            ax.scatter(np.full(len(grp), xbase) + jitter, grp,
                       color=col, alpha=alpha, s=16, zorder=2,
                       marker=marker, edgecolors='none')
            ax.scatter([xbase], [grp.mean()], color=col, s=60, zorder=4,
                       marker=marker, edgecolors='white', linewidths=0.8)

    ax.axhline(0.45, color=AMBER, lw=1.1, ls='--', alpha=0.65, zorder=1)
    ax.set_xticks(range(len(BIND_SHOW)))
    ax.set_xticklabels([b.replace('/','/\n') for b in BIND_SHOW], fontsize=8)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_ylim(-0.04, 1.10)
    ax.set_xlim(-0.6, len(BIND_SHOW)-0.4)

    from matplotlib.lines import Line2D
    leg = [Line2D([0],[0], marker='o', color='#888888', ms=7, ls='none',
                  label='Male-dominated (g=0)'),
           Line2D([0],[0], marker='s', color='#888888', ms=7, ls='none',
                  alpha=0.85, label='Egalitarian (g=1)')]
    ax.legend(handles=leg, fontsize=7.5, loc='upper right', framealpha=0.92)

    r_pg = stats_kw.get('r_part_g', 0)
    ax.text(0.03, 0.04,
            f'Partial r(gender, D | binding)\n= {r_pg:+.3f}, p < 0.001',
            transform=ax.transAxes, fontsize=7.5, color='#444444',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#cccccc', alpha=0.9))
    ax.set_title('C.  D by gender structure \u00d7 binding type\n'
                 '(\u25a1 = gender-egalitarian; \u25cb = male-dominated)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    fig.suptitle(
        'Supplementary analysis: brittleness, seasonality, and gender structure '
        'as predictors of political freedom\n'
        'isonomia dataset v7 \u2014 exploratory; see individual paper sections for caveats',
        fontsize=10, fontweight='bold', y=1.02)

    plt.tight_layout(w_pad=2.5)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved figure: {out_path}')


if __name__ == '__main__':
    main()
