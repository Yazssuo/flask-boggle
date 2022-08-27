from app import app
from unittest import TestCase

class BoggleEssentialTest(TestCase):
    """See if the game of boggle works, including POST request when game ends"""

    def test_start(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Start Game', html)
    
    def test_redirection_followed(self):
        with app.test_client() as client:
            resp = client.get("/start", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4 id="score">Score: 0</h4>', html)
    
    def test_guessing_ok(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E']]

            resp = client.get('/response?word=dog')
            self.assertEqual(resp.json['result'], 'ok')
    
    def test_guessing_no_board(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E']]

            resp = client.get('/response?word=cat')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_guessing_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E'],
                ['D','O','G','E','E']]

            resp = client.get('/response?word=gsdfkljghklsdjhgluidsbfgjlksdbnflugbduskly')
            self.assertEqual(resp.json['result'], 'not-a-word')
    
    


