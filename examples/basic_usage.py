from cool_memories.core import FragmentEngine
f=FragmentEngine()
for theme in ["america","media","technology","desire"]:
    info=f.get_theme(theme)
    print(f"{theme}: {info['description']}")
print(f"\nRandom fragment: {f.generate_fragment()}")
print(f"\nChronology:")
for e in f.chronology(): print(f"  {e['year']}: {e['event']}")
