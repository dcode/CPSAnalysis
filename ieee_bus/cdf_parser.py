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
	    print "Done."

    def Parse( self, data ):

        lines = data.splitlines()
	cur_line = 0

        fields = {}

        # Title Data
        fields['date'] =      lines[0][1:9].strip()
        fields['orig_name'] = lines[0][10:30].strip()
        fields['mva_base'] =  lines[0][31:37].strip()
        fields['year'] =      lines[0][38:42].strip()
        fields['season'] =    lines[0][43].strip()
        fields['case_id'] =   lines[0][45:73].strip()
	cur_line += 1
        
        # Bus Data Header
        bus_qty = int(lines[cur_line][17:].split()[0])
	cur_line += 1
        fields['bus_qty'] = bus_qty
        
        # Bus Data
        busses = []
        
	for line in lines[cur_line:(cur_line+bus_qty)]:
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
	cur_line += max(1, bus_qty)

        assert( lines[cur_line].strip() == "-999" )
	cur_line += 1

        # Branch Data Header
        branch_qty = int(lines[cur_line][20:].split()[0])
	cur_line += 1
        fields['branch_qty'] = branch_qty

        # Branch Data
        branches=[]
        for line in lines[cur_line:(cur_line+branch_qty)]:
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
	cur_line += max(1, branch_qty)

        assert( lines[cur_line].strip() == "-999" )
	cur_line += 1

	# Loss Zone data - qty column is fuzzy, but anything after 16 should suffice
	losszone_qty = int(lines[cur_line][20:].split()[0] )
	cur_line += 1

	# Loss Zone data
	zones = []
	for line in lines[cur_line:(cur_line+losszone_qty)]:
	    zone = {}
	    zone['number'] = int(line[0:3].strip())
	    zone['name'] = line[4:14].strip()

	    zones.append(zone)

	fields['loss_zones'] = zones
	cur_line += max(1, losszone_qty)

	assert( lines[cur_line].strip() == "-99" )
	cur_line += 1

	# Interchange - qty column is fuzzy, but anything after 25 should suffice
	interchange_qty = int(lines[cur_line][26:].split()[0] )
	cur_line += 1

	# Interchange Data
	interchanges = []
        for line in lines[cur_line:(cur_line+interchange_qty)]:
            interchange = {}
            interchange['num'] = int( line[0:2].strip() )
            interchange['slack_bus'] = int( line[4:7].strip() )
            interchange['alt_swing'] = line[9:20]
            interchange['area_export'] = float( line[20:27].strip() )
            interchange['area_tolerance'] = float( line[31:35].strip() )
            interchange['area_code'] = line[38:43].strip()
            interchange['area_name'] = line[45:75].strip()

            interchanges.append(interchange)

	fields['interchanges'] = interchanges
	cur_line += max(1, interchange_qty)

	assert( lines[cur_line].strip() == "-9" )
	cur_line += 1

	# Tie Lines - qty column is fuzzy, but anything after 18 should suffice
	tieline_qty = int(lines[cur_line][19:].split()[0] )

	# Tie Line Data
	tielines = []
        for line in lines[cur_line:(cur_line+tieline_qty)]:
            tieline = {}
            tieline['metered_bus'] = int( line[0:4].strip() )
            tieline['metered_area'] = int( line[6:8].strip() )
            tieline['non-metered_bus'] = int( line[10:14].strip() )
            tieline['non-metered_area'] = int( line[16:18].strip() )
	    tieline['circuit'] = int( line[20:22].strip() )

            tielines.append(tieline)

	fields['tielines'] = tielines
	cur_line += max(1, tieline_qty)

	assert( lines[cur_line].strip() == "-999" )
	cur_line += 1

        self.fields = fields
	
	print "Number of Buses: ", bus_qty	
	print "Number of Branches: ", branch_qty
	print "Number of Loss Zones: ", losszone_qty 
	print "Number of Interchanges: ", interchange_qty
	print "Number of Tie Lines: ", tieline_qty
       
    def get_graph( self ):
	pass


if __name__ == '__main__':
	import sys
	print "Testing CDFParser"
	print
	if len(sys.argv) != 2:
		print "pass filename of CDF file for parsing."

	parser = CDFParser( sys.argv[1] )

