import pytest

from pathlib import Path

from spotdl.providers.provider_utils import _parse_duration
from spotdl.providers.provider_utils import _parse_path_template
from spotdl.search import SongObject


def test_parse_duration():
    """
    Test the duration parsing
    """

    assert _parse_duration("3:16") == float(196.0)  # 3 min song
    assert _parse_duration("20") == float(20.0)  # 20 second song
    assert _parse_duration("25:59") == float(1559.0)  # 26 min result
    assert _parse_duration("25:59:59") == float(93599.0)  # 26 hour result
    assert _parse_duration("likes") == float(0.0)  # bad values
    assert _parse_duration("views") == float(0.0)
    assert _parse_duration([1, 2, 3]) == float(0.0)  # type: ignore
    assert _parse_duration({"json": "data"}) == float(0.0)  # type: ignore


@pytest.mark.parametrize("path_template, expected_path", [
    ("{title}.{ext}", "test song.mp3"),
    ("{track_number}-{title}.{ext}", "03-test song.mp3"),
    ("{artist}/{album}/{title}.{ext}", "test_artist/test album/test song.mp3"),
])
def test_parse_path_template(path_template, expected_path):
    song_object = create_song_obj()
    assert _parse_path_template(path_template, song_object, output_format="mp3") == Path(expected_path)


def create_song_obj():
    artist_objs = [{"name": "test_artist"}]
    raw_track_meta = {
        "name": "test song",
        "album": {
            "name": "test album",
            "artists": artist_objs,
            "release_date": "2021",
            "images": [
                {"url": "https://i.ytimg.com/vi_webp/iqKdEhx-dD4/hqdefault.webp"}
            ],
        },
        "artists": artist_objs,
        "track_number": "3",
        "genres": ["test genre"],
    }

    raw_album_meta = {"genres": ["test genre"]}
    raw_artist_meta = {"genres": ["test artist genre"]}

    return SongObject(
        raw_track_meta,
        raw_album_meta,
        raw_artist_meta,
        "https://www.youtube.com/watch?v=Th_C95UMegc",
        "test lyrics",
        None,
    )
