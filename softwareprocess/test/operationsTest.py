import unittest
import copy

import softwareprocess.dispatch as dispatch
import softwareprocess.operations.adjust as adjust
import softwareprocess.operations.correct as correct
import softwareprocess.operations.locate as locate
import softwareprocess.operations.predict as predict
import softwareprocess.operations.util


class operationsTest(unittest.TestCase):

    # 100 correct
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting: dictionary containing 'op': 'correct', validated.
    #       outputs:    sighting passed, unchanged.
    #   Happy Path
    #       dictionary containing only op
    #       dictionary containing extra values
    #
    # Happy Path
    def test100_010_ShouldPassPlainDictionary(self):
        sighting = dict()
        sighting['op'] = 'correct'
        actual = correct.correct(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    def test100_020_ShouldPassDictionaryWithAddedEntry(self):
        sighting = dict()
        sighting['op'] = 'correct'
        sighting['extra'] = 'ignore me'
        actual = correct.correct(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    # 200 locate
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting: dictionary containing 'op': 'locate', validated.
    #       outputs:    sighting passed, unchanged.
    #   Happy Path
    #       dictionary containing only op
    #       dictionary containing extra values
    #
    # Happy Path
    def test200_010_ShouldPassPlainDictionary(self):
        sighting = dict()
        sighting['op'] = 'locate'
        actual = locate.locate(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    def test200_020_ShouldPassDictionaryWithAddedEntry(self):
        sighting = dict()
        sighting['op'] = 'locate'
        sighting['extra'] = 'ignore me'
        actual = locate.locate(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    # 300 predict
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting: dictionary containing 'op': 'predict', validated.
    #       outputs:    sighting passed, unchanged.
    #   Happy Path
    #       dictionary containing only op
    #       dictionary containing extra values
    #
    # Happy Path
    def test300_010_ShouldPassPlainDictionary(self):
        sighting = dict()
        sighting['op'] = 'predict'
        actual = predict.predict(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    def test300_020_ShouldPassDictionaryWithAddedEntry(self):
        sighting = dict()
        sighting['op'] = 'predict'
        sighting['extra'] = 'ignore me'
        actual = predict.predict(sighting)
        self.assertEqual(actual, sighting, 'Should return unmodified')

    # 510 degreeStringToDegrees
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     degreeString: unvalidated string of the form '<x>d<y>',
    #                   where x is the amount of degrees, and y is the amount of minutes.
    #                   This value must be >= '0d0.1' and < '90d0.0'
    #
    #       outputs:    The value, in degrees.
    #   Happy Path
    #       nominal x, nominal y    '45d30.0'   -> 45.5
    #       nominal x, low y        '45d0.0'    -> 45.0
    #       nominal x, integer y    '45d0'      -> 45.0
    #       nominal x, high y       '45d59.9'   -> 45.99833..
    #       low x, nominal y        '0d30.0'    -> 0.5
    #       low x, low y            '0d0.1'     -> 0.00166...
    #       low x, high y           '0d59.9'    -> 0.99833...
    #       high x, nominal y       '89d30.0'   -> 89.5
    #       high x, low y           '89d0.0'    -> 89.0
    #       high x, high y          '89d59.9'   -> 89.99833...
    #   Sad Path
    #       no 'd'                  '85'        -> raise ValueError
    #       multiple 'd's           '45dd30.0'  -> raise ValueError
    #       negative x              '-15d30.0'  -> raise ValueError
    #       negative y              '45d-15.0'  -> raise ValueError
    #       too large y             '45d60.0'   -> raise ValueError
    #       value too small         '0d0.0'     -> raise ValueError
    #       value too large         '90d0.0'    -> raise ValueError
    #       non-integer x           '45.0d30.0' -> raise ValueError
    # Happy Path
    def test510_010ShouldCalculateNominalXNominalY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('45d30.0')
        self.assertAlmostEquals(actual, 45.5, 5)

    def test510_020ShouldCalculateNominalXLowY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('45d0.0')
        self.assertAlmostEquals(actual, 45.0, 5)

    def test510_030ShouldCalculateNominalXIntegerY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('45d0')
        self.assertAlmostEquals(actual, 45.0, 5)

    def test510_040ShouldCalculateNominalXHighY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('45d59.9')
        self.assertAlmostEquals(actual, 45.99833333, 5)

    def test510_050ShouldCalculateLowXLowY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('0d0.1')
        self.assertAlmostEquals(actual, 0.001666667, 5)

    def test510_060ShouldCalculateLowXNominalY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('0d30.0')
        self.assertAlmostEquals(actual, 0.5, 5)

    def test510_070ShouldCalculateLowXHighY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('0d59.9')
        self.assertAlmostEquals(actual, 0.99833333, 5)

    def test510_080ShouldCalculateHighXLowY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('89d0.0')
        self.assertAlmostEquals(actual, 89.0, 5)

    def test510_090ShouldCalculateHighXNominalY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('89d30.0')
        self.assertAlmostEquals(actual, 89.5, 5)

    def test510_100ShouldCalculateHighXHighY(self):
        actual = softwareprocess.operations.util.degreeStringToDegrees('89d59.9')
        self.assertAlmostEquals(actual, 89.99833333, 5)

    # Sad Path
    def test510_700FailIfNoD(self):
        expectedString = "No 'd' delimiter"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('85')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_710FailTooManyDs(self):
        expectedString = "Too many 'd' delimiters"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('45dd30.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_720NegativeX(self):
        expectedString = "Measurement too small"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('-15d30.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_730NegativeY(self):
        expectedString = "Negative number of minutes"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('45d-15.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_740TooLargeY(self):
        expectedString = "Number of minutes too large"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('45d60.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_750TooSmallValue(self):
        expectedString = "Measurement too small"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('0d0.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_760TooLargeValue(self):
        expectedString = "Measurement too large"
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('90d0.0')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test510_770TooLargeValue(self):
        with self.assertRaises(ValueError) as context:
            softwareprocess.operations.util.degreeStringToDegrees('45.0d0.0')

    # 520 degreesToDegreesString
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     degreeString: validated degree.
    #       outputs:    a string indicating the degree/minutes of the value.
    #   Happy Path
    #       Nominal x, Nominal y    45.5    -> '45d30.0'
    #       Nominal x, Zero y       45.0    -> '45d0.0'
    #       Low x, Nominal y        0.5     -> '0d30.0'
    #       High x, High y       89.99833333     -> '89d59.9'
    #   Sad Path
    #       None
    # Happy Path
    def test520_010NominalXNominalY(self):
        actual = softwareprocess.operations.util.degreesToDegreeString(45.5)
        self.assertEqual(actual, '45d30.0')

    def test520_020NominalXZeroY(self):
        actual = softwareprocess.operations.util.degreesToDegreeString(45.0)
        self.assertEqual(actual, '45d0.0')

    def test520_030LowXNominalY(self):
        actual = softwareprocess.operations.util.degreesToDegreeString(0.5)
        self.assertEqual(actual, '0d30.0')

    def test520_040HighXHighY(self):
        actual = softwareprocess.operations.util.degreesToDegreeString(89.9983333333)
        self.assertEqual(actual, '89d59.9')

    # 410 extractHeight
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting, a dictionary containing 'height', which should be a string
    #                   representation of a non-negative numeric value.
    #       outputs:    the non-negative numeric value represented.
    #                   otherwise, sets the error field of the dictionary and raises value error.
    #   Happy Path
    #       No Value                NONE    -> 0
    #       Low Value               '0'     -> 0
    #       Nominal Value         '25.2'    -> 25.2
    #       High Value            '999999.9'-> 999999.9
    #   Sad Path
    #       Non - String Value     'height' : 20    -> 'error': 'height is invalid', ValueError()
    #       String, non numeric    'height' : 'abc' -> 'error': 'height is invalid', ValueError()
    #       negative value         'height': '-1.0' -> 'error': 'height is invalid', ValueError()
    # Happy Path
    def test410_010_ShouldGetDefaultValue(self):
        actual = adjust.extractHeight({})
        self.assertAlmostEquals(actual, 0.0, 5)

    def test410_020_ShouldHandleLowValue(self):
        actual = adjust.extractHeight({'height': '0'})
        self.assertAlmostEquals(actual, 0.0, 5)

    def test410_030_ShouldHandleNominalValue(self):
        actual = adjust.extractHeight({'height': '25.2'})
        self.assertAlmostEquals(actual, 25.2, 5)

    def test410_040_ShouldHandleHighValue(self):
        actual = adjust.extractHeight({'height': '999999.9'})
        self.assertAlmostEquals(actual, 999999.9, 5)

    # Sad Paths
    def test410_910_ShouldHandleNonStringValue(self):
        input = {'height': 1}
        with self.assertRaises(ValueError):
            adjust.extractHeight(input)
        self.assertEqual(input['error'], 'height is invalid')

    def test410_920_ShouldHandleNonNumericStringValue(self):
        input = {'height': 'abc'}
        with self.assertRaises(ValueError):
            adjust.extractHeight(input)
        self.assertEqual(input['error'], 'height is invalid')

    def test410_920_ShouldHandleNonNumericStringValue(self):
        input = {'height': '-1.0'}
        with self.assertRaises(ValueError):
            adjust.extractHeight(input)
        self.assertEqual(input['error'], 'height is invalid')

    # 420 extractObservation
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting, a dictionary containing 'observation', which should be a string
    #                   representation of a non-negative numeric value.
    #       outputs:    the numeric value represented.
    #                   otherwise, sets the error field of the dictionary and raises value error.
    #   Happy Path:
    #       Nominal Value         '45d30.0'   -> 45.5
    #       The bulk of the testing for this is covered in tests 510 for degreeStringToDegrees
    #   Sad Path
    #       Non - String Value     'observation' : 20    -> 'error': 'observation is invalid', ValueError()
    #       No Value                NONE -> 'error': 'mandatory information is missing', ValueError()
    #       Bad Value               '45d-3.0'   -> 'error' : 'observation is invalid', ValueError()
    # Happy Path
    def test420_010_ShouldHandleNominalValue(self):
        input = {'observation': '45d30.0'}
        self.assertAlmostEqual(adjust.extractObservation(input), 45.5, 5)

    # Sad Paths
    def test420_910_ShouldHandleNonStringValue(self):
        input = {'observation': 20}
        with self.assertRaises(ValueError):
            adjust.extractObservation(input)
        self.assertEqual(input['error'], 'observation is invalid')

    def test420_920_ShouldHandleNoValue(self):
        input = {}
        with self.assertRaises(ValueError):
            adjust.extractObservation(input)
        self.assertEqual(input['error'], 'mandatory information is missing')

    def test420_930_ShouldHandleBadValue(self):
        input = {'observation': '45d-3.0'}
        with self.assertRaises(ValueError):
            adjust.extractObservation(input)
        self.assertEqual(input['error'], 'observation is invalid')

    # 430 extractTemperature
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting, a dictionary containing 'temperature', which should be a string
    #                   representation of an integer between -20 and 120.
    #       outputs:    the numeric value represented.
    #                   otherwise, sets the error field of the dictionary and raises value error.
    #   Happy Path:
    #       Nominal Value         '70'   -> 70
    #       Low Bound Value       '-20'  -> -20
    #       High Value            '120'  -> 120
    #       Default Value          NONE  -> 72
    #   Sad Path
    #       Non - String Value     'temperature' : 20    -> 'error': 'temperature is invalid', ValueError()
    #       Non - Integer String   '5.0'   -> 'error' : 'temperature is invalid', ValueError()
    #       Too Cold               '-21'   -> 'error' : 'temperature is invalid', ValueError()
    #       Too Hot                '121'   -> 'error' : 'temperature is invalid', ValueError()
    # Happy Path
    def test430_010_ShouldExtractNominalValue(self):
        actual = adjust.extractTemperature({'temperature': '70'})
        self.assertEqual(actual, 70)

    def test430_020_ShouldExtractLowValue(self):
        actual = adjust.extractTemperature({'temperature': '-20'})
        self.assertEqual(actual, -20)

    def test430_030_ShouldExtractHighValue(self):
        actual = adjust.extractTemperature({'temperature': '120'})
        self.assertEqual(actual, 120)

    def test430_040_ShouldExtractDefaultValue(self):
        actual = adjust.extractTemperature({})
        self.assertEqual(actual, 72)

    # Sad Paths
    def test430_910_ShouldHandleNonString(self):
        input = {'temperature': 20}
        with self.assertRaises(ValueError):
            adjust.extractTemperature(input)
        self.assertEqual(input['error'], 'temperature is invalid')

    def test430_920_ShouldHandleNonIntegerString(self):
        input = {'temperature': '20.0'}
        with self.assertRaises(ValueError):
            adjust.extractTemperature(input)
        self.assertEqual(input['error'], 'temperature is invalid')

    def test430_920_ShouldHandleTooCold(self):
        input = {'temperature': '-21'}
        with self.assertRaises(ValueError):
            adjust.extractTemperature(input)
        self.assertEqual(input['error'], 'temperature is invalid')

    def test430_920_ShouldHandleTooHot(self):
        input = {'temperature': '121'}
        with self.assertRaises(ValueError):
            adjust.extractTemperature(input)
        self.assertEqual(input['error'], 'temperature is invalid')

    # 440 extractPressure
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting, a dictionary containing 'pressure', which should be a string
    #                   representation of an integer between 100 and 1100.
    #       outputs:    the numeric value represented.
    #                   otherwise, sets the error field of the dictionary and raises value error.
    #   Happy Path:
    #       Nominal Value         '1000'   -> 1000
    #       Low Bound Value       '100'  -> 100
    #       High Value            '1100'  -> 1100
    #       Default Value          NONE  -> 1010
    #   Sad Path
    #       Non - String Value     1000    -> 'error': 'pressure is invalid', ValueError()
    #       Non - Integer String   '1000.0'-> 'error': 'pressure is invalid', ValueError()
    #       Too Low                '99'    -> 'error': 'pressure is invalid', ValueError()
    #       Too High               '1101'  -> 'error': 'pressure is invalid', ValueError()
    # Happy Path
    def test440_010_ShouldExtractNominalValue(self):
        actual = adjust.extractPressure({'pressure': '1000'})
        self.assertEqual(actual, 1000)

    def test440_020_ShouldExtractLowValue(self):
        actual = adjust.extractPressure({'pressure': '100'})
        self.assertEqual(actual, 100)

    def test440_030_ShouldExtractHighValue(self):
        actual = adjust.extractPressure({'pressure': '1100'})
        self.assertEqual(actual, 1100)

    def test440_040_ShouldExtractDefaultValue(self):
        actual = adjust.extractPressure({})
        self.assertEqual(actual, 1010)

    # Sad Paths
    def test440_910_ShouldHandleNonString(self):
        input = {'pressure': 1000}
        with self.assertRaises(ValueError):
            adjust.extractPressure(input)
        self.assertEqual(input['error'], 'pressure is invalid')

    def test440_920_ShouldHandleNonIntegerString(self):
        input = {'pressure': '1000.0'}
        with self.assertRaises(ValueError):
            adjust.extractPressure(input)
        self.assertEqual(input['error'], 'pressure is invalid')

    def test440_920_ShouldHandleTooLow(self):
        input = {'pressure': '99'}
        with self.assertRaises(ValueError):
            adjust.extractPressure(input)
        self.assertEqual(input['error'], 'pressure is invalid')

    def test440_920_ShouldHandleTooHigh(self):
        input = {'pressure': '1101'}
        with self.assertRaises(ValueError):
            adjust.extractPressure(input)
        self.assertEqual(input['error'], 'pressure is invalid')

    # 450 extractNaturalHorizon
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:     sighting, a dictionary containing 'horizon', which should be a string
    #                   containing (case-insensitive) 'natural' or 'artificial'
    #       outputs:    True iff 'horizon' is non-existent or natural, False if otherwise and no error.
    #                   otherwise, sets the error field of the dictionary and raises value error.
    #   Happy Path:
    #       Nominal Value         'natural'    -> true
    #                             'artificial' -> false
    #       Mixed Case            'nAtUrAL'    -> true
    #                             'ARTIFICIAL' -> false
    #       Default Value          NONE        -> true
    #   Sad Path
    #       Non - String Value     1000    -> 'error': 'horizon is invalid', ValueError()
    #       Invalid String         'natur'    -> 'error': 'horizon is invalid', ValueError()
    # Happy Path
    def test450_010_ShouldHandleNominalTrue(self):
        actual = adjust.extractNaturalHorizon({'horizon': 'natural'})
        self.assertTrue(actual)

    def test450_020_ShouldHandleNominalFalse(self):
        actual = adjust.extractNaturalHorizon({'horizon': 'artificial'})
        self.assertFalse(actual)

    def test450_030_ShouldHandleMixedTrue(self):
        actual = adjust.extractNaturalHorizon({'horizon': 'NaTuRaL'})
        self.assertTrue(actual)

    def test450_040_ShouldHandleMixedFalse(self):
        actual = adjust.extractNaturalHorizon({'horizon': 'ARTIFICIAL'})
        self.assertFalse(actual)

    def test450_050_ShouldHandleDefault(self):
        actual = adjust.extractNaturalHorizon({})
        self.assertTrue(actual)

    def test450_910_ShouldHandleNonString(self):
        input = {'horizon': 1}
        with self.assertRaises(ValueError):
            adjust.extractNaturalHorizon(input)
        self.assertEqual(input['error'], 'horizon is invalid')

    def test450_920_ShouldHandleInvalidString(self):
        input = {'horizon': 'natur'}
        with self.assertRaises(ValueError):
            adjust.extractNaturalHorizon(input)
        self.assertEqual(input['error'], 'horizon is invalid')

    # 460 calculateAltitude
    #   Desired level of confidence:    boundary value analysis
    #   Input-output Analysis:
    #       inputs:         observation: validated float
    #                       height:      validated float
    #                       temperature: validated integer
    #                       pressure:    validated integer
    #                       naturalHorizon: validated boolean
    #      outputs:         The appropriate altitude
    #   Happy Path:
    #       Nominal Values
    #           (30.025, 19.0, 85, 1000, false) -> 29.998333...
    #           (45.25333, 6.0, 71, 1010, true) -> 45.198333...
    #           (42.0, 0.0, 72, 1010, true)     -> 41.98333....
    #   Sad Path
    #       None
    # Happy Path
    def test460_010_ShouldCalculateNominal1(self):
        actual = adjust.calculateAltitude(30.025, 19.0, 85, 1000, False)
        self.assertEqual(softwareprocess.operations.util.degreesToDegreeString(actual), softwareprocess.operations.util.degreesToDegreeString(29.998333))

    def test460_020_ShouldCalculateNominal2(self):
        actual = adjust.calculateAltitude(45.25333, 6.0, 71, 1010, True)
        self.assertEqual(softwareprocess.operations.util.degreesToDegreeString(actual), softwareprocess.operations.util.degreesToDegreeString(45.198333))

    def test460_030_ShouldCalculateNominal3(self):
        actual = adjust.calculateAltitude(42.0, 0.0, 72, 1010, False)
        self.assertEqual(softwareprocess.operations.util.degreesToDegreeString(actual), softwareprocess.operations.util.degreesToDegreeString(41.983333))


    # 400 adjust
    #   Desired level of confidence: boundary value analysis
    #   Input-output Analysis:
    #       inputs:     observation: unvalidated, should be degree/Minute string, Mandatory.
    #                   height:      unvalidated, should be float string, Optional
    #                   temperature: unvalidated, should be float string, Optional
    #                   pressure:    unvalidated, should be integer string, Optional
    #                   horizon:     unvalidated, string, either 'natural', or 'artificial', Optional
    #                   op: validated, string ('adjust')
    #   Happy Path
    #       Nominal Values
    #           Test 1
    #                   observation: '30d1.5'
    #                   height: '19.0'
    #                   pressure: '1000'
    #                   horizon:  'artificial'
    #                   op: 'adjust'
    #                   temperature: '85'
    #           Expected altitude: '29d59.9'
    #           Test 2
    #                   observation: '45d15.2'
    #                   height: '6'
    #                   pressure: '1010'
    #                   horizon 'natural'
    #                   temperature: '71'
    #                   op 'adjust'
    #                   extra: 'ignore me'
    #           Expected altitude: '45d11.9'
    #           Test 3
    #                   observation: '42d0.0'
    #                   op: 'adjust'
    #           Expected altitude: '41d59.0'
    #
    #   Sad Path
    #           Altitude given
    #           {'altitude': '0.1'} => {'error': 'altitude cannot be given in input'}
    #           Invalid observation
    #           {'observation': '0d0.0'} => {'error': 'operation is invalid'}
    #           Invalid height
    #           {'height' : '-10.0'} => {'error': 'height is invalid'}
    #           Invalid pressure
    #           {'pressure' : '99'} => {'error': 'pressure is invalid'}
    #           Invalid temperature
    #           {'temperature': '121'} => {'error' : 'temperature is invalid'}
    #           Invalid  horizon
    #           {'horizon': 'natura') => {'error' : 'horizon is invalid'}
    def test400_010_ShouldAdjustNominal(self):
        input = {
            'observation': '30d1.5',
            'height': '19.0',
            'pressure': '1000',
            'horizon':  'artificial',
            'op': 'adjust',
            'temperature': '85'
        }
        expected = copy.deepcopy(input)
        expected['altitude'] = '29d59.9'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_020_ShouldAdjustNominalHandleExtraKey(self):
        input = {
            'observation': '45d15.2',
            'height': '6',
            'pressure': '1010',
            'horizon':  'natural',
            'op': 'adjust',
            'temperature': '71',
            'extra': 'ignoreme'
        }
        expected = copy.deepcopy(input)
        expected['altitude'] = '45d11.9'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_030_ShouldAdjustNominalDefaultValues(self):
        input = {
            'observation': '42d0.0',
            'op': 'adjust'
        }
        expected = copy.deepcopy(input)
        expected['altitude'] = '41d59.0'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    # Sad Paths

    def test400_910_ShouldHandleInvalidObservation(self):
        input = {
            'op': 'adjust',
            'observation': '0d0.0'
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'observation is invalid'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_920_ShouldHandleInvalidHeight(self):
        input = {
            'op': 'adjust',
            'observation': '45d11.2',
            'height': '-10.0'
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'height is invalid'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_930_ShouldHandleInvalidPressure(self):
        input = {
            'op': 'adjust',
            'observation': '45d11.2',
            'pressure': '99'
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'pressure is invalid'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_940_ShouldHandleInvalidTemperature(self):
        input = {
            'op': 'adjust',
            'observation': '45d11.2',
            'temperature': '121'
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'temperature is invalid'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_950_ShouldHandleInvalidHorizon(self):
        input = {
            'op': 'adjust',
            'observation': '45d11.2',
            'horizon': 'natura'
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'horizon is invalid'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    def test400_960_ShouldHandleAltitudeGivenInInput(self):
        input = {
            'op': 'adjust',
            'observation': '45d11.2',
            'altitude': '5d11.2',
        }
        expected = copy.deepcopy(input)
        expected['error'] = 'altitude cannot be given in input'
        actual = adjust.adjust(input)
        self.assertEqual(actual, expected)

    # Acceptance tests
    def test500_010_ShouldDispatchToAdjust(self):
        input = {
            'observation': '42d0.0',
            'op': 'adjust'
        }
        expected = copy.deepcopy(input)
        expected['altitude'] = '41d59.0'
        actual = dispatch.dispatch(input)
        self.assertEqual(actual, expected)

    # def test500_020_ShouldDispatchToCorrect(self):
    #     input = {
    #         'op': 'correct'
    #     }
    #     expected = copy.deepcopy(input)
    #     actual = dispatch.dispatch(input)
    #     self.assertEqual(actual, expected)

    def test500_030_ShouldDispatchToLocate(self):
        input = {
            'op': 'locate'
        }
        expected = copy.deepcopy(input)
        actual = dispatch.dispatch(input)
        self.assertEqual(actual, expected)

    def test500_040_ShouldDispatchToPredict(self):
        test_input = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'}
        expected = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42',
                    'long':'75d53.6', 'lat':'7d24.3'}
        actual = dispatch.dispatch(test_input)
        self.assertEqual(actual, expected)

    # Sad Paths
    def test500_010_ShouldHandleNoInput(self):
        expected = {'error': 'parameter is missing'}
        self.assertEqual(dispatch.dispatch(), expected)

    def test500_020_ShouldHandleNonDictInput(self):
        expected = {'error': 'parameter is not a dictionary'}
        self.assertEqual(dispatch.dispatch(1), expected)

    def test500_030_ShouldHandleNoOp(self):
        expected = {'error': 'no op  is specified'}
        self.assertEqual(dispatch.dispatch({}), expected)

    def test500_040_ShouldHandleInvalidOp(self):
        input = {'op': 'not a real op'}
        expected = {'op': 'not a real op', 'error': 'op is not a legal operation'}
        self.assertEqual(dispatch.dispatch(input), expected)
