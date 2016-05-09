import netaddr
from ostinato.protocols import payload_pb2
from . import autogenerates
from . import baseclass
from .. import utils


class Mac(autogenerates._Mac):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
        """
        Source MAC address
        """
        return str(netaddr.EUI(self._src_mac))

    @source.setter
    def source(self, value):
        self._src_mac = netaddr.EUI(value).value

    @property
    def destination(self):
        """
        destination MAC address
        """
        return str(netaddr.EUI(self._dst_mac))

    @destination.setter
    def destination(self, value):
        self._dst_mac = netaddr.EUI(value).value


class IPv4(autogenerates._IPv4):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
        return str(netaddr.IPAddress(self._src_ip))

    @source.setter
    def source(self, value):
        self._src_ip = netaddr.IPAddress(value).value

    @property
    def destination(self):
        return str(netaddr.IPAddress(self._dst_ip))

    @destination.setter
    def destination(self, value):
        self._dst_ip = netaddr.IPAddress(value).value


class Payload(baseclass.Protocol):

    __metaclass__ = baseclass.make_protocol_class

    _protocol_id = 101
    _extension = payload_pb2.payload

    def __init__(self, pattern='00 00 00 00', mode='FIXED_WORD', **kwargs):
        super(Payload, self).__init__(pattern=pattern, mode=mode, **kwargs)
        self.mode = mode
        self.pattern = pattern

    class _Mode(utils.Enum):
        DECREMENT_BYTE = payload_pb2.Payload.e_dp_dec_byte
        FIXED_WORD = payload_pb2.Payload.e_dp_fixed_word
        INCREMENT_BYTE = payload_pb2.Payload.e_dp_inc_byte
        RANDOM = payload_pb2.Payload.e_dp_random

    @property
    def mode(self):
        """
        The mode can be one of:
        - ``DECREMENT_BYTE``
        - ``FIXED_WORD``
        - ``INCREMENT_BYTE``
        - ``RANDOM``
        """
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)

    @property
    def pattern(self):
        """
        Payload initial word. Depending on the chosen mode, this word will be
        repeated unchanged, incremented/decremented, or randomized
        """
        return utils.to_str(self._pattern)

    @pattern.setter
    def pattern(self, value):
        self._pattern = utils.parse(value)

    def from_dict(self, values):
        for key, value in values.iteritems():
            setattr(self, key, value)

    def to_dict(self):
        return {'pattern': self.pattern,
                'mode': self.mode}

    def _save_pattern(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.pattern = self._pattern

    def _fetch_pattern(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self._pattern = ext.pattern

    def _save_mode(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.pattern_mode = self._mode

    def _fetch_mode(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self._mode = ext.pattern_mode


class Ethernet(autogenerates._Ethernet):

    __metaclass__ = baseclass.make_protocol_class


class Udp(autogenerates._Udp):

    __metaclass__ = baseclass.make_protocol_class


class Tcp(autogenerates._Tcp):

    __metaclass__ = baseclass.make_protocol_class
