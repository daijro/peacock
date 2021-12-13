# RGB2Colorblind

RGB2Colorblind is an application to convert RGB/Hex values from a
full-color representation to simulate what a colorblind person might see.

**The objective of this tool is to give colorblind graphic designers the ability to translate "normally" colored RGB values back to their own scale of color perception, so that they can include colors in their work universally seen between them and their non-colorblind audience.**

[Coblis—Color Blindness Simulator](http://www.color-blindness.com/coblis-color-blindness-simulator/), [Peacock](https://github.com/jkulesza/peacock) and other such similar utilities are available, however they only offer full image conversion and not single colors. RGB2Colorblind is a fork of Peacock that was written to provide an offline mechanism for quering specific RGB/Hex values and translating them to various types of colorblindness.

The types of colorblindness that can be simulated are (with prevalence
information from [here](http://www.webexhibits.org/causesofcolor/2C.html) as
cited on
[Wikipedia](https://en.wikipedia.org/wiki/Color_blindness#Epidemiology)):

|                                                | **Males Affected (%)** | **Females Affected (%)** |
|:----------------------------------------------:|:----------------------:|:------------------------:|
|               **Dichromacy**                   |           2.4          |           0.03           |
|    Protanopia (red deficient: L cone absent)   |           1.3          |           0.02           |
|  Deuteranopia (green deficient: M cone absent) |           1.2          |           0.01           |
|   Tritanopia (blue deficient: S cone absent)   |          0.001         |           0.03           |
|          **Anomalous trichromacy**             |           6.3          |           0.37           |
|   Protanomaly (red deficient: L cone defect)   |           1.3          |           0.02           |
| Deuteranomaly (green deficient: M cone defect) |            5           |           0.35           |
|   Tritanomaly (blue deficient: S cone defect)  |         0.0001         |           0.001          |
|                 **Other**                      |                        |                          |
|     Monochromacy (total color blindness)       |          rare          |           rare           |


# Installation
Install the required packages using the `requirements.txt` file:
```
> pip install -r requirements.txt
```

# Usage

This script is used to convert "normally" colored RGB/Hex values to colorblind RGB/Hex values.

* Normal (normal vision)
* Protanopia (red-blind)
* Deuteranopia (green-blind)
* Tritanopia (blue-blind)
* Protanomaly (red-weak)
* Deuteranomaly (green-weak)
* Tritanomaly (blue-weak)
* Monochromacy (totally colorblind)

with the default action to convert to 'All' types of colorblindness (and to a normal vision version).  Converting to only a select type of colorblindness can be accomplished with the CB parameter described below.

The conversion processes and coefficients herein are used with permission
from Colblindor [http://www.color-blindness.com/] and were therein used with
permission of Matthew Wickline and the Human-Computer Interaction Resource
Network [http://www.hcirn.com/] for non-commercial purposes.  As such, this
code may only be used for non-commercial purposes.


Typical command line calls might look like:

**Converting RGB**
```
> python rgb2colorblind.py <r> <g> <b> --type <type>
```
**Converting Hex**
```
> python rgb2colorblind.py <hex>       --type <type>
```


# License Information<a name="LicneseInformation"></a>

The conversion processes and coefficients herein are used with permission from
[Colblindor](http://www.color-blindness.com/) and were therein used with
permission of Matthew Wickline and the [Human-Computer Interaction Resource
Network](http://www.hcirn.com/) for non-commercial purposes.  As such, this code
may only be used for non-commercial purposes.

[Original (Normal)
image](https://commons.wikimedia.org/wiki/File:Crayola_24pack_2005.jpg) above
obtained at the linked URL and is used under the Creative Commons
Attribution-Share Alike 3.0 Unported license.

Peacock++ uses the `args.hxx` header-only C++ command line option parser for
command line argument processing from [here](https://github.com/Taywee/args).
This file is used under the MIT license (see top of `args.hpp`).   More
information in [Peacock++'s README](cpp/README.md#OSSCredits).
