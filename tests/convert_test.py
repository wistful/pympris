import os
import sys
import unittest
import dbus

sys.path.insert(0, os.path.abspath('..'))

from pympris.common import convert, convert2dbus

class ConvertTest(unittest.TestCase):

	def test_convert(self):
		"""test converting from dbus types to python types"""

		if sys.version_info[0] == 2:
			str_type = unicode
		else:
			str_type = str

		tests = ((dbus.Boolean(True), bool),
				(dbus.Byte(10), int),
				(dbus.Int16(10), int),
				(dbus.Int32(10), int),
				(dbus.Int64(10), int),
				(dbus.UInt16(10), int),
				(dbus.UInt32(10), int),
				(dbus.UInt64(10), int),
				(dbus.Double(10.01), float),
				(dbus.String('test'), str_type),
				(dbus.ObjectPath('/path/to/stuff'), str_type),
				(dbus.Signature('uu'), str_type),
				(dbus.Dictionary({1:1}), dict),
				(dbus.Struct((1,)), tuple))
		
		for test in tests:
			self.assertIsInstance(convert(test[0]), test[1])

	def test_convert2dbus(self):
		"""Test converting python types to dbus types"""

		if sys.version_info[0] == 2:
			dbus_str_type = dbus.UTF8String
		else:
			dbus_str_type = dbus.String

		tests = ((True, 'b', dbus.Boolean),
				(1, 'y', dbus.Byte),
				('1', 'n', dbus.Int16),
				(-1, 'i', dbus.Int32),
				(1, 'x', dbus.Int64),
				(1, 'q', dbus.UInt16),
				(True, 'u', dbus.UInt32),
				(1, 't', dbus.UInt64),
				(1.1, 'd', dbus.Double),
				('/path/to/stuff', 'o', dbus.ObjectPath),
				('(ii)', 'g', dbus.Signature),
				('test', 's', dbus_str_type))
				#((1,1), '(ii)', dbus.Struct),
				#({1:1}, '{ii}', dbus.Dictionary))

		for test in tests:
			self.assertIsInstance(convert2dbus(test[0], test[1]), test[2])

if __name__ == '__main__':
	unittest.main()

