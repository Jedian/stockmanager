# -*- coding: utf-8 -*-

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
        self.productionData = self.model.Data('./database/corte.csv')
        self.sellData = self.model.Data('./database/venda.csv')
        self.productsData = self.model.Data('./database/produtos.csv')

    def getStockPageContent(self, page=1):
        production = self.productionData.getContent(page).values
        sells = self.sellData.getContent(page).values
        products = self.productsData.getContent(page).values

        stockcontent = []
        sizes = ['ref', 'pp', 'p', 'm', 'g', 'gg', 'xgg']
        for rp, rs in izip(production, sells):
            rp[0] = int(rp[0])
            ref = {'ref': rp[0], 'val': {}}
            for i in xrange(1, 7):
                rp[i] = int(rp[i])
                rs[i] = int(rs[i])
                ref['val'][sizes[i]] = {'p': rp[i], 's': rs[i], 'st': rp[i]-rs[i]}
            stockcontent.append(ref)

        productscontent = {}

        for row in products:
            productscontent[row[0]] = row[1]

        return stockcontent, productscontent
        #fazer as conta e mostrar a planilha bonitinha

    def saveData(self, data, datatype):
        if datatype == 'venda':
            dbdata = self.sellData.getContent('all')
        else:
            dbdata = self.productionData.getContent('all')

        pos = 0
        refpos = {}
        for row in dbdata['ref']:
            refpos[str(row)] = pos
            pos = pos+1

        print dbdata
        print data
        for ref in data:
            for tam in data[ref]:
                if str(ref) not in refpos:
                    raise Exception('ERRO: Referência ' + str(ref) + ' não existe')
                dbdata[tam][refpos[str(ref)]] = int(dbdata[tam][refpos[str(ref)]]) + int(data[ref][tam])

        if datatype == 'venda':
            self.sellData.saveData(dbdata)
        else:
            self.productionData.saveData(dbdata)
