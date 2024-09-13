from lyricsgenius import Genius
from lyricsgenius.utils import clean_str


class GeniusPatched(Genius):
    def _get_item_from_search_response(
        self, response, search_term, type_, result_type, artist=""
    ):
        """Gets the desired item from the search results.

        This method tries to match the `hits` of the :obj:`response` to
        the :obj:`response_term`, and if it finds no match, returns the first
        appropriate hit if there are any.

        Args:
            response (:obj:`dict`): A response from
                :meth:‍‍‍‍`Genius.search_all` to go through.
            search_term (:obj:`str`): The search term to match with the hit.
            type_ (:obj:`str`): Type of the hit we're looking for (e.g. song, artist).
            result_type (:obj:`str`): The part of the hit we want to match
                (e.g. song title, artist's name).
            artist (:obj:`str`): The name of the artist.

        Returns:
            :obj:‍‍`str` \\|‌ :obj:`None`:
            - `None` if there is no hit in the :obj:`response`.
            - The matched result if matching succeeds.
            - The first hit if the matching fails.

        """

        # Convert list to dictionary
        top_hits = response["sections"][0]["hits"]

        # Check rest of results if top hit wasn't the search type
        sections = sorted(response["sections"], key=lambda sect: sect["type"] == type_)

        hits = [
            hit for hit in top_hits if hit["type"] == type_ and hit["index"] == type_
        ]
        hits.extend(
            [
                hit
                for section in sections
                for hit in section["hits"]
                if hit["type"] == type_ and hit["index"] == type_
            ]
        )

        for hit in hits:
            item = hit["result"]
            if clean_str(item[result_type]) == clean_str(search_term):
                return item

        # If the desired type is song lyrics and none of the results matched,
        # return the first result that has lyrics
        if type_ == "song" and self.skip_non_songs:
            for hit in hits:
                song = hit["result"]
                if self._result_is_lyrics(song):
                    # if artist was supplied, compare with song artist.
                    if len(artist):
                        print(
                            clean_str(song["artist_names"]), " vs ", clean_str(artist)
                        )
                        if clean_str(song["artist_names"]) == clean_str(
                            artist
                        ) or clean_str(song["artist_names"]).startswith(
                            clean_str(artist)
                        ):
                            print(
                                "match: ",
                                clean_str(song["artist_names"]),
                                " == ",
                                clean_str(artist),
                            )
                            return song
                        else:
                            continue
                    return song

        # return hits[0]['result'] if hits else None
        # No attempts above worked to find a song match
        return None
