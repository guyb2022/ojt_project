# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START video_detect_faces_gcs]
import time
from google.cloud import videointelligence

gcs_uri = "gs://my_first_bucket_vac/videoplayback.mp4"
output_uri = "gs://result_ojt_after_api/output - {}.json".format(time.time())

video_client = videointelligence.VideoIntelligenceServiceClient.from_service_account_file("my_keys.json")


def run_all_functions(event, file_context):
    """Detects faces in a video."""
    features = [
    videointelligence.Feature.OBJECT_TRACKING,
    videointelligence.Feature.LABEL_DETECTION,
    videointelligence.Feature.SHOT_CHANGE_DETECTION,
    videointelligence.Feature.SPEECH_TRANSCRIPTION,
    videointelligence.Feature.LOGO_RECOGNITION,
    videointelligence.Feature.EXPLICIT_CONTENT_DETECTION,
    videointelligence.Feature.TEXT_DETECTION,
    videointelligence.Feature.FACE_DETECTION,
    videointelligence.Feature.PERSON_DETECTION
    ]
    
    transcript_config = videointelligence.SpeechTranscriptionConfig(
    language_code="en-US", enable_automatic_punctuation=True
    )

    person_config = videointelligence.PersonDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=False,
        include_pose_landmarks=True,
    )

    face_config = videointelligence.FaceDetectionConfig(
        include_bounding_boxes=True, include_attributes=True
    )

    video_context = videointelligence.VideoContext(
        speech_transcription_config=transcript_config,
        person_detection_config=person_config,
        face_detection_config=face_config)

    operation = video_client.annotate_video(
        request={"features": features,
                 "input_uri": gcs_uri,
                 "output_uri": output_uri,
                 "video_context": video_context}
    )

    print("\nProcessing video.", operation)

    result = operation.result(timeout=300)

    print("\n finnished processing.")
                
def trigger_from_cloud_storge(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    file_type = file["name"].split(".")[-1]
    # process the video file
    run_all_functions(file, context)               
