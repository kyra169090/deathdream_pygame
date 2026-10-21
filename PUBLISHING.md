# Publishing the browser version on itch.io

The game runs in the browser through [pygbag](https://github.com/pygame-web/pygbag), which packages a pygame game so it runs as WebAssembly. Players don't download an .exe, so antivirus software has nothing to flag.

## 1. Install pygbag (once)

```
python -m pip install pygbag
```

On Windows, use `py` instead of `python` if `python` isn't found. The build was tested with pygbag 0.9.3.

## 2. Test it locally

Run this from the folder that **contains** `deathdream_pygame` (not from inside it):

```
python -m pygbag deathdream_pygame
```

Open http://localhost:8000 in a browser. The first load takes a little while. Some browsers show "Ready to start! Please click/touch page"; click once and the game starts.

If something goes wrong, open http://localhost:8000/?debug#debug instead. That shows a terminal with Python's output and error messages next to the game.

Press Ctrl+C in the terminal to stop the server.

## 3. Build the upload file

From the same folder:

```
python -m pygbag --archive deathdream_pygame
```

This creates `deathdream_pygame/build/web.zip`. That zip is what goes on itch.io. The `build` folder is ignored by git, so it won't end up in the repo.

## 4. Upload to itch.io

1. Go to https://itch.io/dashboard and click **Edit** on Deathdream.
2. Set **Kind of project** to **HTML**.
3. Under **Uploads**, click **Upload files** and pick `build/web.zip`.
4. Tick **This file will be played in the browser** next to the upload.
5. Under **Embed options**:
   - **Viewport dimensions:** 1280 × 874 (the game is 1500 × 1024 and scales to fit, so any size with roughly that shape works).
   - Tick **Fullscreen button**, so players can make it big.
6. Click **Save**, then **View page** to try it.

You can keep the old Windows download on the same page if you want. Players will see the browser version first.

### Updating the game later

Rebuild with step 3, then on the Edit page delete the old `web.zip` upload, upload the new one, and tick **This file will be played in the browser** again.

## Rules for code that runs in the browser

The browser version has a few limits the desktop version doesn't:

- **No `pygame.time.delay()` or `time.sleep()`.** They freeze the browser tab. For "wait, then do something", use the scene's `self.wait(milliseconds, function)` (defined on `Node` in `slots_n_boxes.py`). Clicks are ignored until the function runs.
- **Keep `await asyncio.sleep(0)` at the end of the main loop** in `game.py`. Without it the browser never gets to draw a frame.
- **Use `.ogg` for sounds,** not `.mp3`. To convert, install ffmpeg and run:
  `ffmpeg -i sound.mp3 -c:a libvorbis -q:a 4 sound.ogg`
- **Filenames must match exactly, including upper/lowercase.** Windows treats `ladder.PNG` and `ladder.png` as the same file, but the browser doesn't.
- **No numpy** (`pygame.surfarray` needs it). It would work, but it makes players download several extra MB.
- **Import new libraries in the top-level `main.py`.** pygbag decides what to download by looking at the imports in that file. `pygame` is already there.

The desktop version still runs with `python main.py` from inside `src`, as before.
