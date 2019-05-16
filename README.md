# SBtab-Explorer

A python GUI for working with SBtab files. 
Published early to allow for use, but code cleaning is currently underway.

![](https://img.shields.io/badge/version-0.1.0-yellow.svg) [![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Loading Models](#usage-loading-models)
  * [Editing Models](#usage-editing-models)
  * [Saving Models](#usage-saving-models)
* [Release History](#release-history)
* [Contributing and Versioning](#contributing-and-versioning)
* [License](#license)
* [Authors and Acknowledgements](#authors-and-acknowledgements)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for working with SBtab Files.

### Prerequisites
* Python 3
* The `openpyxl` python library is required to use SBtab Explorer. It can be used using the following command in command prompt/terminal
```
python -m pip install openpyxl
```

### Installation

To install SBtab Explorer, either download the repo as a zip, or clone the repo to a local location by opening a shell window in the desired install location and using:

```
git clone https://github.com/JakeHattwell/SBtab-Explorer.git
```

To use SBtab Explorer, run the `SBtabExplorer.py` file either through double-click or by running the following command in the directory the files are located in.
```
python SBtabExplorer.py
```
## Usage

#### Usage: Loading models

SBtab Explorer comes with a version of the [WormJam](ttps://gh.wormjam.life) genome scale model as a demo dataset.

To load the WormJam model, use the file menu, and select either **Open TSV** or **Open XLSX**. This will open a folder selection window. 

![](https://i.imgur.com/SbImbRa.png)
<small><i>Loading the model in TSV format</i></small>

Navigate to the WormJam folder in the install location and select the relevant filetype folder, and press Select Folder.

![](https://i.imgur.com/2h53lLA.png)
<small><i>Selecting the TSV folder of the WormJam Model. This **tsv** folder contains the SBtab files</i></small>

SBtab Explorer will then load your model for use.

![](https://i.imgur.com/k25nwDk.png)
<small><i>Model has been successfully loaded</i></small>

#### Usage: Editing models
Models can be searched using the search bar. Opening a search result will open an editor in a new tab.
![](https://i.imgur.com/EBIgh6v.png)
<small>*Left: A search for glucose. Right: An editor window for the first result.*</small>

On the left of the editor window is the link pane. The link pane has references to all of the entries that reference that particular entry.

New entries can be added using the **Tools** button. The list of available entry types will be autopopulated based on what SBtab files were present during the import.

**Note that saving an entry does not save your changes, only stores the changes in the open model. To save your work permanently, use the file menu.**

#### Usage: Saving models
To save your changes, use the `Save` or `Save As` options from the file menu.

## Email Submission
SBtab Explorer has a template available for Email Submission of updated SBtab files for curation efforts.

In the installation directory, edit the `settings.py` file in a text editor, changing the following variables:
```
EMAIL_SUBMISSION_ENABLED = True
EMAIL_SUBMISSION_ADDRESS = 'Target Email Address'
```

This will enable email submission of curation files and a `Submit` option will be added to the file menu.
![](https://i.imgur.com/j8jEgkl.png)
<small><i>Email submission form.</i></small>
Upon clicking Submit, a new prefilled email will opened, and the user can attach the relevant files to the email, before sending it.

## Release History

* 0.1.0
    * Changed repo to Public
    * Initial version of SBtab Interface

## Contributing and Versioning

1. Fork it (<https://github.com/jakehattwell/SBtab-Explorer/fork>)
2. Create your feature branch (`git checkout -b NewFeature`)
3. Commit your changes (`git commit -am 'Brief Description'`)
4. Push to the branch (`git push origin NewFeature`)
5. Create a new Pull Request

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## License


- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2019 © Jake Hattwell.

## Authors and Acknowledgements

* **Jake Hattwell** - *Initial work* - [@jakehattwell](https://twitter.com/JakeHattwell)

<!--See also the list of [contributors](https://github.com/jakehattwell/SBtab-Explorer/contributors) who participated in this project. WILL ADD WHEN MORE THAN ONE-->

Special thanks to:
* WormJam Consortium for feedback
* [Billie Thompson's](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) README template

Built with:
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Used for importing and exporting Excel files
