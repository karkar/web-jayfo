import os.path
import PIL.Image
import unittest
import yaml


class TestConferencePapers(unittest.TestCase):
    def setUp(self) -> None:
        """
        Parse our data files and combine them into a dictionary.
        """
        data_files = [
            'authors',
            'conferencepapers',
            'conferences'
        ]

        self.data = {}
        for data_current in data_files:
            with open('_data/{}.yml'.format(data_current)) as f:
                self.data[data_current] = yaml.load(f)

    def test_parse_yaml(self) -> None:
        """
        Confirm all YAML from setUp successfully parses.
        """
        pass

    def test_conferencepapers_authors_exist(self) -> None:
        """
        Confirm all authors referenced by a paper actually exist.
        """
        for id_conferencepaper, conferencepaper in self.data['conferencepapers'].items():
            for id_author in conferencepaper['authors']:
                self.assertIn(
                    id_author,
                    self.data['authors'],
                    '{} references author {} not found in authors.yml'.format(id_conferencepaper, id_author)
                )

    def test_conferencepapers_conference_exist(self) -> None:
        """
        Confirm all conferences referenced by a paper actually exist.
        """
        for id_conferencepaper, conferencepaper in self.data['conferencepapers'].items():
            id_conference = conferencepaper['conference']
            self.assertIn(
                id_conference,
                self.data['conferences'],
                '{} references conference {} not found in conferences.yml'.format(id_conferencepaper, id_conference)
            )

    def test_conferencepapers_files_exist(self) -> None:
        """
        Confirm all files references by a paper actually exist.
        """
        for id_conferencepaper, conferencepaper in self.data['conferencepapers'].items():
            # Every paper must have a thumb of the right size
            self.assertIn(
                'localthumb',
                conferencepaper,
                '{} missing field localthumb'.format(id_conferencepaper)
            )
            file_path = conferencepaper['localthumb']
            self.assertTrue(
                os.path.isfile('publications/{}'.format(file_path)),
                '{} references localthumb {} not found in publications/'.format(id_conferencepaper, file_path)
            )

            file_name = os.path.basename(file_path)
            self.assertRegexpMatches(
                file_name,
                '^[a-z0-9\-\.]*$',
                '{} file name contains illegal characters'.format(id_conferencepaper)
            )

            image = PIL.Image.open('publications/{}'.format(file_path))
            self.assertEqual(
                image.size,
                (120, 120),
                '{} image thumb is not 120x120'.format(id_conferencepaper)
            )

            # Papers may have a PDF
            if 'localpdf' in conferencepaper:
                file_path = conferencepaper['localpdf']
                self.assertTrue(
                    os.path.isfile('publications/{}'.format(file_path)),
                    '{} references localpdf {} not found in publications/'.format(id_conferencepaper, file_path)
                )

                file_name = os.path.basename(file_path)
                self.assertRegexpMatches(
                    file_name,
                    '^[a-z0-9\-\.]*$',
                    '{} file name contains illegal characters'.format(id_conferencepaper)
                )


            # Papers may have a video
            if 'localvideo' in conferencepaper:
                file_path = conferencepaper['localvideo']
                self.assertTrue(
                    os.path.isfile('publications/{}'.format(file_path)),
                    '{} references localvideo {} not found in publications/'.format(id_conferencepaper, file_path)
                )

                file_name = os.path.basename(file_path)
                self.assertRegexpMatches(
                    file_name,
                    '^[a-z0-9\-\.]*$',
                    '{} file name contains illegal characters'.format(id_conferencepaper)
                )

