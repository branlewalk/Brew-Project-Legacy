import thermo_client
from mock import patch


@patch('thermo_client.read_temp_raw')
def test_read_thermo(mock_read_temp_raw):
    mock_read_temp_raw.return_value = [": crc=el YES\n", "t=25125\n"]
    assert thermo_client.read_thermo("") == 25.125


@patch('thermo_client.read_temp_raw')
def test_read_thermo_no(mock_read_temp_raw):
    mock_read_temp_raw.side_effect = [[": crc=el No\n", "t=25125\n"], [": crc=el YES\n", "t=25125\n"]]
    assert thermo_client.read_thermo("") == 25.125


