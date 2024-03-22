#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.WARNING)
formatter = logging.Formatter('[%(levelname)s]\t %(message)s')
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

default_general = {
	"version": "0.1",
	"name": "MIRACLEpy",
	"description": "Microsatellite Instability (MSI) detection with RNA sequencing data.",
	"author": "Jin-Wook et al.",
	"contact": "argon502@snu.ac.kr"
}

default_detection = {
		"custom_model": False
		}
