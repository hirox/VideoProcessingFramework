import PyNvCodec as nvc
import numpy as np


def test_issue_455():
    gpuID = 0

    nvEnc = nvc.PyNvEncoder({'bitrate': '30K', 'fps': '10', 'codec': 'hevc', 's': '256x256'}, gpuID)
    nvDec = nvc.PyNvDecoder(256, 256, nvc.PixelFormat.NV12, nvc.CudaVideoCodec.HEVC, gpuID)

    rawFrame = np.random.randint(0, 255, size=(256, 256, 3), dtype=np.uint8)

    print('Raw frame size is ' + str(rawFrame.size) + ' bytes.')

    encodedFrame = np.ndarray(shape=(0), dtype=np.uint8)

    count, success = 0, False

    while success is not True and count < 10:
        success = nvEnc.EncodeSingleFrame(rawFrame, encodedFrame, sync=False)
        count += 1

    print('Encoded frame size is ' + str(encodedFrame.size) + ' bytes.')

    exception_raised = False
    try:
        success = nvDec.DecodeSingleFrame(encodedFrame)
    except Exception as ex:
        exception_raised = True
        assert ("Tried to call DecodeSurface on a Decoder that has been initialized without a demuxer. "
                "Please use DecodeSurfaceFromPacket instead or intialized the decoder with demuxer when decoding "
                "from a file" == str(ex))
    assert exception_raised

    decodedFrame = np.ndarray(shape=(0), dtype=np.uint8)
    success = nvDec.DecodeFrameFromPacket(decodedFrame, encodedFrame)
