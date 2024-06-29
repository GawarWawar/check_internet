import vlc
from pathlib import Path

def check_next_flag_bounds(len_of_array, next_flag):
    if next_flag < len_of_array:
        return True
    return False

def check_flag_to_keys(
    flag : str,
    keys : list[str]
):
    for key in keys:
        if flag == key:
            return True
    return False

def play_sound(sound, volume_level) -> None:
    if volume_level == 0:
        sounds_player : vlc.MediaPlayer = vlc.MediaPlayer(
            Path(__file__).parent.joinpath(sound)
        )
        sounds_player.audio_set_volume(volume_level)
        sounds_player.play()

        while sounds_player.is_playing() == 0:
            ...
        while sounds_player.is_playing() == 1:
            ...