"""
crossvalidate_edr.py
Cross-validates the isonomia EDR composite and SAP variables against:
  1. V-Dem v16 (liberal democracy, electoral, egalitarian, deliberative indices
               + disaggregated freedom-of-movement, judicial constraints,
               civil society participation indicators)
  2. Polity5   (DEMOC, AUTOC, XCONST, PARCOMP, XRCOMP)

Usage:
    python src/crossvalidate_edr.py \\
        --vdem  path/to/V-Dem-CY-Full+Others-v16.csv \\
        --polity path/to/p5v2018.csv

Outputs:
    visuals/crossval_vdem.png        scatter matrix EDR vs V-Dem indices
    visuals/crossval_polity.png      scatter matrix EDR/SAP vs Polity components
    visuals/crossval_disagg.png      EDR components vs V-Dem disaggregated vars
    data/crossval_matched.csv        the matched comparison dataset
    results printed to stdout

The script also runs without external files to validate the variable mapping
logic and show the expected isonomia systems that should match each dataset.

Downloads (free):
  V-Dem v16 CSV:  https://www.v-dem.net/data/the-v-dem-dataset/
                  → Country-Year: V-Dem Full+Others version 16
  Polity5 CSV:    https://www.systemicpeace.org/inscrdata.html
                  → Polity5 Annual Time-Series 1946-2018 (Excel → save as CSV)
"""

import os, sys, csv, argparse, warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
warnings.filterwarnings('ignore')

DATA_PATH    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data',
                            'governance_extended.csv')
OUTPUT_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visuals')
MATCHED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data',
                            'crossval_matched.csv')

plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

# ── Variable mappings ─────────────────────────────────────────────────────────

# V-Dem variable names (v16 column names) → isonomia concept
VDEM_MAP = {
    # High-level indices (0–1 scale after normalisation)
    'v2x_libdem':    ('EDR_proxy',   'Liberal democracy index'),
    'v2x_egaldem':   ('EDR_proxy2',  'Egalitarian democracy index'),
    'v2x_polyarchy': ('P_proxy',     'Electoral democracy (polyarchy)'),
    'v2x_delibdem':  ('D_proxy',     'Deliberative democracy index'),
    'v2x_partipdem': ('R_proxy',     'Participatory democracy index'),

    # Disaggregated indicators most aligned to E, D, R
    'v2clfmove':     ('E_proxy',     'Freedom of movement (E)'),
    'v2clrspct':     ('E_proxy2',    'Rigorous and impartial administration (E)'),
    'v2jucomp':      ('D_proxy2',    'Compliance with judiciary (D)'),
    'v2jucorrdc':    ('D_proxy3',    'Judicial corruption decisions (D, inverted)'),
    'v2cseeorgs':    ('R_proxy2',    'Freedom of civil society organisations (R)'),
    'v2csreprss':    ('R_proxy3',    'Civil society repression (R, inverted)'),
    'v2exrescon':    ('S_proxy',     'Executive respects constitution (inv. S)'),
    'v2lgbicam':     ('A_proxy',     'Legislative bicameralism (A)'),
}

# Polity5 variable names → isonomia concept
POLITY_MAP = {
    'democ':   ('EDR_proxy',  'Institutionalised democracy (0–10)'),
    'autoc':   ('SAP_proxy',  'Institutionalised autocracy (0–10)'),
    'xconst':  ('D_proxy',    'Executive constraints (1–7)'),
    'parcomp': ('P_proxy',    'Competitiveness of political participation (1–5)'),
    'xrcomp':  ('succ_proxy', 'Competitiveness of executive recruitment (1–3)'),
    'xropen':  ('E_proxy',    'Openness of executive recruitment (1–4)'),
}

# ── Isonomia systems with modern-state equivalents ────────────────────────────
# Format: isonomia system name → (country_name_in_vdem, iso3, year_to_use)
# Year: use the midpoint of the system's active period, capped at V-Dem coverage
ISONOMIA_TO_MODERN = {
    'Norwegian Sovereign Wealth Democracy':  ('Norway',               'NOR', 2015),
    'Estonian Digital Democracy':            ('Estonia',              'EST', 2015),
    'Swedish Social Democracy':              ('Sweden',               'SWE', 2000),
    'Swiss Consensus Democracy':             ('Switzerland',          'CHE', 2000),
    'European Union Governance':             ('Germany',              'DEU', 2010),
    'British Parliamentary System':          ('United Kingdom',       'GBR', 1990),
    'Dutch Republic States-General':         ('Netherlands',          'NLD', 1800),
    'French Fifth Republic':                 ('France',               'FRA', 1990),
    'American Federal Republic':             ('United States',        'USA', 1990),
    'Soviet Republics System':               ('Russia',               'RUS', 1980),
    'Singaporean Technocracy':               ('Singapore',            'SGP', 2000),
    'Meiji Oligarchy':                       ('Japan',                'JPN', 1900),
    'Japanese Liberal Democracy':            ('Japan',                'JPN', 1990),
    'Napoleonic Meritocracy':                ('France',               'FRA', 1810),
    'Ottoman Empire':                        ('Turkey',               'TUR', 1900),
    'Habsburg Composite Monarchy':           ('Austria',              'AUT', 1900),
    'Qin Legalism':                          ('China',                'CHN', 1949),
    'Confucian Bureaucracy':                 ('China',                'CHN', 1850),
    'Indian Panchayati Raj':                 ('India',                'IND', 1995),
    'Apartheid Bantustans':                  ('South Africa',         'ZAF', 1975),
    'Post-Apartheid South Africa':           ('South Africa',         'ZAF', 2000),
    'Tanzanian Ujamaa Villages':             ('Tanzania',             'TZA', 1975),
    'Mexican PRI Corporatism':               ('Mexico',               'MEX', 1975),
    'Brazilian Military Junta':              ('Brazil',               'BRA', 1970),
    'Weimar Republic':                       ('Germany',              'DEU', 1928),
    'Nazi Germany':                          ('Germany',              'DEU', 1938),
    'Roman Republic':                        ('Italy',                'ITA', 1870),
    'Althingi Carbon-Neutral Parliament':    ('Iceland',              'ISL', 2015),
    'Joseon Confucian Bureaucracy':          ('South Korea',          'KOR', 1870),
    'Cossack Hetmanate':                     ('Ukraine',              'UKR', 2010),
}


# ── Load isonomia data ────────────────────────────────────────────────────────

def load_isonomia():
    systems = {}
    with open(DATA_PATH, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                if int(r.get('coding_confidence', 1) or 1) < 2:
                    continue
                E = float(r['exit_freedom'])
                D = float(r['disobedience_freedom'])
                R = float(r['arrangement_freedom'])
                S = float(r['sovereignty_index'])
                A = float(r['admin_index'])
                P = float(r['competitive_politics_index'])
                L = float(r['surplus_legibility'])
                I = float(r['info_infrastructure'])
                systems[r['System']] = {
                    'E': E, 'D': D, 'R': R,
                    'S': S, 'A': A, 'P': P,
                    'L': L, 'I': I,
                    'EDR': (E + D + R) / 3,
                    'SAP': (S + A + P) / 3,
                    'start': r.get('Start', ''),
                    'end':   r.get('End', ''),
                    'conf':  int(r.get('coding_confidence', 2) or 2),
                }
            except (ValueError, TypeError):
                continue
    return systems


# ── Load and match V-Dem ──────────────────────────────────────────────────────

def load_vdem(vdem_path):
    """Load V-Dem CSV and return dict keyed by (country_name, year)."""
    print(f"Loading V-Dem from {vdem_path}...")
    vdem = {}
    vdem_vars = list(VDEM_MAP.keys()) + ['country_name', 'country_text_id', 'year']
    with open(vdem_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        available = set(reader.fieldnames or [])
        use_vars  = [v for v in list(VDEM_MAP.keys()) if v in available]
        missing   = [v for v in VDEM_MAP if v not in available]
        if missing:
            print(f"  V-Dem vars not in this version: {missing}")
        for row in reader:
            try:
                key = (row['country_text_id'], int(row['year']))
                vdem[key] = {v: float(row[v]) if row.get(v, '') not in ('', 'NA', 'nan')
                             else None
                             for v in use_vars}
                vdem[key]['country_name'] = row.get('country_name', '')
            except (ValueError, KeyError):
                continue
    print(f"  Loaded {len(vdem):,} V-Dem country-year observations")
    return vdem


def match_vdem(iso_systems, vdem):
    """Match isonomia systems to V-Dem entries."""
    matched = []
    for sys_name, (country, iso3, year) in ISONOMIA_TO_MODERN.items():
        if sys_name not in iso_systems:
            continue
        key = (iso3, year)
        if key not in vdem:
            # Try adjacent years
            for dy in range(1, 6):
                if (iso3, year + dy) in vdem:
                    key = (iso3, year + dy)
                    break
                if (iso3, year - dy) in vdem:
                    key = (iso3, year - dy)
                    break
            else:
                print(f"  No V-Dem match: {sys_name} ({iso3}, {year})")
                continue
        iso = iso_systems[sys_name]
        vd  = vdem[key]
        row = {'system': sys_name, 'country': country, 'iso3': iso3,
               'year': key[1]}
        # isonomia variables
        for k in ['E', 'D', 'R', 'S', 'A', 'P', 'L', 'I', 'EDR', 'SAP']:
            row[f'iso_{k}'] = iso[k]
        # V-Dem variables (normalise to 0-1 where needed)
        for vdem_var, (concept, label) in VDEM_MAP.items():
            val = vd.get(vdem_var)
            if val is not None:
                # v2x_* high-level indices are already on 0-1 scale — no normalisation
                # v2c*, v2j*, v2cs* disaggregated indicators are on interval
                # scale approx [-4, +4] → normalise to 0-1
                if vdem_var.startswith('v2x'):
                    pass  # already 0-1
                elif vdem_var.startswith('v2'):
                    val = (val + 4) / 8  # interval → approximate 0-1
                row[f'vdem_{vdem_var}'] = val
        matched.append(row)
    print(f"  Matched {len(matched)} isonomia ↔ V-Dem pairs")
    return matched


# ── Load and match Polity5 ────────────────────────────────────────────────────

def load_polity(polity_path):
    """Load Polity5 — accepts .xls, .xlsx, or .csv."""
    import pathlib
    print(f"Loading Polity5 from {polity_path}...")
    polity = {}
    suffix = pathlib.Path(polity_path).suffix.lower()

    # XLS/XLSX: read with pandas, which handles binary format and encoding
    if suffix in ('.xls', '.xlsx'):
        try:
            import pandas as pd
            engine = 'xlrd' if suffix == '.xls' else 'openpyxl'
            df = pd.read_excel(polity_path, engine=engine)
            rows_iter = df.to_dict('records')
        except ImportError:
            raise ImportError("pandas and xlrd are required for .xls files: "
                              "pip install pandas xlrd")
    else:
        # CSV — try utf-8 then latin-1
        import io, pandas as _pd
        try:
            df = _pd.read_csv(polity_path)
            rows_iter = df.to_dict('records')
        except Exception:
            for enc in ('utf-8', 'latin-1', 'cp1252'):
                try:
                    with open(polity_path, encoding=enc) as f:
                        content = f.read()
                    rows_iter = list(csv.DictReader(io.StringIO(content)))
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"Cannot decode {polity_path}")

    # Common spell-expansion logic for both XLS and CSV paths
    for row in rows_iter:
        try:
            row = {str(k): str(v) if v is not None else '' for k, v in row.items()}
            byear = int(float(row.get('byear', row.get('year', 0))))
            eyear_raw = float(row.get('eyear', row.get('year', byear)))
            eyear = min(int(eyear_raw), 2018) if eyear_raw < 9000 else 2018
            iso = row.get('scode', row.get('country', '')).strip().upper()
            if not iso: continue
            vals = {}
            for var in POLITY_MAP:
                v = row.get(var, '')
                try:
                    fv = float(v)
                    vals[var] = fv if fv > -60 else None
                except (ValueError, TypeError):
                    vals[var] = None
            for yr in range(byear, eyear + 1):
                polity[(iso, yr)] = vals
        except (ValueError, KeyError, TypeError):
            continue

    print(f"  Loaded {len(polity):,} Polity country-year observations")
    return polity


# ── Run correlations and generate figures ─────────────────────────────────────

def sig(p):
    return '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'


def scatter_panel(ax, x, y, xlabel, ylabel, colour='#2166ac'):
    """Scatter with regression line and r annotation."""
    valid = [(xi, yi) for xi, yi in zip(x, y) if xi is not None and yi is not None
             and not (np.isnan(xi) or np.isnan(yi))]
    if len(valid) < 5:
        ax.text(0.5, 0.5, 'insufficient data', transform=ax.transAxes,
                ha='center', color='grey')
        return
    xv, yv = zip(*valid)
    xv, yv = np.array(xv), np.array(yv)
    ax.scatter(xv, yv, c=colour, s=45, alpha=0.8, edgecolors='white', linewidths=0.5)
    m, b = np.polyfit(xv, yv, 1)
    xr = np.linspace(xv.min(), xv.max(), 100)
    ax.plot(xr, m * xr + b, 'k--', lw=1.2, alpha=0.5)
    r, p = stats.pearsonr(xv, yv)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(f'r = {r:.3f} {sig(p)}  (n={len(xv)})', fontsize=9)


def run_vdem_validation(matched):
    """Produce V-Dem cross-validation figures and print summary statistics."""
    print("\n=== V-DEM CROSS-VALIDATION ===\n")

    # Panel 1: EDR vs high-level V-Dem indices
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    pairs = [
        ('iso_EDR', 'vdem_v2x_libdem',    'EDR composite', 'V-Dem liberal democracy'),
        ('iso_EDR', 'vdem_v2x_egaldem',   'EDR composite', 'V-Dem egalitarian democracy'),
        ('iso_EDR', 'vdem_v2x_delibdem',  'EDR composite', 'V-Dem deliberative democracy'),
        ('iso_D',   'vdem_v2jucomp',      'D (disobedience)', 'V-Dem judicial compliance'),
        ('iso_E',   'vdem_v2clfmove',     'E (exit freedom)', 'V-Dem freedom of movement'),
        ('iso_R',   'vdem_v2cseeorgs',    'R (arrangement)', 'V-Dem civil society orgs'),
    ]
    colours = ['#1b9e77', '#1b9e77', '#1b9e77', '#2166ac', '#d62728', '#7570b3']
    for ax, (xk, yk, xl, yl), col in zip(axes.flat, pairs, colours):
        x = [r.get(xk) for r in matched]
        y = [r.get(yk) for r in matched]
        scatter_panel(ax, x, y, xl, yl, col)

    fig.suptitle('EDR composite and components vs V-Dem indices\n'
                 'Cross-validation: isonomia hand-coded dataset vs V-Dem v16',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'crossval_vdem.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: crossval_vdem.png")

    # Print summary table
    print(f"{'Isonomia var':20s}  {'V-Dem var':25s}  r       p      n")
    print("-" * 75)
    for xk, yk, xl, yl in pairs:
        x = [r.get(xk) for r in matched]
        y = [r.get(yk) for r in matched]
        valid = [(xi, yi) for xi, yi in zip(x, y)
                 if xi is not None and yi is not None
                 and not (np.isnan(float(xi)) or np.isnan(float(yi)))]
        if len(valid) >= 5:
            xv, yv = zip(*valid)
            r_val, p_val = stats.pearsonr(xv, yv)
            print(f"  {xl:20s}  {yl:25s}  {r_val:.3f}   {p_val:.4f} {sig(p_val)}  n={len(valid)}")


def run_polity_validation(iso_systems, polity):
    """Match isonomia modern systems to Polity5 and run correlations."""
    print("\n=== POLITY5 CROSS-VALIDATION ===\n")

    # Polity uses different country codes — build a mapping
    POLITY_ISO = {
        'NOR': 'NOR', 'EST': 'EST', 'SWE': 'SWE', 'CHE': 'CHE',
        'GBR': 'UKG', 'USA': 'USA', 'RUS': 'RUS', 'JPN': 'JPN',
        'FRA': 'FRN', 'DEU': 'GMY', 'TUR': 'TUR', 'IND': 'IND',
        'ZAF': 'SAF', 'MEX': 'MEX', 'BRA': 'BRA', 'ISL': 'ICE',
        'NLD': 'NTH', 'AUT': 'AUS', 'CHN': 'CHN', 'KOR': 'ROK',
        'UKR': 'UKR', 'SGP': 'SIN', 'TZA': 'TAZ', 'ITA': 'ITA',
    }

    matched_pol = []
    for sys_name, (country, iso3, year) in ISONOMIA_TO_MODERN.items():
        if sys_name not in iso_systems:
            continue
        pol_code = POLITY_ISO.get(iso3, iso3)
        key = (pol_code, year)
        if key not in polity:
            for dy in range(1, 6):
                if (pol_code, year + dy) in polity:
                    key = (pol_code, year + dy); break
                if (pol_code, year - dy) in polity:
                    key = (pol_code, year - dy); break
            else:
                continue
        iso = iso_systems[sys_name]
        pol = polity[key]
        row = {'system': sys_name}
        for k in ['E', 'D', 'R', 'S', 'A', 'P', 'EDR', 'SAP']:
            row[f'iso_{k}'] = iso[k]
        for var in POLITY_MAP:
            row[f'pol_{var}'] = pol.get(var)
        matched_pol.append(row)

    print(f"  Matched {len(matched_pol)} isonomia ↔ Polity5 pairs")

    if len(matched_pol) < 5:
        print("  Insufficient matches for Polity cross-validation")
        return matched_pol

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    pairs = [
        ('iso_EDR', 'pol_democ',   'EDR composite', 'Polity DEMOC (0-10)'),
        ('iso_SAP', 'pol_autoc',   'SAP composite', 'Polity AUTOC (0-10)'),
        ('iso_D',   'pol_xconst',  'D (disobedience)', 'Polity XCONST (exec. constraints)'),
        ('iso_P',   'pol_parcomp', 'P (competitive politics)', 'Polity PARCOMP'),
        ('iso_S',   'pol_autoc',   'S (sovereignty)', 'Polity AUTOC'),
        ('iso_EDR', 'pol_xconst',  'EDR composite', 'Polity XCONST'),
    ]
    colours = ['#1b9e77','#d62728','#2166ac','#7570b3','#d95f02','#1b9e77']
    for ax, (xk, yk, xl, yl), col in zip(axes.flat, pairs, colours):
        x = [r.get(xk) for r in matched_pol]
        y = [r.get(yk) for r in matched_pol]
        scatter_panel(ax, x, y, xl, yl, col)

    fig.suptitle('EDR/SAP composites vs Polity5 components\n'
                 'Cross-validation: isonomia hand-coded dataset vs Polity5',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'crossval_polity.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: crossval_polity.png")

    print(f"\n{'Isonomia var':20s}  {'Polity var':20s}  r       p      n")
    print("-" * 70)
    for xk, yk, xl, yl in pairs:
        x = [r.get(xk) for r in matched_pol]
        y = [r.get(yk) for r in matched_pol]
        valid = [(xi, yi) for xi, yi in zip(x, y)
                 if xi is not None and yi is not None]
        if len(valid) >= 5:
            xv, yv = zip(*valid)
            r_val, p_val = stats.pearsonr(xv, yv)
            print(f"  {xl:20s}  {yl:20s}  {r_val:.3f}   {p_val:.4f} {sig(p_val)}  n={len(valid)}")

    return matched_pol


def save_matched_csv(vdem_matched, polity_matched):
    """Save the matched dataset for reproducibility."""
    all_keys = set()
    for r in vdem_matched + polity_matched:
        all_keys.update(r.keys())
    all_keys = sorted(all_keys)
    with open(MATCHED_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for r in vdem_matched:
            writer.writerow({k: r.get(k, '') for k in all_keys})
    print(f"\nMatched dataset saved to {MATCHED_PATH}")


# ── Dry-run mode: show expected matches without external data ─────────────────

def dry_run(iso_systems):
    """Show which isonomia systems have modern-state matches, without loading
    external datasets. Useful for checking coverage before downloading data."""
    print("\n=== DRY RUN: expected cross-validation matches ===\n")
    print(f"Isonomia hand-coded systems with modern-state equivalents: "
          f"{sum(1 for s in ISONOMIA_TO_MODERN if s in iso_systems)} "
          f"of {len(ISONOMIA_TO_MODERN)} mappings defined")
    print()
    print(f"{'Isonomia system':45s}  {'Match':25s}  {'Year'}  "
          f"{'EDR':5s}  {'SAP':5s}")
    print("-" * 90)
    for sys_name, (country, iso3, year) in sorted(ISONOMIA_TO_MODERN.items()):
        if sys_name in iso_systems:
            iso = iso_systems[sys_name]
            print(f"  {sys_name[:43]:43s}  {country:25s}  {year}  "
                  f"{iso['EDR']:.2f}   {iso['SAP']:.2f}")
        else:
            print(f"  {sys_name[:43]:43s}  {country:25s}  {year}  "
                  f"[not in hand-coded dataset]")
    print()
    print("To run full validation:")
    print("  1. Download V-Dem v16 CSV from https://www.v-dem.net/data/the-v-dem-dataset/")
    print("     → 'Country-Year: V-Dem Full+Others version 16' → unzip → find .csv")
    print("  2. Download Polity5 from https://www.systemicpeace.org/inscrdata.html")
    print("     → 'Polity5 Annual Time-Series' → open in Excel → Save As CSV")
    print("  3. (Optional) Download Seshat Equinox-2020 from https://seshat-db.com/downloads_page/")
    print("     (free registration required)")
    print("  4. Run:")
    print("     python src/crossvalidate_edr.py \\")
    print("         --vdem   path/to/V-Dem-CY-Full+Others-v16.csv \\")
    print("         --polity path/to/p5v2018d.csv \\")
    print("         --seshat path/to/Equinox2020_05_2023.csv  # optional")



# ── Seshat Equinox-2020 cross-validation ──────────────────────────────────────

SESHAT_MAPPING = [
    ('Early Uruk',                          'IqUruk*', 'Mesopotamia c.4000 BCE'),
    ('Ubaid Culture',                       'IqUbaid', 'Mesopotamia c.5500 BCE'),
    ('Egyptian Old Kingdom',                'EgOldK1', 'Egypt c.2650 BCE'),
    ('Egyptian Middle Kingdom',             'EgMidKg', 'Egypt c.2000 BCE'),
    ('Egyptian Nomarchies',                 'EgRegns', 'Egypt c.2150 BCE'),
    ('Tang Dynasty',                        'CnTangE', 'China c.650 CE'),
    ('Inca Empire (Tawantinsuyu)',           'PeInca*', 'Andes c.1450 CE'),
    ('Aztec Triple Alliance',               'MxAztec', 'Mexico c.1480 CE'),
    ('Iroquois Confederacy / Haudenosaunee','UsIroqE',  'NE America c.1600 CE'),
    ('Althingi Carbon-Neutral Parliament',  'IsCommw',  'Iceland c.1000 CE'),
    ('Mauryan Empire',                      'InMaury',  'India c.250 BCE'),
    ('Ottoman Empire',                      'TrOttm2',  'Anatolia c.1600 CE'),
    ('\u00c7atalh\u00f6y\u00fck',        'TrNeoLT',  'Konya Plain c.7000 BCE'),
    ('Roman Republic',                      'ItRomMR',  'Latium c.200 BCE'),
]

# Seshat variables → isonomia dimension
SESHAT_VARS = [
    'Administrative levels', 'Full-time bureaucrats', 'Merit promotion',
    'Formal legal code', 'Examination system', 'Professional soldiers',
    'Military levels', 'Settlement hierarchy', 'Written records', 'Script',
    'Constraint on executive by government',
    'Constraint on executive by non-government', 'elite status is hereditary',
]

# Download:
#   Seshat Equinox-2020: https://seshat-db.com/downloads_page/
#   (requires free registration)
#   File: Equinox2020_05_2023.xlsx or .csv (both accepted)

def load_seshat(seshat_path):
    """Load Seshat Equinox-2020 XLSX or CSV and return per-polity variable means."""
    import pathlib
    print(f"Loading Seshat from {seshat_path}...")
    suffix = pathlib.Path(seshat_path).suffix.lower()
    try:
        import pandas as _pd
        if suffix in ('.xlsx', '.xlsm'):
            df = _pd.read_excel(seshat_path, engine='openpyxl')
        elif suffix == '.xls':
            df = _pd.read_excel(seshat_path, engine='xlrd')
        else:
            # CSV — try utf-8 then latin-1
            for enc in ('utf-8', 'utf-8-sig', 'latin-1', 'cp1252'):
                try:
                    df = _pd.read_csv(seshat_path, encoding=enc, low_memory=False)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise RuntimeError(f"Cannot decode {seshat_path}")
    except Exception as e:
        raise RuntimeError(f"Could not load Seshat file: {e}")

    def _encode(v):
        if _pd.isna(v): return None
        s = str(v).strip().lower()
        if s in ('present', 'yes', '1', 'true', 'inferred present'): return 1.0
        if s in ('absent', 'no', '0', 'false', 'inferred absent'): return 0.0
        if s in ('unknown', 'suspected unknown'): return None
        try: return float(s)
        except: return None

    polity_data = {}
    for var in SESHAT_VARS:
        sub = df[df['Variable'] == var][['Polity', 'Value.From']].copy()
        sub['val'] = sub['Value.From'].apply(_encode)
        sub = sub.dropna(subset=['val'])
        for polity, val in sub.groupby('Polity')['val'].mean().items():
            if polity not in polity_data: polity_data[polity] = {}
            polity_data[polity][var] = val

    print(f"  Loaded {len(polity_data):,} Seshat polities with variable data")
    return polity_data


def run_seshat_validation(iso_systems, seshat_path):
    """Cross-validate isonomia SAP dimensions against Seshat social complexity."""
    import numpy as np

    seshat = load_seshat(seshat_path)

    matched = []
    for iso_name, ses_code, desc in SESHAT_MAPPING:
        if iso_name not in iso_systems or ses_code not in seshat:
            continue
        iso = iso_systems[iso_name]
        sd  = seshat[ses_code]

        # Normalise Seshat ordinals to 0-1 before storing
        adm_raw = sd.get('Administrative levels')
        mil_raw = sd.get('Military levels')
        adm_n = min(adm_raw / 8.0, 1.0) if adm_raw is not None else None
        mil_n = min(mil_raw / 6.0, 1.0) if mil_raw is not None else None

        # Build composites
        def _mean(*vals):
            clean = [v for v in vals if v is not None]
            return float(np.mean(clean)) if clean else None

        row = {
            'system': iso_name, 'seshat_id': ses_code, 'period': desc,
            'iso_A':   iso['A'], 'iso_I': iso['I'],
            'iso_S':   iso['S'], 'iso_D': iso['D'],
            'iso_SAP': iso['SAP'], 'iso_EDR': iso['EDR'],
            # Store normalised individual variables
            'ses_admin_levels_n':   adm_n,
            'ses_military_levels_n': mil_n,
            'ses_bureaucrats':      sd.get('Full-time bureaucrats'),
            'ses_merit':            sd.get('Merit promotion'),
            'ses_writing':          sd.get('Written records'),
            'ses_script':           sd.get('Script'),
            'ses_profsoldiers':     sd.get('Professional soldiers'),
            'ses_legal':            sd.get('Formal legal code'),
            'ses_constr_gov':       sd.get('Constraint on executive by government'),
            'ses_constr_nongov':    sd.get('Constraint on executive by non-government'),
            # Composites (all on 0-1 scale)
            'ses_A': _mean(adm_n,
                           sd.get('Full-time bureaucrats'),
                           sd.get('Merit promotion')),
            'ses_I': _mean(sd.get('Written records'),
                           sd.get('Script')),
            'ses_S': _mean(sd.get('Professional soldiers'), mil_n),
            'ses_D': _mean(sd.get('Formal legal code'),
                           sd.get('Constraint on executive by government'),
                           sd.get('Constraint on executive by non-government')),
        }
        matched.append(row)
        a_str = f"{row['ses_A']:.2f}" if row['ses_A'] is not None else '—'
        i_str = f"{row['ses_I']:.2f}" if row['ses_I'] is not None else '—'
        print(f"  ✓ {iso_name[:38]:38s}  A={a_str}  I={i_str}")

    print(f"\n  Matched {len(matched)} isonomia ↔ Seshat pairs")
    if len(matched) < 4:
        print("  Insufficient matches for Seshat cross-validation")
        return

    # Correlations
    print(f"\n{'Isonomia':22s}  {'Seshat proxy':30s}  r       p      n")
    print("-" * 70)
    comparisons = [
        ('iso_A',   'ses_A', 'A (admin index)',         'Seshat admin composite'),
        ('iso_I',   'ses_I', 'I (info infrastructure)', 'Seshat writing composite'),
        ('iso_S',   'ses_S', 'S (sovereignty)',         'Seshat military composite'),
        ('iso_D',   'ses_D', 'D (disobedience)',        'Seshat legal composite'),
        ('iso_SAP', 'ses_A', 'SAP composite',           'Seshat admin composite'),
    ]
    for xk, yk, xl, yl in comparisons:
        pairs = [(r[xk], r[yk]) for r in matched
                 if r.get(xk) is not None and r.get(yk) is not None]
        if len(pairs) < 4:
            print(f"  {xl:22s}  {yl:28s}  insufficient data (n={len(pairs)})")
            continue
        from scipy import stats as _stats
        x, y = zip(*pairs)
        r_val, p_val = _stats.pearsonr(x, y)
        print(f"  {xl:22s}  {yl:28s}  {r_val:.3f}   {p_val:.4f} {sig(p_val)}  n={len(pairs)}")

    # Save figure — legend-based design: one colour+marker per civilisation,
    # shared across all three panels; no inline text annotations.
    try:
        import matplotlib.pyplot as _plt
        import matplotlib.lines as _ml
        import numpy as _np
        from scipy import stats as _stats
        _plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

        # Short display names for legend
        SHORT = {
            'Early Uruk':                           'Early Uruk',
            'Ubaid Culture':                        'Ubaid Culture',
            'Egyptian Old Kingdom':                 'Old Kingdom',
            'Egyptian Middle Kingdom':              'Middle Kingdom',
            'Egyptian Nomarchies':                  'Egypt (Nomarchies)',
            'Tang Dynasty':                         'Tang Dynasty',
            'Inca Empire (Tawantinsuyu)':           'Inca Empire',
            'Aztec Triple Alliance':                'Aztec Empire',
            'Iroquois Confederacy / Haudenosaunee': 'Iroquois Confederacy',
            'Althingi Carbon-Neutral Parliament':   'Iceland (Althingi)',
            'Mauryan Empire':                       'Mauryan Empire',
            'Ottoman Empire':                       'Ottoman Empire',
            '\u00c7atalh\u00f6y\u00fck':           '\u00c7atalh\u00f6y\u00fck',
            'Roman Republic':                       'Roman Republic',
        }

        # Stable colour palette — 14 visually distinct colours
        PALETTE = [
            '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
            '#a65628', '#f781bf', '#999999', '#1b9e77', '#d95f02',
            '#7570b3', '#e7298a', '#66a61e', '#e6ab02',
        ]
        # Marker cycle — helps distinguish points even in greyscale
        MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X', 'h',
                   'o', 's', '^', 'D', 'v', 'P']

        # Build a stable index → (colour, marker, label) mapping across the
        # full SESHAT_MAPPING list so the legend is consistent across panels.
        system_style = {}
        for i, (iso_name, _, _desc) in enumerate(SESHAT_MAPPING):
            system_style[iso_name] = (PALETTE[i % len(PALETTE)],
                                      MARKERS[i % len(MARKERS)],
                                      SHORT.get(iso_name, iso_name))

        # Layout: 3 scatter panels + legend panel on the right
        fig = _plt.figure(figsize=(16, 5))
        # Ratios: three equal scatter panels + one narrow legend column
        gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.55],
                              wspace=0.35)
        axes = [fig.add_subplot(gs[0, i]) for i in range(3)]

        legend_handles = {}  # system → handle, built from first panel that plots it

        for ax, (xk, yk, xl, yl) in zip(axes, comparisons[:3]):
            pairs = [(r[xk], r[yk], r['system']) for r in matched
                     if r.get(xk) is not None and r.get(yk) is not None]
            if len(pairs) < 4:
                continue
            xv, yv, lv = zip(*pairs)
            xv = [float(v) for v in xv]
            yv = [float(v) for v in yv]

            for x, y, l in zip(xv, yv, lv):
                colour, marker, label = system_style.get(
                    l, ('#555555', 'o', l[:18]))
                sc = ax.scatter(x, y, c=colour, marker=marker,
                                s=60, alpha=0.9, edgecolors='white',
                                linewidths=0.5, zorder=4)
                if l not in legend_handles:
                    legend_handles[l] = _ml.Line2D(
                        [], [], marker=marker, color='w',
                        markerfacecolor=colour, markeredgecolor='white',
                        markersize=7, label=label)

            r_val, p_val = _stats.pearsonr(xv, yv)
            m, b = _np.polyfit(xv, yv, 1)
            xr = _np.linspace(min(xv), max(xv), 100)
            ax.plot(xr, m * xr + b, 'k--', lw=1.2, alpha=0.4)
            title_col = ('darkgreen' if abs(r_val) >= 0.7
                         else '#b8860b' if abs(r_val) >= 0.5
                         else 'darkred')
            ax.set_title(f'r={r_val:.3f} {sig(p_val)}  n={len(xv)}',
                         fontsize=9.5, color=title_col)
            ax.set_xlabel(xl, fontsize=9)
            ax.set_ylabel(yl, fontsize=9)

        # Legend panel — ordered by SESHAT_MAPPING for stability
        ax_leg = fig.add_subplot(gs[0, 3])
        ax_leg.axis('off')
        ordered_handles = [legend_handles[m[0]]
                           for m in SESHAT_MAPPING
                           if m[0] in legend_handles]
        ax_leg.legend(handles=ordered_handles, loc='center left',
                      fontsize=8, frameon=True, framealpha=0.9,
                      edgecolor='#cccccc', title='Polity', title_fontsize=8.5,
                      handlelength=1.2, handletextpad=0.6, borderpad=0.8)

        fig.suptitle('Seshat Equinox-2020 cross-validation (pre-modern, n=14)\n'
                     'SAP dimensions vs Seshat social complexity variables',
                     fontsize=11, fontweight='bold')
        _plt.savefig(os.path.join(OUTPUT_DIR, 'crossval_seshat.png'),
                     dpi=150, bbox_inches='tight')
        _plt.close()
        print("Saved: crossval_seshat.png")
    except Exception as e:
        print(f"  Figure not saved: {e}")



# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cross-validate EDR against V-Dem and Polity5')
    parser.add_argument('--vdem',   help='Path to V-Dem CSV (Full+Others)')
    parser.add_argument('--polity', help='Path to Polity5 CSV')
    parser.add_argument('--seshat', help='Path to Seshat Equinox-2020 XLSX')
    args = parser.parse_args()

    iso_systems = load_isonomia()
    print(f"Loaded {len(iso_systems)} hand-coded isonomia systems")

    if not args.vdem and not args.polity and not args.seshat:
        dry_run(iso_systems)
        sys.exit(0)

    vdem_matched  = []
    polity_matched = []

    if args.seshat:
        run_seshat_validation(iso_systems, args.seshat)

    if args.vdem:
        vdem = load_vdem(args.vdem)
        vdem_matched = match_vdem(iso_systems, vdem)
        run_vdem_validation(vdem_matched)

    if args.polity:
        polity = load_polity(args.polity)
        polity_matched = run_polity_validation(iso_systems, polity)

    if vdem_matched or polity_matched:
        save_matched_csv(vdem_matched, polity_matched)

    print("\nDone.")
