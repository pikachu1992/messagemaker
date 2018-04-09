# Message Maker [![Build Status](https://travis-ci.org/pedro2555/messagemaker.svg?branch=master)](https://travis-ci.org/pedro2555/messagemaker)

Message Maker provides ATIS services for VATSIM at LPPT, LPPR, LPFR, and LPMA airfields.
All ATIS text and recordings are intended to be as close, as is possible on VATSIM, to the real ATIS provided by NAV Portugal at the respective airfields.

Without disconsideration to the above, information deemed as not useful on VATSIM and/or in simulation may not be provided, dispite its publication on the real ATIS for the time or situation.

Message Maker is provided as free software under the terms of the GNU General Public License, version 2 of the license.
Other software used by Message Maker may be provided under different licenses, please refer to any 

## Euroscope Installation

1. Get the [latest audio package](https://github.com/pedro2555/messagemaker/releases/latest), extract to `Documents/Euroscope/messagemaker/`.

![image](https://user-images.githubusercontent.com/1645623/38401424-92d36974-394d-11e8-9bb0-c5e2535b1de8.png)

2. On the `Voice ATIS Setup Dialog` in Euroscope, select the `atisfiles.txt` included with the audio package

![image](https://user-images.githubusercontent.com/1645623/38401444-b149ae54-394d-11e8-9b5a-e95d8944f86e.png)

3. On the same dialog, replace your current `ATIS Maker URL` with:

    `https://messagemaker.herokuapp.com/?metar=$metar($atisairport)&rwy=$arrrwy($atisairport)&letter=$atiscode`

## Contributing

Make sure your contributions fall under projecto scope above, and submit either an issue or a pull request.

If your pull request includes code, make sure it includes test cases for, at least, the most basic functionality it provides.

Welcome changes:

 - PEP8. Thats a big failure from the start.
 
 - New API. The python-metar module, really does more than it should; I guess a metar parser, and metar (parsed) to ATIS translator is the proper way to go.
