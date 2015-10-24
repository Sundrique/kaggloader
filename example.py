from kaggloader import KaggLoader

competition = 'titanic'

loader = KaggLoader()
loader.download_all(competition)
