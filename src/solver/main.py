from src.solver.simulator import Report, Simulator


def test_report():
    test_words = ["book", "pumpkin", "moldova", "radiohead", "cuttlefish", "ice"]
    algorithm_names = ["char_prob", "wiki_1000", "wiki_10000"]
    data = [
        ('char_prob', 'book', 8),
        ('char_prob', 'pumpkin', 8),
        ('char_prob', 'moldova', 3),
        ('char_prob', 'radiohead', 3),
        ('char_prob', 'cuttlefish', 0),
        ('char_prob', 'ice', 2),
        ('wiki_1000', 'book', 3),
        ('wiki_1000', 'pumpkin', 5),
        ('wiki_1000', 'moldova', 5),
        ('wiki_1000', 'radiohead', 5),
        ('wiki_1000', 'cuttlefish', 3),
        ('wiki_1000', 'ice', 10),
        ('wiki_10000', 'book', 3),
        ('wiki_10000', 'pumpkin', 8),
        ('wiki_10000', 'moldova', 3),
        ('wiki_10000', 'radiohead', 3),
        ('wiki_10000', 'cuttlefish', 0),
        ('wiki_10000', 'ice', 10),
    ]

    report = Report(data, test_words, algorithm_names)
    print(report.dataframe)
    print(report.stats)


def run_simulator():
    simulator = Simulator(debug=True)
    report: Report = simulator.simulate()
    print(report.dataframe)
    print(report.stats)


if __name__ == '__main__':
    run_simulator()
