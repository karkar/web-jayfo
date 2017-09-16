import operator
import invoke
import yaml


@invoke.task()
def report_nsf_collaborators():
    data_files = [
        'authors',
        'conferences',
        'conferencepapers',
        'journals',
        'journalpapers',
        'workshops',
        'workshoppapers'
    ]

    data_loaded = {}
    for data_current in data_files:
        with open('_data/{}.yml'.format(data_current)) as f:
            data_loaded[data_current] = yaml.load(f)

    # Join the year as a field each paper, except journalpapers already have this
    for (key, paper_current) in data_loaded['conferencepapers'].items():
        paper_current['year'] = data_loaded['conferences'][paper_current['conference']]['year']
    for (key, paper_current) in data_loaded['workshoppapers'].items():
        paper_current['year'] = data_loaded['workshops'][paper_current['workshop']]['year']

    # Join authors with the year of a collaboration
    collaborators_raw = []
    for (key, paper_current) in data_loaded['conferencepapers'].items():
        for author_current_key in paper_current['authors']:
            collaborators_raw.append(
                {
                    'author_key': author_current_key,
                    'year': paper_current['year']
                }
            )
    for (key, paper_current) in data_loaded['journalpapers'].items():
        for author_current_key in paper_current['authors']:
            collaborators_raw.append(
                {
                    'author_key': author_current_key,
                    'year': paper_current['year']
                }
            )
    for (key, paper_current) in data_loaded['workshoppapers'].items():
        for author_current_key in paper_current['authors']:
            collaborators_raw.append(
                {
                    'author_key': author_current_key,
                    'year': paper_current['year']
                }
            )

    # For each author we find, keep the most recent year
    collaborators = {}
    for collaborator_current in collaborators_raw:
        if collaborator_current['author_key'] in collaborators:
            collaborators[collaborator_current['author_key']]['year'] = max(
                collaborator_current['year'],
                collaborators[collaborator_current['author_key']]['year']
            )
        else:
            collaborators[collaborator_current['author_key']] = collaborator_current

    # Remove myself
    del collaborators['id_author_fogarty_james']

    # Apply a name field
    for key, collaborator_current in collaborators.items():
        author_current = data_loaded['authors'][collaborator_current['author_key']]

        collaborator_current['name'] = author_current['name'][0]
        collaborator_current['name'] += ','
        for name_current in author_current['name'][1:]:
            collaborator_current['name'] += ' ' + name_current

    # Sort the collaborators
    collaborators_sorted = sorted(
        collaborators.values(),
        key=operator.itemgetter('name')
    )
    collaborators_sorted = sorted(
        collaborators_sorted,
        key=operator.itemgetter('year'),
        reverse=True
    )

    # Output in a usable format
    with open('report_nsf_collaborators.txt', 'w') as f:
        for collaborator_current in collaborators_sorted:
            print(
                '{}\t{}'.format(
                    collaborator_current['name'],
                    collaborator_current['year']
                ),
                file=f
            )
