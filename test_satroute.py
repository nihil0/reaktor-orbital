'''
Test module for SatRoute
'''

import unittest,satroute

class TestSatroute(unittest.TestCase):
    def test_to_cartesian(self):
        def sat_position(h,lat,lon):
            my_sat = satroute.Satellite('dummy',h,lat,lon)
            return tuple(round(m,6) for m in (my_sat.x,my_sat.y,my_sat.z))

        self.assertEqual(sat_position(0,0,0),(satroute.earth_radius,0.0,0.0))
        self.assertEqual(sat_position(0,90,0),(0.0,0.0,satroute.earth_radius))
        self.assertEqual(sat_position(0,0,90),(0.0,satroute.earth_radius,0.0))



if __name__ == '__main__':
    unittest.main()
