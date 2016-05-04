'''
Test module for SatRoute
'''

import unittest,satroute

class TestSatroute(unittest.TestCase):
    def test_to_cartesian(self):
        def sat_position(lat,lon,h):
            my_sat = satroute.Satellite('dummy',lat,lon,h)
            return tuple(round(m,6) for m in (my_sat.x,my_sat.y,my_sat.z))

        self.assertEqual(sat_position(0,0,0),(satroute.earth_radius,0.0,0.0))
        self.assertEqual(sat_position(0,90,0),(0.0,satroute.earth_radius,0.0))
        self.assertEqual(sat_position(90,0,0),(0.0,0.0,satroute.earth_radius))



if __name__ == '__main__':
    unittest.main()
