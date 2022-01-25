class fish:
    def __init__(self, entry):
        self.species = entry['\ufeffSpecies']
        self.stats = {}
        for key in list(entry.keys()):
            if key!='\ufeffSpecies':
                self.stats[key] = [float(entry[key])]

    def update(self, entry):
        '''Add new entry to fish's stats'''
        for key in list(entry.keys()):
            if key!='\ufeffSpecies':
                self.stats[key].append(float(entry[key]))

    def average(self):
        '''Returns the average stats for the fish'''
        mean_fish = {}
        mean_fish['Species'] = self.species
        for key in list(self.stats.keys()):
            if key!='\ufeffSpecies':
                mean_fish[key] = sum(self.stats[key]) / len(self.stats[key])
        return(mean_fish)
