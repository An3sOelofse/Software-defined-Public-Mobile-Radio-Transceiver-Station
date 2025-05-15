# Software-defined-Public-Mobile-Radio-Transceiver-Station

## Dependancies
Install Gnu Radio using

```
sudo apt-get install gnuradio
```

Install uhd library

```
sudo apt-get install libuhd-dev uhd-host
```

Make sure to add 

```
export UHD_IMAGES_DIR=/usr/local/share/uhd/images
```
to your ~/.bashrc file otherwise gnu radio does not recognise the SDR.

Next, clone this repository into your home folder.

## Running the software as is

Use the bash scripts in the "scripts" directory to run the FM radio or the walkie talkie.

```
./Software-defined-Public-Mobile-Radio-Transceiver-Station/scripts/fmradio.sh
```

## Generation the python files after changes made in Gnu-radio
First open the two files in the Heir blocks folder and build them (the downward arrow next to the play button)

Then open the demo2.grc file via the command line (this way gnu radio knows the UHD_IMAGES_DIR=/usr/local/share/uhd/images directory) .

```
gnuradio-companion demo2.grc 
```

click the reload blocks (blue arrow in a circle - top right) button and then press the play button to start.

Ensure that the laptop mic is not set to 100% otherwise the transmitted signal will be very noisy. Typical value used is 50%, but experiment for best results on specific hardware.


## WARNING

Always keep a 50 Ohm dummy load on the splitter or TX port of the SDR to prevent damage.


# Software-defined-Public-Mobile-Radio-Transceiver-Station
