#!/usr/bin/python
import BaseHTTPServer
import cgi
import sys
import xgboost as xgb
import lightgbm as lgb
import numpy as np
import pandas as pd
import json
import pdb
from pprint import pformat

if len(sys.argv) == 1:
    PORT = 8000
else:
    PORT = int(sys.argv[1])

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def do_POST(self, *args, **kwargs):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = json.loads(post_data)
        data1 = {}
        data2 = {}
        data2['fullbathcnt'],data1['FullBath'] = data['Full_Bath'],[int(data['Full_Bath'][0])]
        data2['garagetotalsqft'],data1['GarageArea'] = data['Garage_Area'],[int(data['Garage_Area'][0])]
        data2['yearbuilt'],data1['YearBuilt'] = data['Year_Built'],[int(data['Year_Built'][0])]
        data2['buildingqualitytypeid'],data1['OverallQual'] = data['Building_Qualit'],[int(data['Building_Qualit'][0])]
        data2['fireplacecnt'],data1['Fireplaces'] = data['Fire_Places'],[int(data['Fire_Places'][0])]
        data2['lotsizesquarefeet'],data1['LotArea'] = data['Lot_Area'],[int(data['Lot_Area'][0])]
        data2['finishedsquarefeet15'],data1['TotalSF'] = data['Total_Area'],[int(data['Total_Area'][0])]
        data2['finishedsquarefeet6'],data1['TotalBsmtSF'] = data['Total_BsmtS'],[int(data['Total_BsmtS'][0])]
        data2['roomcnt'],data1['TotRmsAbvGrd'] = data['Room_Count'],[int(data['Room_Count'][0])]
        data2['poolsizesum'],data1['PoolArea'] = data['Pool_Area'],[int(data['Pool_Area'][0])]
        data2['garagecarcnt'],data1['GarageCars'] = data['Garage_Cars'], [int(data['Garage_Cars'][0])]
        data2['threequarterbathnbr'],data1['HalfBath'] = data['Half_Bath'],[int(data['Half_Bath'][0])]
        data2['basementsqft'],data1['BsmtFinSF1'] = data['Basement_Area'],[int(data['Basement_Area'][0])]
        data2['finishedfloor1squarefeet'],data1['1stFlrSF'] = data['1st_Floor_Square_Feet'],[int(data['1st_Floor_Square_Feet'][0])]

        xgb_model = xgb.Booster(model_file='XGB_model2.model')            
        clf = lgb.Booster(model_file='lgb_model_logerror.txt')

        df_test_logerror = pd.DataFrame.from_dict(data2, orient = 'columns')
        for c in df_test_logerror.dtypes[df_test_logerror.dtypes == object].index.values:
            df_test_logerror[c] = (df_test_logerror[c] == True)
        df_test_logerror = df_test_logerror.values.astype(np.float32, copy=False)
        p_logerror = clf.predict(df_test_logerror)
        df_test_price = pd.DataFrame.from_dict(data1,orient = 'columns')
        df_test_price = xgb.DMatrix(df_test_price)

        pred_price = xgb_model.predict(df_test_price)
        pred_price = np.expm1(pred_price)
        body = str(pred_price[0]) +','+ str(p_logerror.tolist()[0])
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)
        self.wfile.close()

    def do_GET(self, *args, **kwargs):
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.end_headers()
        body = 'ib'
        self.wfile.write(body)
        self.wfile.close()


def httpd(handler_class=MyHandler, server_address=('0.0.0.0', PORT), file_=None):
    try:
        print "Server started on http://%s:%s" % (server_address[0], server_address[1])
        srvr = BaseHTTPServer.HTTPServer(server_address, handler_class)
        srvr.serve_forever()  # serve_forever
    except KeyboardInterrupt:
        srvr.socket.close()


if __name__ == "__main__":
    """ ./corsdevserver.py """
    httpd()
