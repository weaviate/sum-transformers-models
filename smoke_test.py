import unittest
import requests
import time

class SmokeTest(unittest.TestCase):
    def _waitForStartup(self):
        print('inside waitfor')
        url = 'http://localhost:8006/.well-known/ready'

        for i in range(0, 100):
            try:
                res = requests.get(url)
                if res.status_code == 204:
                    print('done')
                    return
                else:
                    raise Exception(
                            "status code is {}".format(res.status_code))
            except Exception as e:
                print("Attempt {}: {}".format(i, e))
                time.sleep(1)

        raise Exception("did not start up")

    def testNer(self):
        print('inside testNER')
        self._waitForStartup()
        url = 'http://localhost:8006/sum/'

        req_body = {'text': 'The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.'}
        
        try:
            res = requests.post(url, json=req_body)

        except Exception as e:
            print("e is {}".format(e))

        resBody = res.json()
        # print('response:',resBody)

        expected_result = {'text': 'The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.', 'summary': [{'result':'The Eiffel Tower is a landmark in Paris, France.'}]}
        
        self.assertEqual(200, res.status_code)
        self.assertEqual(req_body['text'], resBody['text'])
        self.assertEqual(len(resBody['summary']), len(expected_result['summary']))

        req_body = {'text': 'Hello how are you doing'}
        res = requests.post(url, json=req_body)
        resBody = res.json()

        print('response:',resBody)
        expected_result = {'text': 'Hello how are you doing', 'summary': [{'result':'How are you doing?'}]}
        
        self.assertEqual(200, res.status_code)
        self.assertEqual(req_body['text'], resBody['text'])
        self.assertCountEqual(resBody['summary'], expected_result['summary'])



if __name__ == "__main__":
    unittest.main()