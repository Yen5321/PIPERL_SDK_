"""Import and protocol test only. No adapter enumeration or robot connection."""
import importlib.metadata as metadata
from pathlib import Path
import struct
import can
import agx_cando
from piper_sdk.protocol.protocol_v2 import C_PiperParserV2
from piper_sdk.piper_msgs.msg_v2 import PiperMessage


def main():
    for name in ('piper_sdk','python-can','python-can-agx-cando','wrapt','packaging','typing_extensions'):
        print(name,metadata.version(name))
    entries=metadata.entry_points(group='can.interface')
    assert any(e.name=='agx_cando' for e in entries), 'AGX backend not registered'
    binaries=Path(agx_cando.__file__).parent/'bin'/'x64'
    for name in ('cando.dll','agx_receive.dll'):
        assert (binaries/name).is_file(), name+' is missing'
    parser=C_PiperParserV2()
    output=PiperMessage()
    frame=can.Message(arbitration_id=0x2A5,data=struct.pack('>ii',1000,-2000),is_extended_id=False)
    assert parser.DecodeMessage(frame,output)
    assert output.arm_joint_feedback.joint_1==1000
    assert output.arm_joint_feedback.joint_2==-2000
    print('PASS: imports, backend registration, DLL presence and SDK V2 decoding. No hardware opened.')


if __name__=='__main__': main()
