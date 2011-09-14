"""
Parser for IEEE CDF format as defined at:
    http://www.ee.washington.edu/research/pstca/formats/cdf.txt
"""

import pprint
pp = pprint.PrettyPrinter(indent=4)

class CDFParser( object ):
    fields = {} 

    def __init__( self, filename=None ):
        if filename and type(filename) == type(""):
            data = open(filename).read()
            self.Parse( data )

    def Parse( self, data ):

        lines = data.splitlines()

        fields = {}

        # Title Data
        fields['date'] = lines[0][1:9].strip()
        fields['orig_name'] = lines[0][10:30].strip()
        fields['mva_base'] = lines[0][31:37].strip()
        fields['year'] = lines[0][38:42].strip()
        fields['season'] = lines[0][43].strip()
        fields['case_id'] = lines[0][45:73].strip()
        
        # Bus Data Header
        bus_qty = int(lines[1][17:].split()[0])
        fields['bus_qty'] = bus_qty
        
        # Bus Data
        busses = []
        for line in lines[2:2+bus_qty]:
            bus = {}
            bus['num'] = int(line[0:4].strip())
            bus['name'] = line[5:17].strip()
            bus['load_flow_area'] = int(line[18:20].strip())
            bus['loss_zone'] = int(line[20:23].strip())
            bus['type'] = int(line[24:26].strip())
            bus['final_v'] = float(line[27:33].strip())
            bus['final_theta'] = float(line[33:40].strip())
            bus['load_mw'] = float(line[40:49].strip())
            bus['load_mvar'] = float(line[49:59].strip())
            bus['gen_mv'] = float(line[59:67].strip())
            bus['gen_mvar'] = float(line[67:75].strip())
            bus['base_kv'] = float(line[76:83].strip())
            bus['desired_v'] = float(line[84:90].strip())
            bus['max_v'] = float(line[90:98].strip())
            bus['min_v'] = float(line[98:106].strip())
            bus['shunt_G'] = float(line[106:114].strip())
            bus['shunt_B'] = float(line[114:122].strip())
            bus['rc_bus'] = int(line[123:127].strip())

            busses.append(bus)
        
        fields['busses'] = busses

        assert( lines[2+bus_qty].strip() == "-999" )

        # Branch Data Header
        branch_qty = int(lines[3+bus_qty][20:].split()[0])
        fields['branch_qty'] = branch_qty

        # Branch Data
        branches=[]
        for line in lines[4+bus_qty:(4+bus_qty+branch_qty)]:
            branch = {}
            branch['tap_bus'] = int(line[0:4].strip())
            branch['z_bus'] = int(line[5:9].strip())
            branch['load_flow_area'] = int(line[10:12].strip())
            branch['loss_zone'] = int(line[13:15].strip())
            branch['circuit'] = int(line[16])
            branch['type'] = int(line[18])
            branch['R'] = float(line[19:29].strip())
            branch['X'] = float(line[29:40].strip())
            branch['B'] = float(line[40:50].strip())
            branch['mva1'] = float(line[50:55].strip())
            branch['mva2'] = float(line[56:61].strip())
            branch['mva3'] = float(line[62:67].strip())
            branch['ctrl_bus'] = int(line[68:72].strip())
            branch['side'] = int(line[73])
            branch['trans_turn_ratio'] = float(line[76:82].strip())
            branch['trans_final_theta'] = float(line[83:90].strip())
            branch['min_tap_shift'] = float(line[90:97].strip())
            branch['max_tap_shift'] = float(line[97:104].strip())
            branch['step_size'] = float(line[105:111].strip())
            branch['min_v'] = float(line[112:118].strip())
            branch['max_v'] = float(line[119:126].strip())

            branches.append(branch)

        fields['branches'] = branches

        assert( lines[4+bus_qty+branch_qty].strip() == "-999" )

        # TODO Add Loss Zone, Interchange, and Tie Line Data sections

        self.fields = fields
       
    def get_graph( self ):
        pass
