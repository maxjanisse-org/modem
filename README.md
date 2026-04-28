# Modem
## Description
This project is meant to represent the receiver of a 300 baud modem signal, allowing for the decoding of data as if it had bee transmitted over a phone line.

## Usage

### Python Environment
Run the provided script to set up and/or activate a Python environment. Use the command below to execute the script; notice that it starts with a period. This allows the activation of the Python environment to update the terminal used to execute the script.
```bash
. ./env-setup.bash
```
* If the directory hasn't been initialized, then the environment will be created, activated, and the required packages will be installed. 
* If the environment is initialized, but has not been activated, that will be taken care of.
* If the environment is initialized and activated, nothing will be done
* If you would like to remove the environment, using the `-R` argument.

### Running the Program
Use the following command to execute the program:
```bash
python3 modem.py
```
Configuration options are available as well (can also be seen by using `python3 modem.py -h`):
```bash
insert help options here
```

## My Story
This project started by translating the pseudocode for the tone detector from the assignment's document to Python; a fairly straight-forward process. Then, I implemented the code to read the WAV file and analyze the data by following the hints provided in the assignment document. The first step is to break up the samples of the sound into 160-bit long segments, then analyzes those segments to determine whether it's closer to the `mark` tone (2225 Hz) or the `space` tone (2025 Hz). If the segment is determined to be a `mark`, then a `1` is stored in the array that represents the binary form of the signal; otherwise, a `0` is added instead. 

Once that process is complete, there should now be an array of binary data that represents the original signal. This binary data, however, is still encoded following the 8N1 protocol, which means the data is constructed of 10-bit long segments each with 2 framing bits on either end, leaving 8 inner, LSB-ordered, bits of actual data. To perform the final conversion from the 8N1-formatted binary data to the message a loop is needed to iterate over the binary data in 10-bit chunks and, for each chunk, slice out the inner 8 values, reverse the order (putting them into the standard ordering), convert it to a string, then the string to an integer and then, ultimately, to the corresponding ASCII character. Once the loop is complete, the message that was encoded in the original signal should have been reconstructed.

Testing this approach went off without a hitch. I grabbed the provided `test1.wav` and `test2.wav` files, compared their output to the expected result and confirmed that they matched. I was further pleased when I ran my personal WAV file through the program and got the result found in the `MESSAGE.txt` file.
### Further Development Efforts
After feeling confident that I had successfully completed the assignment, I decided to at least try and tackle decoding the song by _Information Society_. As the assigment document mentions, some tweaks will be required but, in my case, the only one I've been able to make that affects anything positively, is to recognize when the number of samples read from the file won't work with the way I'm iterating over chunks of samples at a time. When I detect this scenario (which doesn't happen with the test or message files) I pad the beginning of the samples with enough zeros so that, at the very least, iterating over it in chunks won't go out-of-bounds.

Sadly, this does not get me a clean or complete result... but it does get me a dirty, partial result.
```
hÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿHCÂ  SO WE'RE SUPPOSED TO PLAY IN CURITIBA IN 18 HOURS, BUT OUR BUS IS BEING HELD
HOSTAGE BY THE LOCAL PROMOTERS. THEY'VE FORMED SOME UNHOLY ALLIANCE WITH THE
BRAZILIAN COUNTERPART OF ASCAP; THE PRS. APPARANTLY THE PRS HAS THE LEGAL POWER
<SNIP>
  WE KNEW IT WAS TIME FOR ACTION. PAUL WENT UP TO THE PRS GUYS AND INVITED 
THEM INTO THE BAR TO DISCUSS IT LIKE CIVILIZED MEN OVER A FEW BRÁZILIAN DRIKS,
▒HIOI@d ®¼ä@@▒î¦@@ @¨@@@@@¦@®²@X@®@¦¨@¨\▒@@@¦¨¨@¨\@¤ ▒¤ª@@¨@@¬¨@ ¨@¦@¨¤¦@@ª¦X@@¤¨@¤
```
It wasn't hard to guess that the `ÿ` represents the long tone at the beginning of the track (I later confirmed as being the 2225 Hz carrier, or `mark`, tone). But what really got me was the fact that I only got a _partial_ success here, why would it suddenly seem to start hallucinating before going into gibberish garbage? Honestly, I began to wonder if my copy of the track had been corrupted in some way (it'd be near impossible to tell by just _listening_ to it), which would be unfortunate, but at least it would explain this seemingly random failure. 

As I was doing my research, I stumbled upon someone using the program `minimodem` to do this exact activity, so I thought it would be a great way to prove the veracity of my own file. Running `minimodem -a 300 --ascii -f track.wav` produced a perfect result; the file is not my problem. Not a surprising result, but at least a welcome one.

### What's Next?