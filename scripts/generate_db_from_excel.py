#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERADOR DE BASE DE DATOS DESDE EXCEL
Lee el Excel del inventario y crea SQL con los componentes reales
"""

import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

# PATHS
EXCEL_PATH = Path("/mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front/Inventario_Cirujanosintetizadores.xlsx")
DB_PATH = Path("/mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front/backend/cirujano.db")
SQL_OUTPUT = Path("/mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front/database/cirujano_database.sql")

def normalize_resistance(value):
    """Normaliza valores de resistencia a Ohms"""
    try:
        ohms = float(value)
        if ohms >= 1_000_000:
            display = f"{ohms/1_000_000:.2g}MΩ"
        elif ohms >= 1_000:
            display = f"{ohms/1_000:.2g}kΩ"
        else:
            display = f"{ohms:.2g}Ω"
        return ohms, display
    except:
        return None, None

def normalize_capacitor(value):
    """Normaliza valores de capacitor"""
    try:
        val = float(str(value).replace('NP', '').strip())
        # Asumir que están en µF para cerámicos/electrolíticos
        farads = val * 1e-6
        display = f"{val:.2g}µF"
        return farads, display
    except:
        return None, None

def read_excel():
    """Lee el Excel y extrae componentes"""
    print("📖 Leyendo Excel...")
    df = pd.read_excel(EXCEL_PATH, sheet_name=0)
    
    components = {
        'resistors': [],
        'capacitors_ceramic': [],
        'capacitors_electrolytic': [],
        'integrated_circuits': [],
        'transistors': [],
        'diodes': []
    }
    
    # Resistencias
    if 'Resistencias' in df.columns:
        for val in df['Resistencias'].dropna():
            ohms, display = normalize_resistance(val)
            if ohms:
                components['resistors'].append({
                    'value_ohms': ohms,
                    'display_value': display,
                    'tolerance_percent': 5.0,
                    'power_watts': 0.25,
                    'technology': 'METAL_FILM',
                    'package': 'TH_AXIAL'
                })
    
    # Capacitores Cerámicos
    if 'Capacitores Ceramicos' in df.columns:
        for val in df['Capacitores Ceramicos'].dropna():
            farads, display = normalize_capacitor(val)
            if farads:
                components['capacitors_ceramic'].append({
                    'value_farads': farads,
                    'display_value': display,
                    'dielectric': 'CERAMIC',
                    'voltage_volts': 50.0,
                    'package': 'TH_RADIAL'
                })
    
    # Capacitores Electrolíticos
    if 'Capacitores Electrolíticos' in df.columns:
        for val in df['Capacitores Electrolíticos'].dropna():
            farads, display = normalize_capacitor(val)
            if farads:
                components['capacitors_electrolytic'].append({
                    'value_farads': farads,
                    'display_value': display,
                    'dielectric': 'ELECTROLYTIC_AL',
                    'voltage_volts': 25.0,
                    'polarized': True,
                    'package': 'TH_RADIAL'
                })
    
    # ICs
    if "Ic's" in df.columns:
        for val in df["Ic's"].dropna():
            pn = str(val).strip().upper()
            if pn:
                components['integrated_circuits'].append({
                    'part_number': pn,
                    'package': 'DIP',
                    'voltage_volts': 5.0
                })
    
    # Transistores
    if 'Transistores' in df.columns:
        for val in df['Transistores'].dropna():
            pn = str(val).strip().upper()
            if pn:
                components['transistors'].append({
                    'part_number': pn,
                    'type': 'BJT' if pn.startswith('2N') or pn.startswith('BC') else 'MOSFET',
                    'package': 'TO92'
                })
    
    # Diodos
    if 'Diodos' in df.columns:
        for val in df['Diodos'].dropna():
            pn = str(val).strip().upper()
            if pn:
                components['diodes'].append({
                    'part_number': pn,
                    'type': 'RECTIFIER',
                    'package': 'DO41'
                })
    
    return components

def generate_sql(components):
    """Genera SQL INSERT statements"""
    print("✍️  Generando SQL...")
    
    sql_lines = []
    sql_lines.append("-- CIRUJANO DB - Componentes desde Excel")
    sql_lines.append(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sql_lines.append("")
    
    # Resistencias
    for comp in components['resistors']:
        sql_lines.append(
            f"INSERT INTO comp_resistors (value_ohms, display_value, tolerance_percent, power_watts, technology, package) "
            f"VALUES ({comp['value_ohms']}, '{comp['display_value']}', {comp['tolerance_percent']}, {comp['power_watts']}, "
            f"'{comp['technology']}', '{comp['package']}');"
        )
    
    # Capacitores Cerámicos
    for comp in components['capacitors_ceramic']:
        sql_lines.append(
            f"INSERT INTO comp_capacitors (value_farads, display_value, dielectric, voltage_volts, package) "
            f"VALUES ({comp['value_farads']}, '{comp['display_value']}', '{comp['dielectric']}', {comp['voltage_volts']}, "
            f"'{comp['package']}');"
        )
    
    # Capacitores Electrolíticos (misma tabla, distinto dielectric)
    for comp in components['capacitors_electrolytic']:
        sql_lines.append(
            f"INSERT INTO comp_capacitors (value_farads, display_value, dielectric, voltage_volts, polarized, package) "
            f"VALUES ({comp['value_farads']}, '{comp['display_value']}', '{comp['dielectric']}', {comp['voltage_volts']}, "
            f"1, '{comp['package']}');"
        )
    
    # ICs
    for comp in components['integrated_circuits']:
        sql_lines.append(
            f"INSERT INTO comp_integrated_circuits (part_number, package, voltage_volts) "
            f"VALUES ('{comp['part_number']}', '{comp['package']}', {comp['voltage_volts']});"
        )
    
    # Transistores
    for comp in components['transistors']:
        sql_lines.append(
            f"INSERT INTO comp_transistors (part_number, type, package) "
            f"VALUES ('{comp['part_number']}', '{comp['type']}', '{comp['package']}');"
        )
    
    # Diodos
    for comp in components['diodes']:
        sql_lines.append(
            f"INSERT INTO comp_diodes (part_number, type, package) "
            f"VALUES ('{comp['part_number']}', '{comp['type']}', '{comp['package']}');"
        )
    
    return "\n".join(sql_lines)

def main():
    print("\n" + "="*60)
    print("GENERADOR DE DB - CIRUJANO SINTETIZADORES")
    print("="*60 + "\n")
    
    if not EXCEL_PATH.exists():
        print(f"❌ Excel no encontrado: {EXCEL_PATH}")
        return
    
    # Leer Excel
    components = read_excel()
    
    # Resumen
    print(f"\n📊 Componentes encontrados:")
    print(f"   • Resistencias: {len(components['resistors'])}")
    print(f"   • Capacitores Cerámicos: {len(components['capacitors_ceramic'])}")
    print(f"   • Capacitores Electrolíticos: {len(components['capacitors_electrolytic'])}")
    print(f"   • ICs: {len(components['integrated_circuits'])}")
    print(f"   • Transistores: {len(components['transistors'])}")
    print(f"   • Diodos: {len(components['diodes'])}")
    
    total = sum(len(v) for v in components.values())
    print(f"\n   ✅ TOTAL: {total} componentes\n")
    
    # Generar SQL
    sql = generate_sql(components)
    
    # Guardar SQL
    SQL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(SQL_OUTPUT, 'w') as f:
        f.write(sql)
    
    print(f"✅ SQL guardado en: {SQL_OUTPUT}\n")
    
    # Mostrar primeras líneas
    print("Primeras inserciones:")
    print("-" * 60)
    for line in sql.split('\n')[:10]:
        if line.strip():
            print(line[:80] + "...")
    print("-" * 60)
    print("\n✨ Listo para ejecutar en la base de datos\n")

if __name__ == "__main__":
    main()
