def parse_args():
    parser = argparse.ArgumentParser(
        description="MultiVerify — identyfikacja multimodalna"
    )
    parser.add_argument("--face", required=True,
        help="Sciezka do zdjecia probe")
    parser.add_argument("--voice", required=True,
        help="Sciezka do nagrania probe")
    parser.add_argument("--threshold", type=float, default=0.7)
    parser.add_argument("--strategy",
        choices=FusionEngine.STRATEGIES, default="weighted")
    return parser.parse_args()
