def define_tdah_join_strategy():
    """Stratégie de jointure pour les données TDAH"""
    return {
        'primary_key': 'code_region_insee',
        'join_mappings': {
            'densite_podopsychiatres': ['code_region', 'annee'],
            'population_insee': ['code_region', 'age_groupe'],
            'methylphenidate': ['region_code', 'periode'],
            'pauvrete_regionale': ['code_insee_region']
        },
        'temporal_alignment': {
            'reference_year': 2022,
            'tolerance_years': 1
        }
    }
