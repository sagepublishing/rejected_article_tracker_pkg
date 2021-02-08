class FakeOAIPMHData:
    fake_xml_record = """<?xml version="1.0"?>
                    <arXiv xsi:schemaLocation="http://arxiv.org/OAI/arXiv/ http://arxiv.org/OAI/arXiv.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://arxiv.org/OAI/arXiv/">
                    <id>0704.0025</id>
                    <created>2007-04-02</created>
                    <authors>
                    <author>
                    <keyname>Mishchenko</keyname>
                    <forenames>A. S.</forenames>
                    <affiliation>CREST, Japan Science and Technology Agency</affiliation>
                    <affiliation>Russian Research Centre ``Kurchatov Institute''</affiliation>
                    </author>
                    <author>
                    <keyname>Nagaosa</keyname>
                    <forenames>N.</forenames>
                    <affiliation>CREST, Japan Science and Technology Agency</affiliation>
                    <affiliation>The University of Tokyo</affiliation>
                    </author>
                    </authors>
                    <title>Spectroscopic Properties of Polarons in Strongly Correlated Systems byExact Diagrammatic Monte Carlo Method</title>
                    <categories>cond-mat.str-el cond-mat.stat-mech</categories>
                    <comments>41 pages, 13 figures, in "Polarons in Advanced Materials" ed. A. S.Alexandrov (Canopus/Springer Publishing, Bristol (2007)), pp. 503-544.</comments>
                    <doi>10.1007/978-1-4020-6348-0_12</doi>
                    <abstract> We present recent advances in understanding of the ground and excited states of the electron-phonon coupled systems obtained by novel methods of Diagrammatic Monte Carlo and Stochastic Optimization, which enable the approximation-free calculation of Matsubara Green function in imaginary times and perform unbiased analytic continuation to real frequencies. We present exact numeric results on the ground state properties, Lehmann spectral function and optical conductivity of different strongly correlated systems: Frohlich polaron, Rashba-Pekar exciton-polaron, pseudo Jahn-Teller polaron, exciton, and interacting with phonons hole in the t-J model. </abstract>
                    </arXiv>
                        """
    fake_json_record = {'@xsi:schemaLocation': 'http://arxiv.org/OAI/arXiv/ http://arxiv.org/OAI/arXiv.xsd',
                        '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                        '@xmlns': 'http://arxiv.org/OAI/arXiv/',
                        'id': '0704.0025',
                        'created': '2007-04-02',
                        'authors': {'author':[
                                        {'keyname': 'Mishchenko',
                                        'forenames': 'A. S.',
                                        'affiliation':['CREST, Japan Science and Technology Agency',
                                                    "Russian Research Centre ``Kurchatov Institute''"]},
                                        {'keyname': 'Nagaosa',
                                        'forenames': 'N.',
                                        'affiliation':['CREST, Japan Science and Technology Agency',
                                                    'The University of Tokyo']}]},
                        'title': 'Spectroscopic Properties of Polarons in Strongly Correlated Systems byExact Diagrammatic Monte Carlo Method',
                        'categories': 'cond-mat.str-el cond-mat.stat-mech',
                        'comments': '41 pages, 13 figures, in "Polarons in Advanced Materials" ed. A. S.Alexandrov (Canopus/Springer Publishing, Bristol (2007)), pp. 503-544.',
                        'doi': '10.1007/978-1-4020-6348-0_12',
                        'abstract': 'We present recent advances in understanding of the ground and excited states of the electron-phonon coupled systems obtained by novel methods of Diagrammatic Monte Carlo and Stochastic Optimization, which enable the approximation-free calculation of Matsubara Green function in imaginary times and perform unbiased analytic continuation to real frequencies. We present exact numeric results on the ground state properties, Lehmann spectral function and optical conductivity of different strongly correlated systems: Frohlich polaron, Rashba-Pekar exciton-polaron, pseudo Jahn-Teller polaron, exciton, and interacting with phonons hole in the t-J model.'}
    
    fake_clean_json_record = {'id': '0704.0025',
                        'created': '2007-04-02',
                        'updated': '2007-04-02',
                        'authors': "Author+1, Author+2",
                        'title': 'Spectroscopic Properties of Polarons in Strongly Correlated Systems byExact Diagrammatic Monte Carlo Method',
                        'doi': '10.1007/978-1-4020-6348-0_12',
                        'abstract': 'We present recent advances in understanding of the ground and excited states of the electron-phonon coupled systems obtained by novel methods of Diagrammatic Monte Carlo and Stochastic Optimization, which enable the approximation-free calculation of Matsubara Green function in imaginary times and perform unbiased analytic continuation to real frequencies. We present exact numeric results on the ground state properties, Lehmann spectral function and optical conductivity of different strongly correlated systems: Frohlich polaron, Rashba-Pekar exciton-polaron, pseudo Jahn-Teller polaron, exciton, and interacting with phonons hole in the t-J model.'}

    fake_clean_record_long_authors = {'id': '0704.0025',
                        'created': '2007-04-02',
                        'updated': '2007-04-02',
                        'authors': "Author+1, Author+2, Author+3, Author+4, Author+5, Author+6, Author+7, Author+8, Author+9, Author+10, Author+11, Author+12, ",
                        'title': 'Spectroscopic Properties of Polarons in Strongly Correlated Systems byExact Diagrammatic Monte Carlo Method',
                        'doi': '10.1007/978-1-4020-6348-0_12',
                        'abstract': 'We present recent advances in understanding of the ground and excited states of the electron-phonon coupled systems obtained by novel methods of Diagrammatic Monte Carlo and Stochastic Optimization, which enable the approximation-free calculation of Matsubara Green function in imaginary times and perform unbiased analytic continuation to real frequencies. We present exact numeric results on the ground state properties, Lehmann spectral function and optical conductivity of different strongly correlated systems: Frohlich polaron, Rashba-Pekar exciton-polaron, pseudo Jahn-Teller polaron, exciton, and interacting with phonons hole in the t-J model.'}

    fake_bad_xml_records = [None, """I am not an XML record.""", dict(), list()]
    fake_bad_json_records = [None, """I am not an JSON record.""", dict(), list()]

    fake_good_author_data = {'author':[{'keyname':'Einstein','forenames':'Albert','affiliation':'Princeton'},
                                {'keyname':'Curie','forenames':'Marie','affiliation':['1','2']},
                                {'keyname':'Ada Lovelace'}]}

    fake_bad_author_datas = [[None], ["""I am not author data."""],[ dict()], [list()]]

    fake_dirty_text = """
                There should be no linebreaks\n
                or multiple spaces                 in this sentence once processed.
                """