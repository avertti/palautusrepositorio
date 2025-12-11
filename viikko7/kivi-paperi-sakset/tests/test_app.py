import pytest
from app import app, WINNING_SCORE


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


class TestRoutes:
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data

    def test_index_clears_session(self, client):
        with client.session_transaction() as session:
            session['test_key'] = 'test_value'
        response = client.get('/')
        with client.session_transaction() as session:
            assert 'test_key' not in session

    def test_select_mode_pvp(self, client):
        response = client.post('/select_mode', data={'mode': 'pvp'})
        assert response.status_code == 302
        with client.session_transaction() as session:
            assert session['game_mode'] == 'pvp'

    def test_select_mode_easy(self, client):
        response = client.post('/select_mode', data={'mode': 'easy'})
        assert response.status_code == 302
        with client.session_transaction() as session:
            assert session['game_mode'] == 'easy'

    def test_make_move_pvp(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
        response = client.post('/make_move', data={'move': 'k', 'move2': 'p'})
        assert response.status_code == 200
        with client.session_transaction() as session:
            assert 'tuomari' in session
            assert session['tuomari']['tokan_pisteet'] == 1

    def test_game_continues_until_5_wins(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
        for i in range(4):
            response = client.post('/make_move', data={'move': 'k', 'move2': 's'})
            assert response.status_code == 200
        response = client.post('/make_move', data={'move': 'k', 'move2': 's'})
        assert response.status_code == 200
        assert b'player1' in response.data or b'Pelaaja 1 voitti' in response.data

    def test_play_redirects_to_game_over_when_won(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
            session['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 2, 'tasapelit': 0}
        response = client.get('/play')
        assert response.status_code == 302

    def test_game_over_route(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
            session['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 3, 'tasapelit': 1}
        response = client.get('/game_over')
        assert response.status_code == 200

    def test_game_over_redirects_if_no_winner(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
            session['tuomari'] = {'ekan_pisteet': 3, 'tokan_pisteet': 2, 'tasapelit': 0}
        response = client.get('/game_over')
        assert response.status_code == 302

    def test_winning_score_constant(self):
        assert WINNING_SCORE == 5

    def test_player2_can_win(self, client):
        with client.session_transaction() as session:
            session['game_mode'] = 'pvp'
        for i in range(5):
            client.post('/make_move', data={'move': 's', 'move2': 'k'})
        with client.session_transaction() as session:
            assert session['tuomari']['tokan_pisteet'] == 5
        response = client.get('/play')
        assert response.status_code == 302
