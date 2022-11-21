
## Mixed Reality Window, v3, twilight edition


### Install Dependencies
- `pip install -r requirements.txt`


### Run on server
- `python server.py`


### Run on client
- `python client.py --device="guest"`
- `python client.py --device="window"`
- `python client.py --device="windowBack"`



### Docs for queue and multi-threading
look [here](https://docs.python.org/3/library/queue.html#queue.Queue.join) for examples



### TODOs
- [ ] try using worker threads for mediapipe processing?
- [ ] [audio clip support](https://github.com/jeffbass/imagezmq/issues/66). NOTE: THIS IS NOT AUDIO STREAMING


