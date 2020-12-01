import pstats
p = pstats.Stats('prof/combined.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(r'^test_.*(?<!\(setup_function\))$')
