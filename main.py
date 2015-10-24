from kaggloader import KaggLoader

competition = 'the-allen-ai-science-challenge'
file_name = 'training_set.tsv.zip'

loader = KaggLoader()
loader.download(competition, file_name)
