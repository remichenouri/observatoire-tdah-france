"""Test complet de l'installation."""

print("=== TEST INSTALLATION OBSERVATOIRE TDAH ===")

# Test imports essentiels
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import sqlite3  # Module built-in - doit marcher
    print("✅ Imports réussis")
except ImportError as e:
    print(f"❌ Erreur import: {e}")

# Test données TDAH
data = {
    'regions': ['Normandie', 'Île-de-France', 'PACA'], 
    'prevalence_tdah': [4.2, 5.1, 3.8]
}
df = pd.DataFrame(data)
print(f"\n📊 DataFrame test :\n{df}")

# Test SQLite (pour futures données)
conn = sqlite3.connect(':memory:')
df.to_sql('test_tdah', conn, index=False)
result = pd.read_sql('SELECT * FROM test_tdah', conn)
print(f"\n💾 Test SQLite :\n{result}")
conn.close()

print("\n🎉 Installation complète et fonctionnelle !")
