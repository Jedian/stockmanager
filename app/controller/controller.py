from itertools import izip

class StockManagerController():
    def __init__(self, model, view, controller):
        self.view = view
        self.model = model
        # self.other_controllers = ...
        
        self.loadDatabase()

    def start(self):
        self.view = self.view.StockManagerView(controller=self)
        self.view.mainloop()

    def loadDatabase(self):
        self.productionData = self.model.Data('../database/corte.csv')
        self.sellData = self.model.Data('../database/venda.csv')

    def getStockPageContent(self, page=1):
        production = self.productionData.getContent(page).values
        sells = self.sellData.getContent(page).values
        
        stockcontent = []

        sizes = ['pp', 'p', 'm', 'g', 'gg', 'xgg']
        for rp, rs in izip(production, sells):
            rp[0] = int(rp[0])
            ref = {'ref': rp[0], 'val': {}}
            for i in xrange(0, len(sizes)):
                rp[i] = int(rp[i])
                rs[i] = int(rs[i])
                ref['val'][sizes[i]] = {'p': rp[i], 's': rs[i], 'st': rp[i]-rs[i]}
            stockcontent.append(ref)

        return stockcontent
        #fazer as conta e mostrar a planilha bonitinha
