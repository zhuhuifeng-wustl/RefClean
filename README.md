# RefClean
The latest update: 10/3/2019

## Description
This is a tool that can automatically deal with the duplicated reference items in the Letax project.
When writing the proposals/papers in Latex, sometimes we may have multiple bib files in one project. 
And we may cite the same paper using different names, especially when several people are working on one project.
This tool will deal with the duplicated bib items so you don't need to manually check them one by one.

## How to use it


1. Put all your bib files into one folder(The default folder is `./bib`).
You can set the folder name by setting `bib_path`.

2. Set the path and file name of the generated report through setting `rpt_path` and `rpt_name`.

3. Set the operation mode of RefClean. The default mode is `mode=0`, which only generates one report and do not make any modifications to the original files.
This means you need to delete the duplicated items manually and modify the `\cite{}` commands according to the report.
In the future version, I will make RelClean automatically do the latter steps.


## Why I want to write this tool
One time I participated in writing a proposal for NSF. There are five bib files in the Latex project. 
```bibtex
mybiblio.bib
ns.bib
proposal.bib
sslpub.bib
xzpubs.bib
```
These files are created by different people, so there exist multiple duplicated items. 
Some of them have the same cite name, which is obvious and can be detected by Latex comelier.
So this won't be a problem.
```bibtex
In ./bib/mybiblio.bib : 1382-1389 :
	@inproceedings{gnad2016analysis,
	  title={Analysis of transient voltage fluctuations in FPGAs},
	  author={Gnad, Dennis RE and Oboril, Fabian and Kiamehr, Saman and Tahoori, Mehdi B},
	  booktitle={Field-Programmable Technology (FPT), 2016 International Conference on},
	  pages={12--19},
	  year={2016},
	  organization={IEEE}
	}

In ./bib/mybiblio.bib : 2267-2274 :
	@inproceedings{gnad2016analysis,
	  title={Analysis of transient voltage fluctuations in FPGAs},
	  author={Gnad, Dennis RE and Oboril, Fabian and Kiamehr, Saman and Tahoori, Mehdi B},
	  booktitle={Field-Programmable Technology (FPT), 2016 International Conference on},
	  pages={12--19},
	  year={2016},
	  organization={IEEE}
	}
```

But some of them are duplicated in a quite sneaky way. For one paper, there may be several bib items with the different cite names, for example:
```bibtex
In ./bib/ns.bib : 66-75 :
	@article{walden1999analog,
	  title={Analog-to-digital converter survey and analysis},
	  author={Walden, Robert H},
	  journal={IEEE Journal on selected areas in communications},
	  volume={17},
	  number={4},
	  pages={539--550},
	  year={1999},
	  publisher={IEEE}
	}

In ./bib/proposal.bib : 498-506 :
	@ARTICLE{Walden, 
	author={R. H. Walden}, 
	journal={IEEE Journal on Selected Areas in Communications}, 
	title={Analog-to-digital converter survey and analysis}, 
	year={1999}, 
	volume={17}, 
	number={4}, 
	pages={539-550},  
	month={April},}
``` 
The former one is cited by `\cite{walden1999analog}` and the latter one is cited by `\cite{walden1999analog}`.
This would be a big problem because the Latex comelier cannot detect such duplications.

For the body part, each of us wrote a different part and we cited the same paper with different names.
Therefore in the complied `.pdf` file, there are several duplicated references.
From a reviewer's perspective, this kind of mistake is basically showing the authors are unprofessional. 

In this proposal, we totally cited about one hundred references.
At the final step of this proposal, we need to check the references to make sure there are no duplicated ones.
So I had to use `ctrl+F` to check them one by one, which is time-consuming and easy to make mistakes.

It took me a long long time to do this, but they still exist a mistake (I did not find it until the proposal was submitted....).
So I decided to write a tool automatically doing such "annoying works" and then there comes the RefClean.


## Update records

10/3/2019: Finish the first version of RefClean.