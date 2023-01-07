import io

from typing import Optional

import grpc
from google.protobuf import json_format

from . import PTSL_pb2_grpc
from . import PTSL_pb2 as p

PTSL_VERSION=1

class Client:
    stub: PTSL_pb2_grpc.PTSLStub
    session_id: str


    def __init__(self, api_key_path, address = 'localhost:31416') -> None:
        channel = grpc.insecure_channel(address)
        self.stub = PTSL_pb2_grpc.PTSLStub(channel) 
        self.session_id = ""
        self.check_if_ready()
        self.authorize_connection(api_key_path)


    def _send_sync_request(self, command_id, request_body, task_id="") -> p.Response:

        if request_body is not None:
            request_body_json = json_format.MessageToJson(request_body, preserving_proto_field_name=True)
        else:
            request_body_json = "" 

        request = p.Request(
            header=p.RequestHeader(
                task_id=task_id,
                session_id=self.session_id,
                command=command_id,
                version=PTSL_VERSION
            ),
            request_body_json=request_body_json
        )

        response = self.stub.SendGrpcRequest(request)

        return response

    # This works
    def get_session_sample_rate(self) -> p.SampleRate:
        response = self._send_sync_request(p.CommandId.GetSessionSampleRate, None)

        if response.header.status == p.Failed:
            print("Failed:")
            print(response)
        else:
            body = json_format.Parse(response.response_body_json, p.GetSessionSampleRateResponseBody(), 
                ignore_unknown_fields=True)
            return body.sample_rate

    # This works
    def get_session_audio_format(self) -> p.FileType:
        response = self._send_sync_request(p.GetSessionAudioFormat, None)

        if response.header.status == p.Failed:
            print("Failed:")
            print(response)
        else:
            body = json_format.Parse(response.response_body_json, p.GetSessionAudioFormatResponseBody())
            return body.current_setting

    # This does not work 
    # Here is the error I get: https://gist.github.com/iluvcapra/fb8e2480070b0a9891076d39ed95d605
    def create_session(self, name, session_location, 
        file_type : p.FileType = p.FT_WAVE, 
        sample_rate: p.SampleRate = p.SR_48000, 
        io_settings: p.IOSettings = p.IO_Last,
        is_interleaved = True,
        is_cloud_project = False,
        bit_depth: p.BitDepth = p.Bit24
        ):

        req_body = p.CreateSessionRequestBody(session_name=name,file_type=file_type, sample_rate=sample_rate,
            input_output_settings=io_settings, is_interleaved=is_interleaved, 
            session_location=session_location, bit_depth=bit_depth, is_cloud_project=is_cloud_project)

        response = self._send_sync_request(p.CreateSession, req_body)

        if response.header.status == p.Failed:
            print("Failed:")
            print(response)

    # This fails if there are zero tracks, the JSON returned from Pro Tools in the response
    # body has a strange format
    #
    # Here is the error I get: https://gist.github.com/iluvcapra/90601ade487b245510e08b9c68650925
    def get_track_list(self):
        req_body = p.GetTrackListRequestBody(page_limit=24, 
            track_filter_list=[p.TrackListInvertibleFilter(filter=p.All, is_inverted=False)], 
            is_filter_list_additive=False)

        response = self._send_sync_request(p.GetTrackList, req_body)

        if response.header.status == p.Failed:
            print("Failed:")
            print(response)
        else:
            resp_body = json_format.Parse(response.response_body_json, p.GetTrackListResponseBody())
            return resp_body.track_list

    # This works
    def check_if_ready(self):
        response = self._send_sync_request(p.CommandId.HostReadyCheck, None)

        if response.header.status == p.Failed:
            print("Pro Tools Not Ready")
            print(response)
        else:
            print("Pro Tools Ready")

    # This works
    def authorize_connection(self, api_key_path) -> Optional[str]:
        with io.FileIO(api_key_path) as f:
            api_token = f.readall().decode(encoding='ascii')

        response = self._send_sync_request(p.CommandId.AuthorizeConnection, p.AuthorizeConnectionRequestBody(auth_string=api_token))

        if response.header.status == p.Failed:
            print("An error occurred")
            print(response)
        else:
            authorization_response = json_format.Parse(response.response_body_json, p.AuthorizeConnectionResponseBody)
            if authorization_response.is_authorized:
                print("Connection authorized successfully, message:" + authorization_response.message)
                self.session_id = authorization_response.session_id
            else:
                print("Connection did not authorize, message: " + authorization_response.message)
