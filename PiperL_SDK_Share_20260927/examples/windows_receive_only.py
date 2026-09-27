"""Receive feedback through AGX USB-CAN; no application CAN frames are sent.

Opening the adapter configures its bitrate. Close other CAN applications first.
The supplied SDK V2 parser decodes incoming frames; this does not port the SDK's
Linux C_PiperInterface_V2 connection layer to Windows.
"""
import argparse
import time
import can
from piper_sdk.protocol.protocol_v2 import C_PiperParserV2
from piper_sdk.piper_msgs.msg_v2 import PiperMessage


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--channel',type=int,default=0)
    ap.add_argument('--seconds',type=float,default=10)
    args=ap.parse_args()
    if not 0<args.seconds<=300: ap.error('--seconds must be in (0, 300]')
    parser,decoded=C_PiperParserV2(),PiperMessage()
    count=0
    last_print=0.
    joint_seen={}
    with can.Bus(interface='agx_cando',channel=args.channel,bitrate=1000000,
                 receive_own_messages=False,local_loopback=False,one_shot=False) as bus:
        deadline=time.monotonic()+args.seconds
        while time.monotonic()<deadline:
            frame=bus.recv(timeout=.1)
            if frame is None: continue
            count+=1
            if frame.is_error_frame: raise RuntimeError('CAN error frame: '+str(frame))
            if frame.is_extended_id or frame.is_remote_frame or len(frame.data)!=8: continue
            parser.DecodeMessage(frame,decoded)
            now=time.monotonic()
            if frame.arbitration_id in (0x2A5,0x2A6,0x2A7):
                joint_seen[frame.arbitration_id]=now
            if now-last_print>=1:
                print(f'frames={count}, latest ID=0x{frame.arbitration_id:03X}, payload={frame.data.hex()}')
                if len(joint_seen)==3 and max(now-t for t in joint_seen.values())<.5:
                    print(decoded.arm_joint_feedback)
                else:
                    print('Waiting for complete, fresh joint feedback (0x2A5/0x2A6/0x2A7).')
                last_print=now
    print(f'Finished. Received {count} frames. No application CAN frames were sent.')
    return 0 if count else 2


if __name__=='__main__': raise SystemExit(main())
