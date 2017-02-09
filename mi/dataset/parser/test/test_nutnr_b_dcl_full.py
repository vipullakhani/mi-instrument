#!/usr/bin/env python

"""
@package mi.dataset.parser.test.test_nutnr_b_dcl_full
@file mi/dataset/parser/test/test_nutnr_b_dcl_full.py
@author Mark Worden
@brief Test code for a nutnr_b_dcl_full data parser
"""

import os

from nose.plugins.attrib import attr

from mi.core.log import get_logger
from mi.dataset.dataset_parser import DataSetDriverConfigKeys
from mi.dataset.driver.nutnr_b.dcl_full.resource import RESOURCE_PATH
from mi.dataset.parser.nutnr_b_dcl_full import NutnrBDclFullRecoveredParser, \
    NutnrBDclFullTelemeteredParser
from mi.dataset.parser.nutnr_b_particles import \
    NutnrBDclFullRecoveredInstrumentDataParticle, \
    NutnrBDclDarkFullRecoveredInstrumentDataParticle, \
    NutnrBDclFullTelemeteredInstrumentDataParticle, \
    NutnrBDclDarkFullTelemeteredInstrumentDataParticle, \
    NutnrBDclFullRecoveredMetadataDataParticle,  \
    NutnrBDclFullTelemeteredMetadataDataParticle
from mi.dataset.test.test_parser import ParserUnitTestCase

log = get_logger()


MODULE_NAME = 'mi.dataset.parser.nutnr_b_particles'

NO_PARTICLES_FILE = '20010101.nutnr_b_dcl_full.log'
HAPPY_PATH_FILE_1 = '20130424.nutnr_b_dcl_full.log'
HAPPY_PATH_FILE_2 = '20031129.nutnr_b_dcl_full.log'
FILE_INVALID_FRAME_TYPE = '19990401.nutnr_b_dcl_full.log'
FILE_MISSING_METADATA = '19980401.nutnr_b_dcl_full.log'
FILE_INVALID_FIELDS = '19970401.nutnr_b_dcl_full.log'
SECOND_BLOCK_IN_DATA_BLOCK_FILE = '20040901.nutnr_b_dcl_full.log'

NO_PARTICLES_EXPECTED_PARTICLES = 0
HAPPY_PATH_EXPECTED_PARTICLES_1 = 26
HAPPY_PATH_EXPECTED_PARTICLES_2 = 42

EXPECTED_PARTICLES_INVALID_FRAME_TYPE = 3
EXPECTED_EXCEPTIONS_INVALID_FRAME_TYPE = 4
EXPECTED_PARTICLES_MISSING_METADATA = 4
EXPECTED_EXCEPTIONS_MISSING_METADATA = 3
EXPECTED_PARTICLES_INVALID_FIELDS = 2
EXPECTED_EXCEPTIONS_INVALID_FIELDS = 100
EXPECTED_PARTICLES_SECOND_BLOCK_IN_DATA_BLOCK = 4
EXPECTED_EXCEPTIONS_SECOND_BLOCK_IN_DATA_BLOCK = 0

HAPPY_PATH_REC_YML_1 = 'rec_20130424.nutnr_b_dcl_full.yml'
HAPPY_PATH_REC_YML_2 = 'rec_20031129.nutnr_b_dcl_full.yml'
HAPPY_PATH_TEL_YML_1 = 'tel_20130424.nutnr_b_dcl_full.yml'
HAPPY_PATH_TEL_YML_2 = 'tel_20031129.nutnr_b_dcl_full.yml'

REC_YML_INVALID_FRAME_TYPES = 'rec_19990401.nutnr_b_dcl_full.yml'
TEL_YML_INVALID_FRAME_TYPES = 'tel_19990401.nutnr_b_dcl_full.yml'
REC_YML_INVALID_FIELDS = 'rec_19970401.nutnr_b_dcl_full.yml'
TEL_YML_INVALID_FIELDS = 'tel_19970401.nutnr_b_dcl_full.yml'

HAPPY_PATH_TABLE = [
    (HAPPY_PATH_FILE_1, HAPPY_PATH_EXPECTED_PARTICLES_1, HAPPY_PATH_REC_YML_1, HAPPY_PATH_TEL_YML_1),
    (HAPPY_PATH_FILE_2, HAPPY_PATH_EXPECTED_PARTICLES_2, HAPPY_PATH_REC_YML_2, HAPPY_PATH_TEL_YML_2),
]


@attr('UNIT', group='mi')
class NutnrBDclFullParserUnitTestCase(ParserUnitTestCase):
    """
    nutnr_b_dcl_full Parser unit test suite
    """

    def create_rec_parser(self, file_handle, new_state=None):
        """
        This function creates a NutnrBDclfull parser for recovered data.
        """
        return NutnrBDclFullRecoveredParser(
            self.rec_config,
            file_handle, lambda state, ingested: None,
            lambda data: None, self.rec_exception_callback)

    def create_tel_parser(self, file_handle, new_state=None):
        """
        This function creates a NutnrBDclfull parser for telemetered data.
        """
        return NutnrBDclFullTelemeteredParser(
            self.tel_config,
            file_handle, lambda state, ingested: None,
            lambda data: None, self.tel_exception_callback)

    def open_file(self, filename):
        return open(os.path.join(RESOURCE_PATH, filename), mode='r')

    def rec_state_callback(self, state, file_ingested):
        """ Call back method to watch what comes in via the position callback """
        self.rec_state_callback_value = state
        self.rec_file_ingested_value = file_ingested

    def tel_state_callback(self, state, file_ingested):
        """ Call back method to watch what comes in via the position callback """
        self.tel_state_callback_value = state
        self.tel_file_ingested_value = file_ingested

    def rec_pub_callback(self, pub):
        """ Call back method to watch what comes in via the publish callback """
        self.rec_publish_callback_value = pub

    def tel_pub_callback(self, pub):
        """ Call back method to watch what comes in via the publish callback """
        self.tel_publish_callback_value = pub

    def rec_exception_callback(self, exception):
        """ Call back method to watch what comes in via the exception callback """
        self.rec_exception_callback_value = exception
        self.rec_exceptions_detected += 1

    def tel_exception_callback(self, exception):
        """ Call back method to watch what comes in via the exception callback """
        self.tel_exception_callback_value = exception
        self.tel_exceptions_detected += 1

    def setUp(self):
        ParserUnitTestCase.setUp(self)

        self.rec_config = {
            DataSetDriverConfigKeys.PARTICLE_MODULE: MODULE_NAME,
            DataSetDriverConfigKeys.PARTICLE_CLASS: None
        }

        self.tel_config = {
            DataSetDriverConfigKeys.PARTICLE_MODULE: MODULE_NAME,
            DataSetDriverConfigKeys.PARTICLE_CLASS: None
        }

        self.rec_state_callback_value = None
        self.rec_file_ingested_value = False
        self.rec_publish_callback_value = None
        self.rec_exception_callback_value = None
        self.rec_exceptions_detected = 0

        self.tel_state_callback_value = None
        self.tel_file_ingested_value = False
        self.tel_publish_callback_value = None
        self.tel_exception_callback_value = None
        self.tel_exceptions_detected = 0

        self.maxDiff = None

    def test_happy_path(self):
        """
        Read files and verify that all expected particles can be read.
        Verify that the contents of the particles are correct.
        """
        log.debug('===== START TEST HAPPY PATH =====')

        for input_file, expected_particles, rec_yml_file, tel_yml_file in HAPPY_PATH_TABLE:

            in_file = self.open_file(input_file)
            parser = self.create_rec_parser(in_file)
            particles = parser.get_records(expected_particles)
            self.assert_particles(particles, rec_yml_file, RESOURCE_PATH)
            self.assertEqual(self.rec_exceptions_detected, 0)
            in_file.close()

            in_file = self.open_file(input_file)
            parser = self.create_tel_parser(in_file)
            particles = parser.get_records(expected_particles)
            self.assert_particles(particles, tel_yml_file, RESOURCE_PATH)
            self.assertEqual(self.tel_exceptions_detected, 0)
            in_file.close()

        log.debug('===== END TEST HAPPY PATH =====')

    def test_invalid_fields(self):
        """
        The file used in this test has errors in every instrument record
        except the first NDF record.
        This results in 1 metadata particle and 1 instrument particle.
        """
        log.debug('===== START TEST INVALID FIELDS =====')

        input_file = FILE_INVALID_FIELDS
        expected_particles = EXPECTED_PARTICLES_INVALID_FIELDS
        expected_exceptions = EXPECTED_EXCEPTIONS_INVALID_FIELDS
        total_records = expected_particles + expected_exceptions

        in_file = self.open_file(input_file)
        parser = self.create_rec_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assert_particles(particles, REC_YML_INVALID_FIELDS, RESOURCE_PATH)
        self.assertEqual(self.rec_exceptions_detected, expected_exceptions)
        in_file.close()

        in_file = self.open_file(input_file)
        parser = self.create_tel_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assert_particles(particles, TEL_YML_INVALID_FIELDS, RESOURCE_PATH)
        self.assertEqual(self.tel_exceptions_detected, expected_exceptions)
        in_file.close()

        log.debug('===== END TEST INVALID FIELDS =====')

    def test_invalid_frame_type(self):
        """
        The file used in this test has an valid frame type instead
        of the NDF (dark) type and 1 other invalid frame type.
        This results in no metadata,
        instrument particles for the other valid instrument types,
        plus 2 Recoverable exceptions.
        """
        log.debug('===== START TEST INVALID FRAME TYPE =====')

        input_file = FILE_INVALID_FRAME_TYPE
        expected_particles = EXPECTED_PARTICLES_INVALID_FRAME_TYPE
        expected_exceptions = EXPECTED_EXCEPTIONS_INVALID_FRAME_TYPE
        total_records = expected_particles + expected_exceptions

        in_file = self.open_file(input_file)
        parser = self.create_rec_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.rec_exceptions_detected, expected_exceptions)
        in_file.close()

        in_file = self.open_file(input_file)
        parser = self.create_tel_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.tel_exceptions_detected, expected_exceptions)
        in_file.close()

        log.debug('===== END TEST INVALID FRAME TYPE =====')

    def test_missing_metadata(self):
        """
        The file used in this test is missing one of the required
        metadata records.
        This causes no metadata particles to be generated.
        """
        log.debug('===== START TEST MISSING METADATA =====')

        input_file = FILE_MISSING_METADATA
        expected_particles = EXPECTED_PARTICLES_MISSING_METADATA
        expected_exceptions = EXPECTED_EXCEPTIONS_MISSING_METADATA
        total_records = expected_particles + expected_exceptions

        in_file = self.open_file(input_file)
        parser = self.create_rec_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.rec_exceptions_detected, expected_exceptions)

        inst_particles = 0
        meta_particles = 0
        for particle in particles:
            if isinstance(particle, NutnrBDclFullRecoveredInstrumentDataParticle) or \
               isinstance(particle, NutnrBDclDarkFullRecoveredInstrumentDataParticle):

                inst_particles += 1
            elif isinstance(particle, NutnrBDclFullRecoveredMetadataDataParticle):
                meta_particles += 1

        self.assertEqual(inst_particles, expected_particles)
        self.assertEqual(meta_particles, 0)

        in_file.close()

        in_file = self.open_file(input_file)
        parser = self.create_tel_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.tel_exceptions_detected, expected_exceptions)

        inst_particles = 0
        meta_particles = 0
        for particle in particles:
            if isinstance(particle, NutnrBDclFullTelemeteredInstrumentDataParticle) or \
               isinstance(particle, NutnrBDclDarkFullTelemeteredInstrumentDataParticle):

                inst_particles += 1
            elif isinstance(particle, NutnrBDclFullTelemeteredMetadataDataParticle):
                meta_particles += 1

        self.assertEqual(inst_particles, expected_particles)
        self.assertEqual(meta_particles, 0)

        in_file.close()

        log.debug('===== END TEST MISSING METADATA =====')

    def test_second_nitrate_dark_in_data_block(self):
        """
        Verify that no particles are produced if the input file
        has no instrument records.
        """
        log.debug('===== START TEST SECOND DARK IN DATA BLOCK =====')

        input_file = SECOND_BLOCK_IN_DATA_BLOCK_FILE
        expected_particles = EXPECTED_PARTICLES_SECOND_BLOCK_IN_DATA_BLOCK
        expected_exceptions = EXPECTED_EXCEPTIONS_SECOND_BLOCK_IN_DATA_BLOCK
        total_records = expected_particles + 1

        in_file = self.open_file(input_file)
        parser = self.create_rec_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.rec_exceptions_detected, expected_exceptions)
        in_file.close()

        in_file = self.open_file(input_file)
        parser = self.create_tel_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.tel_exceptions_detected, expected_exceptions)
        in_file.close()

        log.debug('===== END TEST SECOND DARK IN DATA BLOCK =====')

    def test_no_particles(self):
        """
        Verify that no particles are produced if the input file
        has no instrument records.
        """
        log.debug('===== START TEST NO PARTICLES =====')

        input_file = NO_PARTICLES_FILE
        expected_particles = NO_PARTICLES_EXPECTED_PARTICLES
        total_records = expected_particles + 1

        in_file = self.open_file(input_file)
        parser = self.create_rec_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.rec_exceptions_detected, 0)
        in_file.close()

        in_file = self.open_file(input_file)
        parser = self.create_tel_parser(in_file)
        particles = parser.get_records(total_records)
        self.assertEqual(len(particles), expected_particles)
        self.assertEqual(self.tel_exceptions_detected, 0)
        in_file.close()

        log.debug('===== END TEST NO PARTICLES =====')