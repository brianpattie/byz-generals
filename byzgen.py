import threading

class General(threading.Thread):

    def __init__(self, loyal, commander):
        threading.Thread.__init__(self)
        self.loyal
        self.commander
        self.buffer

    def run(self):
        print("Running")

    def majority(orders):
        values = []
        counts = []

        # count occurences of each order
        for o in orders:
            if o not in values:
                values.append(o)
                counts.append(orders.count(o))

        #check for ties
        m = max(counts)
        if counts.count(m) > 1:
            #Tie -> take default option
            return #TODO ADD VALUE HERE

        try:
            i = counts.index(m)
        except:
            print("Something has gone horribly wrong")
            # TODO is this a possibility?

        return values[i]
