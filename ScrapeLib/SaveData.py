import os
import openpyxl
from openpyxl.utils import get_column_letter

class SaveData:
    def __init__(self, path = '', logPath = ''):
        if path == '':
            pass
        elif not os.path.exists(path):
            os.makedirs(path)
        self.path = path

    def excelWriter(self, df, node = '1', if_exists = 'replace', sheet_name = 'Sheet1', encoding = 'utf-8'):
        if if_exists == 'append' or if_exists == 'append_ignore':
            try:
                wb = openpyxl.load_workbook(self.path + node + '.xlsx')
                ws = wb.get_sheet_by_name(sheet_name)
            except Exception as what:
                wb = openpyxl.workbook.Workbook()
                ws = wb.create_sheet(sheet_name, 0)
        elif if_exists == 'replace':
            wb = openpyxl.workbook.Workbook()
            ws = wb.create_sheet(sheet_name, 0)
        else:
            wb = openpyxl.workbook.Workbook()
            ws = wb.create_sheet(sheet_name, 0)

        # dfIndexs = df.index
        # dfColumns = df.columns
        # dfValues = df.values
        dfIndexs = df['indexs']
        dfColumns = df['columns']
        dfValues = df['values']

        for i in range(0, len(dfColumns)):
            index_col = i + 1
            index_row = 1
            col = get_column_letter(index_col + 1)
            ws.cell( '%s%s' %(col, index_row)).value = dfColumns[i]
        for i in range(0, len(dfIndexs)):
            index_row = dfIndexs[i] + 1
            ws.cell('A'+str(index_row)).value = dfIndexs[i]
            for j in range(0, len(dfColumns)):
                index_col = j + 1
                col = get_column_letter(index_col + 1)
                tmpValue = dfValues[i][j]
                try:
                    if (ws.cell('%s%s' %(col, index_row)).value is not None) and ws.cell('%s%s' %(col, index_row)).value != '':
                        if if_exists == 'append_ignore':
                            pass
                        elif if_exists == 'append' or if_exists == 'replace':
                            ws.cell( '%s%s' %(col, index_row)).value = str(tmpValue)
                    else:
                        ws.cell( '%s%s' %(col, index_row)).value = tmpValue
                    # ws['%s%s' %(col, index_row)] = int(tmpValue)
                except Exception as what:
                    pass
                    # # print 'encoding error: ', col, index_row, what
                    # self.logger.error('write excel raw error: ' + str(col) + ' ' + str(index_row) + ' |_| reading error ' + str(what))
        wb.save(filename = '%s%s.xlsx' % (self.path, unicode(node)))
