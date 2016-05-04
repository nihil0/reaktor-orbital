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

    def test_is_visible(self):
        sat1 = satroute.Satellite('1',90,0,0)
        sat2 = satroute.Satellite('2',0,0,0)
        self.assertFalse(satroute.is_visible(sat1,sat2))

        sat1 = satroute.Satellite('1',90,0,2*satroute.earth_radius)
        sat2 = satroute.Satellite('2',0,0,2*satroute.earth_radius)
        self.assertTrue(satroute.is_visible(sat1,sat2))




if __name__ == '__main__':
    unittest.main()
