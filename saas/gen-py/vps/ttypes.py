#
# Autogenerated by Thrift Compiler (0.8.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class Vps:
  """
  Attributes:
   - id
   - ipv4
   - ipv4_netmask
   - ipv4_gateway
   - password
   - os
   - pc
   - ram
   - cpu
   - hd
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'id', None, None, ), # 1
    (2, TType.I32, 'ipv4', None, None, ), # 2
    (3, TType.I32, 'ipv4_netmask', None, None, ), # 3
    (4, TType.I32, 'ipv4_gateway', None, None, ), # 4
    (5, TType.STRING, 'password', None, None, ), # 5
    (6, TType.I32, 'os', None, None, ), # 6
    (7, TType.I32, 'pc', None, None, ), # 7
    (8, TType.I32, 'ram', None, None, ), # 8
    (9, TType.I16, 'cpu', None, None, ), # 9
    (10, TType.I16, 'hd', None, None, ), # 10
  )

  def __init__(self, id=None, ipv4=None, ipv4_netmask=None, ipv4_gateway=None, password=None, os=None, pc=None, ram=None, cpu=None, hd=None,):
    self.id = id
    self.ipv4 = ipv4
    self.ipv4_netmask = ipv4_netmask
    self.ipv4_gateway = ipv4_gateway
    self.password = password
    self.os = os
    self.pc = pc
    self.ram = ram
    self.cpu = cpu
    self.hd = hd

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.id = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.ipv4 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.ipv4_netmask = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I32:
          self.ipv4_gateway = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.password = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.I32:
          self.os = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.I32:
          self.pc = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.I32:
          self.ram = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.I16:
          self.cpu = iprot.readI16();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.I16:
          self.hd = iprot.readI16();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Vps')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.I32, 1)
      oprot.writeI32(self.id)
      oprot.writeFieldEnd()
    if self.ipv4 is not None:
      oprot.writeFieldBegin('ipv4', TType.I32, 2)
      oprot.writeI32(self.ipv4)
      oprot.writeFieldEnd()
    if self.ipv4_netmask is not None:
      oprot.writeFieldBegin('ipv4_netmask', TType.I32, 3)
      oprot.writeI32(self.ipv4_netmask)
      oprot.writeFieldEnd()
    if self.ipv4_gateway is not None:
      oprot.writeFieldBegin('ipv4_gateway', TType.I32, 4)
      oprot.writeI32(self.ipv4_gateway)
      oprot.writeFieldEnd()
    if self.password is not None:
      oprot.writeFieldBegin('password', TType.STRING, 5)
      oprot.writeString(self.password)
      oprot.writeFieldEnd()
    if self.os is not None:
      oprot.writeFieldBegin('os', TType.I32, 6)
      oprot.writeI32(self.os)
      oprot.writeFieldEnd()
    if self.pc is not None:
      oprot.writeFieldBegin('pc', TType.I32, 7)
      oprot.writeI32(self.pc)
      oprot.writeFieldEnd()
    if self.ram is not None:
      oprot.writeFieldBegin('ram', TType.I32, 8)
      oprot.writeI32(self.ram)
      oprot.writeFieldEnd()
    if self.cpu is not None:
      oprot.writeFieldBegin('cpu', TType.I16, 9)
      oprot.writeI16(self.cpu)
      oprot.writeFieldEnd()
    if self.hd is not None:
      oprot.writeFieldBegin('hd', TType.I16, 10)
      oprot.writeI16(self.hd)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
