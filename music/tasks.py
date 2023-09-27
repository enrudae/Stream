import os
from pydub import AudioSegment
from datetime import timedelta

from celery import shared_task


@shared_task
def process_and_upload_track(track_id):
    from .models import Track
    track = Track.objects.get(id=track_id)
    file_name = os.path.basename(track.original_track.name)

    input_audio = AudioSegment.from_file(track.original_track.path)
    output_audio = input_audio.export(track.original_track.name, format="mp3", bitrate="128k")
    track.original_track.delete()
    track.duration = timedelta(seconds=len(input_audio) // 1000)
    track.track.save(file_name, output_audio)
    output_audio.close()


